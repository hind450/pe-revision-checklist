"""
Flask Web Application for PE Assessment System
Provides web interface for uploading mark schemes and student scripts
"""

import os
import sys
import json
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
app.config['DATA_FOLDER'] = Path(__file__).parent / 'data'

# Create necessary directories
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(exist_ok=True)
app.config['DATA_FOLDER'].mkdir(exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Global system instance and class data
pe_system = None
classes_data = {}
assessments_data = {}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_classes_data():
    """Load classes data from JSON file"""
    global classes_data
    classes_file = app.config['DATA_FOLDER'] / 'classes.json'
    if classes_file.exists():
        with open(classes_file, 'r') as f:
            classes_data = json.load(f)
    else:
        classes_data = {}
    return classes_data


def save_classes_data():
    """Save classes data to JSON file"""
    classes_file = app.config['DATA_FOLDER'] / 'classes.json'
    with open(classes_file, 'w') as f:
        json.dump(classes_data, f, indent=2)


def load_assessments_data():
    """Load assessments data from JSON file"""
    global assessments_data
    assessments_file = app.config['DATA_FOLDER'] / 'assessments.json'
    if assessments_file.exists():
        with open(assessments_file, 'r') as f:
            assessments_data = json.load(f)
    else:
        assessments_data = {}
    return assessments_data


def save_assessments_data():
    """Save assessments data to JSON file"""
    assessments_file = app.config['DATA_FOLDER'] / 'assessments.json'
    with open(assessments_file, 'w') as f:
        json.dump(assessments_data, f, indent=2)


# Load data on startup
load_classes_data()
load_assessments_data()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Teacher dashboard"""
    load_classes_data()
    load_assessments_data()
    
    # Get list of classes
    class_names = list(classes_data.keys())
    
    # Get classes with mark schemes
    classes_with_mark_schemes = [
        class_name for class_name, data in classes_data.items()
        if data.get('mark_scheme_uploaded')
    ]
    
    # Get recent results
    recent_results = []
    for assessment_id, assessment_data in assessments_data.items():
        recent_results.append({
            'class_name': assessment_data.get('class_name', 'Unknown'),
            'assessment_name': assessment_data.get('assessment_name', 'Unnamed'),
            'student_count': assessment_data.get('student_count', 0),
            'date': assessment_data.get('date', 'Unknown'),
            'assessment_id': assessment_id
        })
    
    # Sort by date (most recent first)
    recent_results.sort(key=lambda x: x['date'], reverse=True)
    recent_results = recent_results[:10]  # Show last 10
    
    return render_template('dashboard.html',
                         classes=class_names,
                         classes_with_mark_schemes=classes_with_mark_schemes,
                         recent_results=recent_results,
                         mark_scheme_status=None)


@app.route('/add_class', methods=['POST'])
def add_class():
    """Add a new class"""
    class_name = request.form.get('class_name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not class_name:
        flash('Class name is required', 'error')
        return redirect(url_for('dashboard'))
    
    load_classes_data()
    
    if class_name in classes_data:
        flash(f'Class "{class_name}" already exists', 'error')
        return redirect(url_for('dashboard'))
    
    classes_data[class_name] = {
        'description': description,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mark_scheme_uploaded': False,
        'assessments': []
    }
    
    save_classes_data()
    flash(f'Class "{class_name}" added successfully', 'success')
    return redirect(url_for('dashboard'))


@app.route('/edit_class', methods=['POST'])
def edit_class():
    """Edit a class name"""
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    
    if not old_name or not new_name:
        return jsonify({'success': False, 'message': 'Invalid data'})
    
    load_classes_data()
    
    if old_name not in classes_data:
        return jsonify({'success': False, 'message': 'Class not found'})
    
    if new_name in classes_data and new_name != old_name:
        return jsonify({'success': False, 'message': 'Class name already exists'})
    
    # Rename class
    classes_data[new_name] = classes_data.pop(old_name)
    save_classes_data()
    
    # Update assessments data
    load_assessments_data()
    for assessment_id, assessment_data in assessments_data.items():
        if assessment_data.get('class_name') == old_name:
            assessment_data['class_name'] = new_name
    save_assessments_data()
    
    return jsonify({'success': True})


@app.route('/delete_class', methods=['POST'])
def delete_class():
    """Delete a class"""
    data = request.get_json()
    class_name = data.get('class_name')
    
    if not class_name:
        return jsonify({'success': False, 'message': 'Invalid data'})
    
    load_classes_data()
    
    if class_name not in classes_data:
        return jsonify({'success': False, 'message': 'Class not found'})
    
    # Delete class
    del classes_data[class_name]
    save_classes_data()
    
    # Delete associated assessments
    load_assessments_data()
    assessments_to_delete = [
        aid for aid, adata in assessments_data.items()
        if adata.get('class_name') == class_name
    ]
    for aid in assessments_to_delete:
        del assessments_data[aid]
    save_assessments_data()
    
    return jsonify({'success': True})


@app.route('/dashboard/upload_mark_scheme', methods=['POST'])
def dashboard_upload_mark_scheme():
    """Upload mark scheme from dashboard"""
    class_name = request.form.get('class_name')
    assessment_name = request.form.get('assessment_name', '').strip()
    
    if not class_name or not assessment_name:
        flash('Class name and assessment name are required', 'error')
        return redirect(url_for('dashboard'))
    
    if 'mark_scheme' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    file = request.files['mark_scheme']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # Initialize PE system and load mark scheme
        global pe_system
        try:
            output_dir = app.config['OUTPUT_FOLDER'] / f"{class_name}_{timestamp}"
            output_dir.mkdir(exist_ok=True)
            
            pe_system = PEAssessmentSystem(output_dir=str(output_dir))
            mark_scheme = pe_system.load_mark_scheme(str(filepath))
            
            # Update class data
            load_classes_data()
            if class_name in classes_data:
                classes_data[class_name]['mark_scheme_uploaded'] = True
                classes_data[class_name]['last_mark_scheme'] = str(filepath)
                classes_data[class_name]['last_assessment_name'] = assessment_name
                classes_data[class_name]['last_timestamp'] = timestamp
                save_classes_data()
            
            flash(f'Mark scheme "{assessment_name}" loaded for {class_name}! {len(mark_scheme.mark_criteria)} questions found.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error loading mark scheme: {str(e)}', 'error')
            logger.error(f"Error loading mark scheme: {e}")
            return redirect(url_for('dashboard'))
    else:
        flash('Invalid file type. Please upload PDF or DOCX.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/dashboard/upload_students', methods=['POST'])
def dashboard_upload_students():
    """Upload student scripts from dashboard"""
    global pe_system
    
    class_name = request.form.get('class_name')
    
    if not class_name:
        flash('Please select a class', 'error')
        return redirect(url_for('dashboard'))
    
    load_classes_data()
    if class_name not in classes_data or not classes_data[class_name].get('mark_scheme_uploaded'):
        flash('Please upload a mark scheme for this class first', 'error')
        return redirect(url_for('dashboard'))
    
    # Reinitialize PE system with the class's mark scheme
    try:
        mark_scheme_path = classes_data[class_name].get('last_mark_scheme')
        timestamp = classes_data[class_name].get('last_timestamp')
        assessment_name = classes_data[class_name].get('last_assessment_name', 'Assessment')
        
        output_dir = app.config['OUTPUT_FOLDER'] / f"{class_name}_{timestamp}"
        output_dir.mkdir(exist_ok=True)
        
        pe_system = PEAssessmentSystem(output_dir=str(output_dir))
        pe_system.load_mark_scheme(mark_scheme_path)
    except Exception as e:
        flash(f'Error loading mark scheme: {str(e)}', 'error')
        return redirect(url_for('dashboard'))
    
    if 'student_scripts' not in request.files:
        flash('No files selected', 'error')
        return redirect(url_for('dashboard'))
    
    files = request.files.getlist('student_scripts')
    
    if not files or files[0].filename == '':
        flash('No files selected', 'error')
        return redirect(url_for('dashboard'))
    
    # Process uploaded files
    uploaded_files = []
    student_ids = []
    student_names = []
    
    current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for idx, file in enumerate(files):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{current_timestamp}_{filename}"
            filepath = app.config['UPLOAD_FOLDER'] / filename
            file.save(filepath)
            
            uploaded_files.append(str(filepath))
            student_ids.append(f"S{idx+1:03d}")
            
            # Extract student name from filename or use default
            student_name = file.filename.rsplit('.', 1)[0]
            student_names.append(student_name)
    
    if not uploaded_files:
        flash('No valid files uploaded', 'error')
        return redirect(url_for('dashboard'))
    
    # Process student scripts
    try:
        reports = pe_system.process_batch(
            uploaded_files,
            student_ids,
            student_names
        )
        
        # Generate class analytics
        class_id = f"{class_name}_{current_timestamp}"
        analytics = pe_system.generate_class_analytics(class_id, reports)
        
        # Export reports
        pe_system.export_reports(reports, analytics, format='both')
        
        # Save assessment data
        assessment_id = f"{class_name}_{current_timestamp}"
        load_assessments_data()
        assessments_data[assessment_id] = {
            'class_name': class_name,
            'assessment_name': assessment_name,
            'student_count': len(reports),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'output_dir': str(output_dir),
            'timestamp': current_timestamp
        }
        save_assessments_data()
        
        # Update class data
        if class_name in classes_data:
            if 'assessments' not in classes_data[class_name]:
                classes_data[class_name]['assessments'] = []
            classes_data[class_name]['assessments'].append(assessment_id)
            save_classes_data()
        
        flash(f'Successfully processed {len(reports)} student scripts for {class_name}!', 'success')
        return redirect(url_for('view_class_results', class_name=class_name, assessment_id=assessment_id))
    except Exception as e:
        flash(f'Error processing student scripts: {str(e)}', 'error')
        logger.error(f"Error processing students: {e}")
        return redirect(url_for('dashboard'))


@app.route('/results/<class_name>/<assessment_id>')
def view_class_results(class_name, assessment_id):
    """View results for a specific class assessment"""
    load_assessments_data()
    
    if assessment_id not in assessments_data:
        flash('Assessment not found', 'error')
        return redirect(url_for('dashboard'))
    
    assessment_data = assessments_data[assessment_id]
    output_dir = Path(assessment_data['output_dir'])
    
    # Get list of files
    student_reports = list(output_dir.glob('student_*_report.txt'))
    class_analytics_txt = list(output_dir.glob('class_*_analytics.txt'))
    class_analytics_csv = list(output_dir.glob('class_*_analytics.csv'))
    student_summary_csv = list(output_dir.glob('class_student_summary.csv'))
    
    # Parse student data (simplified for now)
    students = []
    for report_file in student_reports:
        student_name = report_file.stem.replace('student_', '').replace('_report', '')
        student_id = student_name.split('_')[0] if '_' in student_name else student_name
        
        # Try to extract score from file (basic parsing)
        score = 0
        performance_level = 'red'
        try:
            with open(report_file, 'r') as f:
                content = f.read()
                if 'Total Score:' in content:
                    score_line = [line for line in content.split('\n') if 'Total Score:' in line][0]
                    score = int(score_line.split(':')[1].split('%')[0].strip())
                    if score >= 70:
                        performance_level = 'green'
                    elif score >= 50:
                        performance_level = 'amber'
        except:
            pass
        
        students.append({
            'name': student_name.replace('_', ' '),
            'id': student_id,
            'score': score,
            'performance_level': performance_level,
            'report_txt': report_file.name,
            'report_csv': report_file.name.replace('.txt', '.csv')
        })
    
    # Basic class analytics (simplified)
    class_analytics = {
        'average_score': sum(s['score'] for s in students) // len(students) if students else 0,
        'highest_score': max((s['score'] for s in students), default=0),
        'lowest_score': min((s['score'] for s in students), default=0)
    }
    
    return render_template('class_results.html',
                         class_name=class_name,
                         assessment_name=assessment_data.get('assessment_name', 'Assessment'),
                         date=assessment_data.get('date', 'Unknown'),
                         student_count=len(students),
                         students=students,
                         class_analytics=class_analytics,
                         class_analytics_txt=class_analytics_txt[0].name if class_analytics_txt else '',
                         class_analytics_csv=class_analytics_csv[0].name if class_analytics_csv else '',
                         student_summary_csv=student_summary_csv[0].name if student_summary_csv else '',
                         misconceptions=[],
                         recommendations=[])


@app.route('/download/<filename>')
def download(filename):
    """Download a report file - search across all output directories"""
    # Search in all subdirectories of OUTPUT_FOLDER
    output_base = app.config['OUTPUT_FOLDER']
    
    for subdir in output_base.iterdir():
        if subdir.is_dir():
            filepath = subdir / filename
            if filepath.exists():
                return send_file(filepath, as_attachment=True)
    
    flash('File not found', 'error')
    return redirect(url_for('dashboard'))


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
