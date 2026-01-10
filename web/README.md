# PE Assessment System - Web Interface

Web-based interface for the PE Assessment for Learning system, allowing teachers to upload mark schemes and student scripts through a browser.

## Features

- 📤 **Upload Mark Schemes**: PDF or DOCX format
- 📝 **Upload Student Scripts**: Multiple PDF files in batch
- 📊 **View Results**: Download individual and class reports
- 🎨 **User-Friendly Interface**: Clean, responsive design
- 📥 **Export Reports**: TXT and CSV formats

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Run the web server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Step 1: Upload Mark Scheme
1. Click "Upload Mark Scheme" in the navigation
2. Select your mark scheme file (PDF or DOCX)
3. Click "Upload Mark Scheme"
4. Wait for confirmation that the mark scheme was loaded successfully

### Step 2: Upload Student Scripts
1. After uploading the mark scheme, you'll be redirected to upload students
2. Select one or more student script PDFs (use Ctrl/Cmd+Click for multiple)
3. Click "Process Student Scripts"
4. Wait for processing to complete

### Step 3: Download Results
1. View the results summary showing number of students processed
2. Download individual student reports (TXT or CSV)
3. Download class analytics report
4. Download CSV summary file

## File Requirements

### Mark Scheme
- **Format**: PDF or DOCX
- **Max Size**: 16MB
- **Content**: Must include:
  - Question numbers (Q1, Question 1a, etc.)
  - Marks allocation
  - Acceptable answers or criteria

### Student Scripts
- **Format**: PDF only
- **Max Size**: 16MB per file
- **Content**: Must include:
  - Question numbers matching mark scheme
  - Student answers
- **Filename**: Used as student name (e.g., "John_Smith.pdf" → "John_Smith")

## Directory Structure

```
web/
├── app.py                 # Flask application
├── templates/            # HTML templates
│   ├── base.html        # Base layout
│   ├── index.html       # Home page
│   ├── upload_mark_scheme.html
│   ├── upload_students.html
│   └── results.html     # Results and downloads
├── static/              # Static files
│   └── css/
│       └── style.css    # Styles
├── uploads/             # Temporary upload storage
└── outputs/             # Generated reports
```

## API Endpoints

- `GET /` - Home page
- `GET/POST /upload_mark_scheme` - Upload mark scheme
- `GET/POST /upload_students` - Upload student scripts
- `GET /results/<class_id>` - View results
- `GET /download/<filename>` - Download report file
- `GET /reset` - Reset system and start over

## Configuration

Edit `app.py` to modify:
- `MAX_CONTENT_LENGTH` - Maximum file size (default: 16MB)
- `UPLOAD_FOLDER` - Location for uploaded files
- `OUTPUT_FOLDER` - Location for generated reports
- Port number (default: 5000)

## Production Deployment

For production use:

1. **Change the secret key** in `app.py`:
```python
app.secret_key = 'your-secure-random-secret-key'
```

2. **Disable debug mode**:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

3. **Use a production WSGI server** (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Set up reverse proxy** (e.g., Nginx) for HTTPS

5. **Configure proper file storage** with size limits and cleanup

## Troubleshooting

### "Mark scheme not loaded" error
- Ensure PDF/DOCX is valid and not corrupted
- Check that the file contains proper question formatting
- Review server logs for specific error messages

### "No files selected" error
- Make sure you've selected files before clicking submit
- Check that files are in PDF format for student scripts
- Verify files are under 16MB size limit

### Processing takes too long
- Large PDF files may take time to process
- Multiple student scripts will take longer
- Check server logs for progress

### Cannot download reports
- Ensure processing completed successfully
- Check that output directory has write permissions
- Verify files exist in the outputs folder

## Security Notes

- ⚠️ **Change the secret key** before production deployment
- 🔒 Files are stored temporarily on the server
- 🗑️ Consider implementing cleanup for old uploads
- 🔐 Add authentication for production use
- 🛡️ Configure appropriate CORS settings

## Support

For issues or questions:
- Check the main README in the repository root
- Review the USER_GUIDE in docs/
- See example_workflow.py for code examples
