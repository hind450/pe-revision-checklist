# 📖 Complete Step-by-Step Deployment Guide - Render.com

**Goal:** Get your PE Assessment System running on a public URL in 10 minutes

**What you'll get:** A URL like `https://pe-assessment-app.onrender.com` accessible from anywhere

**Cost:** FREE (with some limitations - sleeps after 15 minutes of inactivity)

---

## Prerequisites

- A GitHub account (create free at https://github.com)
- An email address for Render.com signup
- 10 minutes of time

---

## Step 1: Sign Up for Render.com

### 1.1 Go to Render.com
- Open your web browser
- Navigate to: **https://render.com**
- You should see the Render homepage

### 1.2 Click "Get Started"
- Look for the "Get Started" or "Sign Up" button (usually top-right corner)
- Click it

### 1.3 Sign Up with GitHub (Recommended)
- Choose "Sign up with GitHub" option
- This is easier than email signup and allows direct repo access
- Click the GitHub button

### 1.4 Authorize Render
- GitHub will ask you to authorize Render
- Click "Authorize Render" button
- You may need to enter your GitHub password

### 1.5 Complete Profile
- Fill in any additional profile information Render requests
- Verify your email if prompted
- You're now logged into Render!

**✅ Checkpoint:** You should now see your Render dashboard

---

## Step 2: Fork or Access the Repository

### 2.1 Ensure You Have Access
Since the repository is at `hind450/pe-revision-checklist`, you need to either:

**Option A: If it's your repository**
- You already have access, proceed to Step 3

**Option B: If it's someone else's repository**
- Go to: https://github.com/hind450/pe-revision-checklist
- Click "Fork" button (top-right)
- This creates your own copy
- Wait for fork to complete
- Your fork will be at: `https://github.com/YOUR_USERNAME/pe-revision-checklist`

**✅ Checkpoint:** Repository is accessible in your GitHub account

---

## Step 3: Create New Web Service on Render

### 3.1 Access Dashboard
- From Render.com, you should be on your dashboard
- If not, click "Dashboard" in the top navigation

### 3.2 Click "New +"
- Look for a "New +" or "New" button (usually top-right)
- Click it
- A dropdown menu appears

### 3.3 Select "Web Service"
- From the dropdown, click "Web Service"
- You'll be taken to the repository connection page

**✅ Checkpoint:** You should see "Create a new Web Service" page

---

## Step 4: Connect Your GitHub Repository

### 4.1 Connect GitHub Account (if not already connected)
- If you see "Connect GitHub", click it
- Authorize Render to access your repositories
- Click "Authorize Render" on GitHub

### 4.2 Find the Repository
- You'll see a list of your repositories
- Look for `pe-revision-checklist` (or `YOUR_USERNAME/pe-revision-checklist` if you forked)
- If you don't see it:
  - Click "Configure account" or "Install Render"
  - Select which repositories Render can access
  - Choose "All repositories" or select `pe-revision-checklist` specifically
  - Click "Install" or "Save"

### 4.3 Click "Connect" on the Repository
- Find `pe-revision-checklist` in the list
- Click the "Connect" button next to it
- You'll be taken to the configuration page

**✅ Checkpoint:** You should now see the "You are deploying..." configuration form

---

## Step 5: Configure Your Web Service

### 5.1 Fill in Basic Information

**Name:**
```
pe-assessment-app
```
(or choose your own name - this will be part of your URL)

**Region:**
- Select the region closest to you
- Options include: Oregon (US West), Ohio (US East), Frankfurt (EU), Singapore (Asia)
- Choose whichever is geographically closest

**Branch:**
```
copilot/add-automated-marking-system-again
```
- Type this exactly or select from dropdown if it appears
- This is the branch with all the web interface code

**Root Directory:**
- Leave this EMPTY (blank)
- Don't type anything here

**Runtime:**
- Should auto-detect as "Python 3"
- If not, select "Python 3" from dropdown

### 5.2 Configure Build & Start Commands

**Build Command:**
```
pip install -r requirements.txt
```
- Type this exactly
- This installs all necessary Python packages

**Start Command:**
```
cd web && gunicorn app:app
```
- Type this exactly
- This starts your web application

### 5.3 Advanced Settings (Optional but Recommended)

- Click "Advanced" button (below Start Command)
- This expands additional options

**Add Environment Variable:**
- Click "Add Environment Variable"
- Key: `PYTHON_VERSION`
- Value: `3.9.18`

**Auto-Deploy:**
- Make sure "Auto-Deploy" is set to "Yes"
- This automatically updates your app when you push to GitHub

### 5.4 Select Plan

**Choose Free Plan:**
- Scroll down to "Instance Type"
- Select "Free" (should be selected by default)
- Free tier limitations:
  - 512 MB RAM
  - Sleeps after 15 minutes of inactivity
  - First request after sleep takes ~30 seconds

**✅ Checkpoint:** All fields should be filled in correctly

---

## Step 6: Deploy!

### 6.1 Create Web Service
- Scroll to the bottom
- Click the blue "Create Web Service" button
- Don't close the browser - deployment will start immediately

### 6.2 Watch the Build Process
- You'll see a console/terminal output appear
- This shows real-time deployment progress
- You'll see messages like:
  ```
  ==> Cloning from https://github.com/...
  ==> Downloading cache...
  ==> Running build command: pip install -r requirements.txt
  ==> Installing dependencies...
  ==> Build complete!
  ==> Starting service with command: cd web && gunicorn app:app
  ```

### 6.3 Wait for Deployment
- Total time: 3-5 minutes (first deployment)
- Green "Live" indicator appears when ready
- You'll see: "Your service is live 🎉"

**✅ Checkpoint:** Status shows "Live" with green indicator

---

## Step 7: Access Your Website!

### 7.1 Find Your URL
- At the top of the page, you'll see your service URL
- Format: `https://pe-assessment-app.onrender.com`
- (The exact URL depends on the name you chose)

### 7.2 Click the URL
- Click on your service URL
- It opens in a new tab
- You should see the PE Assessment homepage!

### 7.3 Test the Website
- You should see: "🎓 PE Assessment for Learning"
- Try clicking "Upload Mark Scheme"
- The interface should load properly

**✅ Checkpoint:** Website loads successfully in your browser!

---

## Step 8: Using Your New Website

### 8.1 Upload a Mark Scheme
1. On your website, click "Upload Mark Scheme"
2. Click "Choose File"
3. Select a PDF or DOCX mark scheme from your computer
4. Click "Upload Mark Scheme" button
5. Wait for "Mark scheme loaded successfully" message

### 8.2 Upload Student Scripts
1. After mark scheme loads, you're redirected to student upload
2. Click "Choose Files"
3. Select one or more student script PDFs
4. Hold Ctrl (Windows) or Cmd (Mac) to select multiple files
5. Click "Process Student Scripts"
6. Wait for processing (about 10-30 seconds per student)

### 8.3 Download Reports
1. After processing completes, you'll see the results page
2. Click on any report file to download it
3. Reports include:
   - Individual student reports (TXT and CSV)
   - Class analytics (TXT and CSV)
   - Student summary CSV

**🎉 Success!** You now have a fully functional PE Assessment website!

---

## Troubleshooting

### Problem: "Build failed" error

**Solution:**
1. Check that branch name is correct: `copilot/add-automated-marking-system-again`
2. Verify Build Command: `pip install -r requirements.txt`
3. Verify Start Command: `cd web && gunicorn app:app`
4. Check the build logs for specific error messages
5. Click "Manual Deploy" → "Clear build cache & deploy"

### Problem: Website shows "Service Unavailable"

**Solution:**
1. Wait 30-60 seconds (server might be starting)
2. Check Render dashboard - status should be "Live"
3. If status is "Build failed" or "Deploy failed", check logs
4. Try clicking "Manual Deploy" → "Deploy latest commit"

### Problem: Website loads but upload doesn't work

**Solution:**
1. Check browser console for errors (F12 → Console tab)
2. Verify file is PDF or DOCX format
3. Check file size (should be under 10MB)
4. Try with a smaller file first
5. Check Render logs for error messages

### Problem: "This service is sleeping"

**Solution:**
- This is normal on free tier
- First request wakes it up (takes ~30 seconds)
- Subsequent requests are fast
- Service sleeps after 15 minutes of no activity

### Problem: Can't find the repository in Render

**Solution:**
1. Go to GitHub.com
2. Fork the repository if you haven't already
3. Go back to Render
4. Click "Configure account" on the repository connection page
5. Select "All repositories" or specifically select your fork
6. Click "Install" to give Render access

---

## Next Steps

### Share Your Website
- Copy your URL: `https://pe-assessment-app.onrender.com`
- Share it with colleagues, students, or administrators
- Anyone can access it from anywhere!

### Customize Settings
- Go to Render dashboard
- Click on your service
- Click "Environment" tab to add more variables
- Click "Settings" to change name or other options

### Monitor Usage
- Check the "Logs" tab to see activity
- View "Metrics" to see request volume
- Monitor for any errors or issues

### Upgrade (Optional)
- Free tier works great for testing
- Paid tiers ($7/month+) offer:
  - Always-on (no sleeping)
  - More RAM and CPU
  - Custom domains
  - Faster builds

---

## Important Notes

### Free Tier Limitations
- ✅ Perfect for: Testing, demos, educational use
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep takes ~30 seconds
- ⚠️ 512 MB RAM (sufficient for this app)

### Data Storage
- Uploaded files are stored temporarily on the server
- Files are lost when service restarts or redeploys
- For production use, consider implementing permanent storage

### Security
- Current setup is fine for testing
- For production:
  - Change the secret key in `web/app.py`
  - Add user authentication
  - Implement file cleanup
  - Use HTTPS (Render does this automatically)

---

## Support & Resources

### Getting Help
- **Render Documentation:** https://render.com/docs
- **Render Community:** https://community.render.com
- **GitHub Issues:** Open an issue in the repository
- **Render Support:** support@render.com (for account issues)

### Additional Guides
- `DEPLOY_TO_CLOUD.md` - Other platform options
- `QUICK_DEPLOY.md` - Quick reference guide
- `WEB_ACCESS_GUIDE.md` - General web interface guide
- `web/README.md` - Web interface documentation

---

## Summary Checklist

Use this to verify you completed everything:

- [ ] Created Render.com account
- [ ] Connected GitHub account
- [ ] Selected pe-revision-checklist repository
- [ ] Configured service settings:
  - [ ] Name: pe-assessment-app
  - [ ] Branch: copilot/add-automated-marking-system-again
  - [ ] Build Command: pip install -r requirements.txt
  - [ ] Start Command: cd web && gunicorn app:app
- [ ] Selected Free plan
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment to complete
- [ ] Accessed website URL
- [ ] Tested mark scheme upload
- [ ] Tested student script upload
- [ ] Downloaded sample reports

**✅ All done?** Congratulations! You now have a fully deployed PE Assessment System!

---

## Quick Command Reference

For future deployments or updates:

**Redeploy from Render Dashboard:**
1. Go to https://dashboard.render.com
2. Click on your service
3. Click "Manual Deploy" → "Deploy latest commit"

**Update the Code:**
1. Make changes to the GitHub repository
2. Push to the `copilot/add-automated-marking-system-again` branch
3. Render automatically redeploys (if Auto-Deploy is on)

**View Logs:**
1. Dashboard → Your Service → "Logs" tab
2. See real-time logs of all activity

**Change Settings:**
1. Dashboard → Your Service → "Settings" tab
2. Modify any configuration
3. Click "Save Changes"

---

**Need Help?** If you get stuck at any step, check the Troubleshooting section above or refer to the additional documentation files.

**Success?** Share your URL and start testing the PE Assessment System with real mark schemes and student scripts!
