# 🚀 Interactive Render.com Deployment Walkthrough

**Let's get your PE Assessment System live on the internet RIGHT NOW!**

I'll walk you through every single step as if I'm sitting next to you. Follow along and in 10 minutes you'll have a working website accessible from anywhere.

---

## 🎯 What We're Doing

**Goal:** Get a public URL like `https://pe-assessment-app.onrender.com` where you can upload mark schemes and student work

**Time:** 10-12 minutes total

**Cost:** FREE (the website sleeps after 15 minutes of no use, but wakes up when someone visits)

**What you need:**
- A GitHub account (you probably have one since you're reading this!)
- 10 minutes
- That's it!

---

## 📋 Quick Checklist Before We Start

Let me verify you have everything:

- [ ] You have a GitHub account
- [ ] You're logged into GitHub
- [ ] You can see this repository: `hind450/pe-revision-checklist`
- [ ] You have an email address for Render signup

**All checked?** Great! Let's begin! 🎉

---

## STEP 1: Create Your Render Account (3 minutes)

### 1.1 Open Render.com

**What to do:**
1. Open a new browser tab
2. Go to: **https://render.com**
3. You should see a clean homepage with "Build, deploy, and scale your apps" or similar

**What you're looking for:** A blue "Get Started" or "Sign Up" button in the top-right corner

---

### 1.2 Sign Up with GitHub

**What to do:**
1. Click the **"Get Started"** button (top-right)
2. You'll see signup options
3. Click **"Sign up with GitHub"** (it's the easiest way!)
4. A GitHub authorization page will appear

**Important:** Use "Sign up with GitHub" rather than email - it's one less password to remember and makes connecting your repo easier!

---

### 1.3 Authorize Render

**What you'll see:**
- GitHub will ask: "Authorize Render to access your account?"
- It will show what permissions Render wants

**What to do:**
1. Review the permissions (they're safe - Render is a trusted platform)
2. Click **"Authorize render"** (green button)
3. You may need to enter your GitHub password

**After clicking:** You'll be redirected back to Render

---

### 1.4 Complete Your Profile

**What might happen:**
- Render may ask for additional info (name, company, etc.)
- You might need to verify your email

**What to do:**
- Fill in any required fields
- Check your email for verification if prompted
- Click through any welcome screens

**✅ Success indicator:** You should now see your Render Dashboard with a "New +" button or "Create New" options

---

## STEP 2: Create a Web Service (2 minutes)

### 2.1 Start Creating a New Service

**What to do:**
1. Look for a big **"New +"** button (usually top-right of dashboard)
2. Click it
3. Select **"Web Service"** from the dropdown menu

**What you'll see:** A page asking "Where is your service's code?"

---

### 2.2 Connect Your GitHub Repository

**What to do:**

**If you see the repository listed:**
1. Look for: `hind450/pe-revision-checklist`
2. Click the **"Connect"** button next to it
3. Skip to Step 2.3

**If you DON'T see the repository:**
1. Click **"Configure account"** or "+ Connect account" 
2. You'll be taken to GitHub
3. Grant Render access to see your repositories
4. Look for "Repository access" section
5. Select "All repositories" OR select just `hind450/pe-revision-checklist`
6. Click **"Save"** or **"Install & Authorize"**
7. You'll be redirected back to Render
8. Now you should see the repository - click **"Connect"**

---

### 2.3 Name Your Service

**What you'll see:** A configuration page with lots of fields

**What to do:**

**Name field:**
- Enter a name for your service (this will be in your URL!)
- Good examples:
  - `pe-assessment-app`
  - `pe-marking-system`
  - `my-pe-assessment`
- Avoid spaces and special characters
- This will become: `https://YOUR-NAME-HERE.onrender.com`

**My suggestion:** Use `pe-assessment-app`

---

## STEP 3: Configure Your Service (3 minutes)

Now let's set up the exact configuration. **Copy and paste these values exactly as shown!**

### 3.1 Basic Settings

**Branch:**
- Click the dropdown next to "Branch"
- Select: `copilot/add-automated-marking-system-again`
- ⚠️ **IMPORTANT:** Must be this exact branch, not `main`!

**Root Directory:**
- Leave this **BLANK** (empty)
- Do NOT enter anything here

**Runtime:**
- Should automatically detect "Python"
- If not, select **"Python 3"** from the dropdown

---

### 3.2 Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**What to do:**
1. Find the "Build Command" field
2. Copy the command above
3. Paste it in (replace any default text)

**Why:** This installs all the Python libraries your app needs

---

### 3.3 Start Command

**Start Command:**
```bash
cd web && gunicorn --bind 0.0.0.0:$PORT app:app
```

**What to do:**
1. Find the "Start Command" field
2. Copy the command above exactly
3. Paste it in (replace any default text)

**Why:** This starts your web server when Render launches your app

---

### 3.4 Plan Selection

**What you'll see:** Different pricing plans

**What to do:**
1. Select **"Free"** plan
2. It says "Spins down after 15 minutes of inactivity"
3. That's okay! It wakes up automatically when someone visits (takes ~30 seconds)

**Note:** You can always upgrade later if you want it to stay awake 24/7

---

### 3.5 Environment Variables (OPTIONAL)

**Do I need to set these?** No, for basic functionality the defaults work fine!

**If you want to customize:**

Click **"Advanced"** button, then add these (one at a time):

| Key | Value | Why |
|-----|-------|-----|
| `PYTHON_VERSION` | `3.9.18` | Specifies Python version |
| `PORT` | (leave empty) | Render sets this automatically |

**My advice:** Skip this section for now - you can add these later if needed

---

### 3.6 Review Your Settings

**Before clicking "Create Web Service", verify:**

- [ ] Name: `pe-assessment-app` (or your chosen name)
- [ ] Branch: `copilot/add-automated-marking-system-again`
- [ ] Runtime: Python
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `cd web && gunicorn --bind 0.0.0.0:$PORT app:app`
- [ ] Plan: Free

**Everything correct?** Awesome! Click the big **"Create Web Service"** button at the bottom!

---

## STEP 4: Watch Your App Deploy (3-5 minutes)

### 4.1 Deployment Begins

**What you'll see:**
- You'll be taken to your service's page
- A section called "Logs" will show activity
- Text will scroll by showing the build progress

**What's happening:**
- Render is creating a server for you
- Installing Python and all libraries
- Setting up your application
- This takes 3-5 minutes - **be patient!**

---

### 4.2 Understanding the Logs

**You'll see messages like:**
```
==> Cloning from https://github.com/hind450/pe-revision-checklist...
==> Downloading cache...
==> Running build command: pip install -r requirements.txt...
==> Collecting flask...
==> Installing collected packages: flask, pandas, pdfplumber...
==> Successfully installed...
==> Build successful
==> Starting service...
```

**What to look for:**
- ✅ Green checkmarks or "Build successful" messages
- ✅ "Starting service..." message
- ✅ "Your service is live" message

**What to worry about:**
- ❌ Red "Error" messages
- ❌ "Build failed" messages
- See troubleshooting section below if you see these

---

### 4.3 Wait for "Live" Status

**At the top of the page**, you'll see a status indicator:

**Current status might say:**
- "Building" (🟡 yellow) - Wait...
- "Deploying" (🟡 yellow) - Almost there...
- "Live" (🟢 green) - **SUCCESS!**

**When you see "Live":**
- Your service is ready!
- Your URL is active!
- Time to test it!

---

## STEP 5: Access Your Live Website! (30 seconds)

### 5.1 Find Your URL

**What to do:**
1. Look at the top of your service page in Render
2. You'll see your URL: `https://pe-assessment-app.onrender.com` (or whatever name you chose)
3. Click the URL, or copy and paste it into a new browser tab

**First visit will be slow!**
- The first time you visit, it takes 20-30 seconds to wake up
- You'll see "Loading..." or a waiting message
- Be patient - this is normal for free tier!

---

### 5.2 You Should See Your Website! 🎉

**What you should see:**
- The PE Assessment System homepage
- Navigation menu with "Home", "Dashboard", etc.
- A clean, professional interface
- Upload buttons and instructions

**If you see this - CONGRATULATIONS! Your website is LIVE!** 🎊

---

### 5.3 Test the Dashboard

**Let's verify everything works:**

1. Click **"Dashboard"** in the navigation (or add `/dashboard` to your URL)
2. You should see:
   - "Teacher Dashboard" heading
   - "Class Management" section
   - Upload sections for mark schemes and student work
3. Try clicking **"Add New Class"**
4. Enter a test class name like "Test Class"
5. Click "Add Class"
6. The class should appear in your class list!

**If all of this works - your deployment is 100% successful!** ✅

---

## 🎊 SUCCESS! What Now?

### Your Website is Live!

**Your URL:** `https://[your-name].onrender.com`

**You can now:**
- ✅ Access it from any device with internet
- ✅ Share the URL with colleagues
- ✅ Upload mark schemes and student work
- ✅ Process assessments and download reports
- ✅ Use all dashboard features

---

### Share Your URL

**Send this to teachers/colleagues:**
```
PE Assessment System
https://[your-name].onrender.com

Use the Dashboard to:
1. Create classes
2. Upload mark schemes
3. Upload student scripts
4. View and download reports
```

---

### Important Notes About Free Tier

**Sleep Mode:**
- Your site sleeps after 15 minutes of inactivity
- First visit after sleep takes 20-30 seconds to wake up
- Subsequent visits are instant
- Data is NOT lost when sleeping

**To keep it awake 24/7:**
- Upgrade to paid plan ($7/month)
- Or use a service like UptimeRobot to ping it every 5 minutes (keeps it awake for free!)

---

### Using Your Live Website

**Workflow:**

1. **Create Classes:**
   - Go to Dashboard
   - Click "Add New Class"
   - Create classes for your groups (e.g., "Year 10 PE", "11A PE")

2. **Upload Mark Scheme:**
   - In Dashboard → Mark Scheme section
   - Select a class from dropdown
   - Upload PDF/DOCX file
   - Give it a name (e.g., "Energy Systems Test")

3. **Upload Student Work:**
   - In Dashboard → Student Work section
   - Select the SAME class
   - Upload multiple PDF files (one per student)
   - System processes them automatically

4. **View Results:**
   - Go to "Recent Results" table
   - Click "View Results" for your assessment
   - See all students with performance indicators
   - Download individual and class reports

---

## 🔧 Troubleshooting

### Problem: Build Failed

**Error message contains: "No module named 'flask'" or similar**

**Solution:**
1. Go back to your service settings (click "Settings" tab)
2. Verify Build Command is: `pip install -r requirements.txt`
3. Scroll down and click "Manual Deploy" → "Deploy latest commit"

---

### Problem: Service Won't Start

**Error message: "Failed to bind to $PORT"**

**Solution:**
1. Go to Settings tab
2. Check Start Command is: `cd web && gunicorn --bind 0.0.0.0:$PORT app:app`
3. Make sure there's NO custom `PORT` environment variable (Render sets it automatically)
4. Click "Manual Deploy" → "Deploy latest commit"

---

### Problem: "Application Error" When Visiting URL

**What it means:** The app started but crashed

**Solution:**
1. Go to your Render dashboard
2. Click on your service
3. Look at the "Logs" tab
4. Find the error message (usually at the bottom)
5. Common fixes:
   - Check branch is `copilot/add-automated-marking-system-again`
   - Verify all files are in the repository
   - Check requirements.txt exists in repo root

---

### Problem: Can't Find Repository

**Error: "Repository not found" or not in list**

**Solution:**
1. Click "Configure account" on the connect repository page
2. On GitHub authorization page:
   - Grant Render access to "All repositories" OR
   - Select `hind450/pe-revision-checklist` specifically
3. Click "Save" / "Install & Authorize"
4. Go back to Render and retry

---

### Problem: Website is Really Slow

**If it takes 20-30 seconds to load:**

**Explanation:** This is normal for free tier!
- The service "sleeps" after 15 minutes of no activity
- First visit after sleep takes time to "wake up"
- Subsequent visits are fast

**Solutions:**
- Wait patiently for first load (only happens after sleep)
- Upgrade to paid plan ($7/month) for always-on
- Use UptimeRobot to ping your URL every 5 minutes (keeps it awake)

---

### Problem: Uploads Not Working

**Files won't upload or processing fails:**

**Solutions:**
1. Check file format:
   - Mark schemes: Must be PDF or DOCX
   - Student scripts: Must be PDF
2. Check file size:
   - Free tier has limits (~10MB per file usually)
   - Split large files or compress PDFs
3. Check you selected a class in the dropdown
4. Make sure mark scheme uploaded before student work

---

## 📱 Next Steps

### Test With Sample Files

**Located in the repo:** `sample_test_files/`

1. Convert the `.txt` files to PDF (or modify app to accept TXT)
2. Upload `mark_scheme_sample.txt` (as PDF) to a test class
3. Upload the student samples to the same class
4. View the results!

**Expected:**
- Alice Thompson: High performance (Green, 85-90%)
- Bob Martinez: Low performance (Red, 30-40%)
- Emma Chen: Medium performance (Amber, 70-75%)

---

### Customize Your Instance

**Want to make changes?**

1. Make changes to code in GitHub (on your branch)
2. Go to Render dashboard
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait for rebuild (2-3 minutes)
5. Changes are live!

---

### Monitor Usage

**In Render Dashboard:**
- Click your service name
- View "Metrics" tab to see:
  - Request counts
  - Response times
  - Memory usage
  - CPU usage

---

### Get Support

**If you're stuck:**

1. **Check logs:**
   - Render dashboard → Your service → "Logs" tab
   - Copy error messages

2. **Render support:**
   - https://render.com/docs
   - Community forum: https://community.render.com

3. **This repository:**
   - Open an issue on GitHub
   - Include your error logs
   - Describe what you were doing when it failed

---

## 🎓 Summary

**What you accomplished:**
✅ Created a Render.com account
✅ Connected your GitHub repository
✅ Configured deployment settings
✅ Deployed a live web application
✅ Got a public URL for your PE Assessment System
✅ Tested the dashboard functionality

**Your URL:** `https://[your-service-name].onrender.com`

**You now have:**
- A fully functional PE assessment system
- Accessible from anywhere via web browser
- Automated marking with AI
- Class management and organization
- Report generation and download
- All without writing a single line of code!

---

## 🚀 You're Done!

**Your PE Assessment System is live on the internet!**

Go ahead and:
1. Create some classes
2. Upload mark schemes
3. Upload student work
4. Generate reports
5. Share your URL with colleagues!

**Welcome to having your own web application!** 🎉

If you followed this guide and got it working, give yourself a pat on the back - you just deployed a production web application to the cloud! 🌟

---

## 📞 Need Help?

If something didn't work:
1. Re-read the troubleshooting section
2. Check the logs in Render dashboard
3. Try "Manual Deploy" to rebuild
4. Open an issue on the GitHub repository with details

**Most common issue:** Wrong branch selected (must be `copilot/add-automated-marking-system-again`)

**Second most common:** Start command incorrect (must include `cd web &&`)

---

## 🎯 Quick Reference Card

**For future use - keep this handy:**

```
Repository: hind450/pe-revision-checklist
Branch: copilot/add-automated-marking-system-again
Build: pip install -r requirements.txt
Start: cd web && gunicorn --bind 0.0.0.0:$PORT app:app
Your URL: https://[your-service-name].onrender.com
Dashboard: https://[your-service-name].onrender.com/dashboard
```

**To redeploy after changes:**
1. Render dashboard → Your service
2. Manual Deploy → Deploy latest commit
3. Wait 2-3 minutes
4. Done!

---

**🎉 Congratulations - you now have a live, working PE Assessment System accessible from anywhere in the world! 🌍**
