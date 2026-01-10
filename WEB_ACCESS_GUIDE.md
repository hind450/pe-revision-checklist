# Quick Start: Web Interface Access Guide

## 🌐 Accessing the PE Assessment Web Interface

### Option 1: Local Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hind450/pe-revision-checklist.git
   cd pe-revision-checklist
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the web server:**

   **On Linux/Mac:**
   ```bash
   ./start_web.sh
   ```

   **On Windows:**
   ```
   start_web.bat
   ```

   **Or manually:**
   ```bash
   cd web
   python app.py
   ```

4. **Access in browser:**
   Open your web browser and go to:
   ```
   http://localhost:5000
   ```

### Option 2: Deploy to Cloud Service

#### Deploy to Heroku (Free Tier)

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create pe-assessment-app
   ```

3. **Add Procfile:**
   Create `Procfile` in root:
   ```
   web: cd web && gunicorn app:app
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Access:**
   ```
   https://pe-assessment-app.herokuapp.com
   ```

#### Deploy to PythonAnywhere (Free Tier)

1. **Sign up** at https://www.pythonanywhere.com

2. **Upload code** via Files tab or Git

3. **Create web app:**
   - Click "Web" tab
   - Add new web app
   - Select Flask
   - Point to `web/app.py`

4. **Configure:**
   - Set working directory to `/home/yourusername/pe-revision-checklist/web`
   - Set virtualenv if needed

5. **Access:**
   ```
   https://yourusername.pythonanywhere.com
   ```

#### Deploy to Render (Free Tier)

1. **Sign up** at https://render.com

2. **Create new Web Service:**
   - Connect GitHub repository
   - Select branch
   - Build command: `pip install -r requirements.txt`
   - Start command: `cd web && gunicorn app:app`

3. **Access:**
   ```
   https://your-app-name.onrender.com
   ```

## 📋 System Requirements

- Python 3.9 or higher
- 500MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🎯 How to Use

### Step 1: Upload Mark Scheme
1. Click "Upload Mark Scheme"
2. Select your PDF or DOCX mark scheme file
3. Wait for "Mark scheme loaded successfully" message
4. Automatic redirect to student upload

### Step 2: Upload Student Scripts
1. Click "Choose Files" and select one or more PDF files
2. Hold Ctrl (Windows) or Cmd (Mac) to select multiple files
3. Click "Process Student Scripts"
4. Wait for processing (may take 30 seconds per student)

### Step 3: Download Reports
1. View results summary
2. Download individual student reports (TXT or CSV)
3. Download class analytics report
4. Download student summary CSV

## 🔒 Security Notes

**For testing/local use:** Current setup is fine

**For production/public deployment:**
1. Change secret key in `web/app.py`
2. Add user authentication
3. Set up HTTPS
4. Configure file cleanup
5. Add rate limiting
6. Use production WSGI server (Gunicorn)

## ⚡ Quick Test

Want to test without real data?

1. Create sample files:
   - Mark scheme: Any PDF with "Q1", "Q2" structure
   - Student script: Any PDF with same question numbers

2. The system will extract and attempt to mark

3. Review generated reports to see output format

## 📞 Need Help?

- Check `web/README.md` for detailed documentation
- Review main `README.md` for system features
- See `examples/example_workflow.py` for code usage
- Check GitHub issues for known problems

## 🚀 Quick Links

- **Repository**: https://github.com/hind450/pe-revision-checklist
- **Documentation**: See README.md files
- **Web Interface Code**: `/web` directory
- **Examples**: `/examples` directory
