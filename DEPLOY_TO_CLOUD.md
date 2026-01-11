# Deploy PE Assessment System to Cloud (Free)

Get your own public URL in under 10 minutes using free hosting services.

## 🚀 Option 1: Render.com (Recommended - Easiest)

**Time: 5-10 minutes | Free tier available**

### Step-by-Step:

1. **Sign up at Render.com:**
   - Go to https://render.com
   - Click "Get Started" and sign up (GitHub login recommended)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the `pe-revision-checklist` repository
   - Branch: `copilot/add-automated-marking-system-again`

3. **Configure Service:**
   ```
   Name: pe-assessment-app (or your choice)
   Region: Choose closest to you
   Branch: copilot/add-automated-marking-system-again
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd web && gunicorn app:app
   ```

4. **Add Environment Variables:**
   - Click "Advanced"
   - Add: `PYTHON_VERSION` = `3.9.0`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - You'll get a URL like: `https://pe-assessment-app.onrender.com`

6. **Access Your Site:**
   - Click the URL Render provides
   - You now have a public website!

**Note:** Render free tier may sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## 🐍 Option 2: PythonAnywhere

**Time: 10-15 minutes | Free tier: 1 web app**

### Step-by-Step:

1. **Sign up:**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Code:**
   - Go to "Files" tab
   - Click "Open Bash console"
   - Run:
     ```bash
     git clone https://github.com/hind450/pe-revision-checklist.git
     cd pe-revision-checklist
     git checkout copilot/add-automated-marking-system-again
     ```

3. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.9

4. **Configure:**
   - Source code: `/home/yourusername/pe-revision-checklist/web`
   - Working directory: `/home/yourusername/pe-revision-checklist/web`
   - WSGI file: Edit to add:
     ```python
     import sys
     path = '/home/yourusername/pe-revision-checklist'
     if path not in sys.path:
         sys.path.append(path)
     
     from web.app import app as application
     ```

5. **Install Dependencies:**
   - Open Bash console
   - Run:
     ```bash
     pip install --user flask werkzeug
     ```

6. **Reload:**
   - Go back to "Web" tab
   - Click green "Reload" button
   - Your URL: `https://yourusername.pythonanywhere.com`

---

## ☁️ Option 3: Heroku

**Time: 10 minutes | Free tier available (requires credit card verification)**

### Step-by-Step:

1. **Prerequisites:**
   ```bash
   # Install Heroku CLI
   # Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
   # Mac: brew tap heroku/brew && brew install heroku
   # Linux: curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Prepare App:**
   ```bash
   cd pe-revision-checklist
   
   # Create Procfile
   echo "web: cd web && gunicorn app:app" > Procfile
   
   # Create runtime.txt
   echo "python-3.9.18" > runtime.txt
   ```

4. **Deploy:**
   ```bash
   heroku create pe-assessment-app
   git push heroku copilot/add-automated-marking-system-again:main
   heroku open
   ```

5. **Your URL:**
   - `https://pe-assessment-app.herokuapp.com`

---

## 🔧 Option 4: Railway.app

**Time: 5 minutes | $5 free credit monthly**

### Step-by-Step:

1. **Sign up:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `pe-revision-checklist`
   - Railway auto-detects Python and deploys

3. **Configure:**
   - Go to Settings
   - Add Start Command: `cd web && gunicorn app:app`
   - Add environment variable if needed

4. **Get URL:**
   - Go to Settings → Domains
   - Generate domain
   - URL: `https://your-app.railway.app`

---

## 📦 Requirements for All Options

You'll need to add `gunicorn` to requirements.txt for production deployment:

```bash
echo "gunicorn>=20.1.0" >> requirements.txt
```

---

## ⚡ Quick Local Test (1 minute)

Before deploying, test locally:

```bash
git clone https://github.com/hind450/pe-revision-checklist.git
cd pe-revision-checklist
pip install flask werkzeug
cd web
python app.py
# Open http://localhost:5000
```

---

## 🎯 Which Option Should You Choose?

| Service | Best For | Speed | Free Tier Limits |
|---------|----------|-------|------------------|
| **Render** | Quick deploy, persistent | ⚡⚡⚡ | Sleeps after 15 min idle |
| **PythonAnywhere** | Python-specific, educational | ⚡⚡ | 1 web app, always-on |
| **Heroku** | Professional, established | ⚡⚡ | Requires card, limited hours |
| **Railway** | Modern, simple | ⚡⚡⚡ | $5 credit/month |

**Recommendation:** Start with **Render.com** - it's the easiest and works great for testing.

---

## 🐛 Troubleshooting

**Deployment fails:**
- Check Python version is 3.9+
- Ensure all dependencies in requirements.txt
- Check logs in deployment service

**App doesn't load:**
- Wait 30-60 seconds (free tiers are slower)
- Check if service is "sleeping" and wake it
- Review error logs

**File upload errors:**
- Check file size limits (most free tiers: 10-50MB)
- Ensure upload directory has write permissions

---

## 🔒 Security Note

For testing/demo purposes, the current configuration is fine. For production use:

1. Change `secret_key` in `web/app.py`
2. Add authentication/authorization
3. Set up HTTPS (most platforms do this automatically)
4. Configure proper file storage and cleanup

---

## 💡 Need Help?

- Check service-specific documentation
- Review error logs in deployment dashboard
- Test locally first to verify it works
- Open GitHub issue if deployment guides need updates
