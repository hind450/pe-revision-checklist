"""
Flask Web Application for PE Assessment System
Provides web interface for uploading mark schemes and student scripts
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import PEAssessmentSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'pe-assessment-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['OUTPUT_FOLDER'] = Path(__file__).parent / 'outputs'

# Create necessary directories
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Global system instance
pe_system = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload_mark_scheme', methods=['GET', 'POST'])
def upload_mark_scheme():
    """Upload mark scheme page"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'mark_scheme' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['mark_scheme']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = app.config['UPLOAD_FOLDER'] / filename
            file.save(filepath)
            
            # Initialize PE system and load mark scheme
            global pe_system
            try:
                output_dir = app.config['OUTPUT_FOLDER'] / timestamp
                output_dir.mkdir(exist_ok=True)
                
                pe_system = PEAssessmentSystem(output_dir=str(output_dir))
                mark_scheme = pe_system.load_mark_scheme(str(filepath))
                
                flash(f'Mark scheme loaded successfully! {len(mark_scheme.mark_criteria)} questions found.', 'success')
                return redirect(url_for('upload_students'))
            except Exception as e:
                flash(f'Error loading mark scheme: {str(e)}', 'error')
                logger.error(f"Error loading mark scheme: {e}")
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload PDF or DOCX.', 'error')
            return redirect(request.url)
    
    return render_template('upload_mark_scheme.html')


@app.route('/upload_students', methods=['GET', 'POST'])
def upload_students():
    """Upload student scripts page"""
    global pe_system
    
    if pe_system is None:
        flash('Please upload a mark scheme first', 'error')
        return redirect(url_for('upload_mark_scheme'))
    
    if request.method == 'POST':
        # Check if files were uploaded
        if 'student_scripts' not in request.files:
            flash('No files selected', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('student_scripts')
        
        if not files or files[0].filename == '':
            flash('No files selected', 'error')
            return redirect(request.url)
        
        # Process uploaded files
        uploaded_files = []
        student_ids = []
        student_names = []
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for idx, file in enumerate(files):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{timestamp}_{filename}"
                filepath = app.config['UPLOAD_FOLDER'] / filename
                file.save(filepath)
                
                uploaded_files.append(str(filepath))
                student_ids.append(f"S{idx+1:03d}")
                
                # Extract student name from filename or use default
                student_name = file.filename.rsplit('.', 1)[0]
                student_names.append(student_name)
        
        if not uploaded_files:
            flash('No valid files uploaded', 'error')
            return redirect(request.url)
        
        # Process student scripts
        try:
            reports = pe_system.process_batch(
                uploaded_files,
                student_ids,
                student_names
            )
            
            # Generate class analytics
            class_id = f"Class_{timestamp}"
            analytics = pe_system.generate_class_analytics(class_id, reports)
            
            # Export reports
            pe_system.export_reports(reports, analytics, format='both')
            
            flash(f'Successfully processed {len(reports)} student scripts!', 'success')
            return redirect(url_for('results', class_id=class_id))
        except Exception as e:
            flash(f'Error processing student scripts: {str(e)}', 'error')
            logger.error(f"Error processing students: {e}")
            return redirect(request.url)
    
    return render_template('upload_students.html')


@app.route('/results/<class_id>')
def results(class_id):
    """Display results page"""
    global pe_system
    
    if pe_system is None:
        flash('No data available', 'error')
        return redirect(url_for('index'))
    
    # Find output files
    output_dir = Path(pe_system.output_dir)
    
    # Get list of student reports
    student_reports = list(output_dir.glob('student_*_report.txt'))
    class_analytics = list(output_dir.glob('class_*_analytics.txt'))
    csv_files = list(output_dir.glob('*.csv'))
    
    files = {
        'student_reports': [f.name for f in student_reports],
        'class_analytics': [f.name for f in class_analytics],
        'csv_files': [f.name for f in csv_files]
    }
    
    return render_template('results.html', 
                         class_id=class_id,
                         student_count=len(student_reports),
                         files=files)


@app.route('/download/<filename>')
def download(filename):
    """Download a report file"""
    global pe_system
    
    if pe_system is None:
        flash('No data available', 'error')
        return redirect(url_for('index'))
    
    output_dir = Path(pe_system.output_dir)
    filepath = output_dir / filename
    
    if filepath.exists():
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found', 'error')
        return redirect(url_for('index'))


@app.route('/reset')
def reset():
    """Reset the system"""
    global pe_system
    pe_system = None
    flash('System reset. You can now upload a new mark scheme.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("=" * 80)
    print("PE Assessment for Learning - Web Interface")
    print("=" * 80)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
