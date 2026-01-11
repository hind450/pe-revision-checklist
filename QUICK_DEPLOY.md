# 🚀 One-Click Deploy to Cloud

Get your PE Assessment System running online in under 5 minutes!

## ⚡ Fastest Option: Deploy to Render

Click this button to deploy instantly:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**After clicking:**
1. Sign in to Render (or create free account)
2. Repository will auto-populate from GitHub
3. Click "Create Web Service"
4. Wait 3-5 minutes
5. You'll get a URL like: `https://pe-assessment-system.onrender.com`
6. Done! Open the URL in your browser

---

## 🎯 Alternative: Manual Deploy (5 minutes)

### Render.com (Recommended)

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect this GitHub repository
4. Use these settings:
   - **Name**: `pe-assessment-app`
   - **Branch**: `copilot/add-automated-marking-system-again`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd web && gunicorn app:app`
   - **Environment**: Python 3
5. Click "Create Web Service"
6. Access your URL when deployment completes!

### Railway.app

1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway auto-deploys!
5. Go to Settings → Generate Domain
6. Access your URL!

### Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Run in terminal:
   ```bash
   git clone https://github.com/hind450/pe-revision-checklist.git
   cd pe-revision-checklist
   heroku login
   heroku create
   git push heroku copilot/add-automated-marking-system-again:main
   heroku open
   ```

---

## 🏠 Local Testing (1 minute)

Prefer to run locally first?

```bash
git clone https://github.com/hind450/pe-revision-checklist.git
cd pe-revision-checklist
pip install flask werkzeug gunicorn
cd web
python app.py
```

Open `http://localhost:5000` in your browser.

---

## 📋 What You Get

Once deployed, you'll have a live website where you can:
- ✅ Upload mark schemes (PDF/DOCX)
- ✅ Upload student scripts (multiple PDFs)
- ✅ Get automated marking with AI
- ✅ Download individual student reports
- ✅ Download class analytics
- ✅ View traffic light performance indicators
- ✅ Access from any device with internet

---

## 💰 Cost

All recommended platforms offer FREE tiers:
- **Render**: Free (sleeps after 15 min idle)
- **Railway**: $5 free credit monthly
- **Heroku**: Free (requires card verification)
- **PythonAnywhere**: Free (1 web app)

Perfect for testing and educational use!

---

## 🆘 Need Help?

- **Not working?** See `DEPLOY_TO_CLOUD.md` for detailed troubleshooting
- **Questions?** Check `web/README.md` for usage guide
- **Issues?** Open a GitHub issue

## 🎓 Ready to Test?

1. Deploy using one of the methods above (5 minutes)
2. Open your new URL
3. Upload a mark scheme
4. Upload student scripts
5. Download the generated reports!

**Note:** First deployment may take 3-5 minutes. Subsequent loads are instant (unless using free tier that "sleeps").
