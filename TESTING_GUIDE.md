# Testing Guide for PE Assessment System

## How to Test the System

Since file attachments cannot be directly uploaded here, you have several options:

### Option 1: Create Sample Files Locally

**1. Create a Sample Mark Scheme (PDF or DOCX)**

Create a document with this content:

```
GCSE PE Paper 1 - Mark Scheme

Question 1: Describe the aerobic energy system (3 marks)
Assessment Objective: AO1 - Knowledge
Keywords: oxygen, energy, aerobic, ATP
Acceptable Answer: The aerobic system uses oxygen to break down glucose to produce ATP (energy). It occurs in the mitochondria and produces energy for long-duration, low-intensity activities.

Question 2: Explain how the aerobic system is used during a marathon (4 marks)
Assessment Objective: AO2 - Application
Keywords: marathon, endurance, oxygen, sustained
Acceptable Answer: During a marathon, the aerobic system provides sustained energy because the activity is long-duration and low-intensity. The runner breathes in oxygen which is used to break down glucose and fats to produce ATP continuously over the race duration.

Question 3: Evaluate the effectiveness of the aerobic system for different types of athletes (6 marks)
Assessment Objective: AO3 - Evaluation
Keywords: evaluate, compare, advantages, disadvantages
Acceptable Answer: The aerobic system is highly effective for endurance athletes like marathon runners because it provides sustained energy without producing lactic acid. However, it is less effective for sprinters who need quick bursts of energy. The system takes time to activate and produces energy slowly compared to anaerobic systems.
```

Save as: `markscheme_sample.pdf` or `markscheme_sample.docx`

**2. Create Sample Student Scripts (PDFs)**

Create 2-3 documents with student answers:

**Student 1 - Alice (Good Performance):**
```
Name: Alice Smith

Question 1: The aerobic system uses oxygen to make energy called ATP. It happens in the mitochondria of cells and is used for activities that last a long time like jogging.

Question 2: In a marathon, the aerobic system is the main energy source because marathons last over 2 hours. The runner needs to maintain a steady pace so they breathe oxygen which is used to break down glycogen for energy throughout the race.

Question 3: The aerobic system is excellent for endurance athletes because it can provide energy for hours without fatigue. Marathon runners rely on it completely. However, sprinters can't use it effectively because it's too slow - they need the ATP-PC or anaerobic systems for quick power. The aerobic system's advantage is no lactic acid buildup, but the disadvantage is the slower energy production rate.
```

**Student 2 - Bob (Needs Improvement):**
```
Name: Bob Johnson

Question 1: The aerobic system makes energy. It uses air.

Question 2: Marathons use the aerobic system because they are long races and you need energy.

Question 3: The aerobic system is good for some athletes and not good for others. It depends on the sport they do.
```

Save as: `student_alice.pdf` and `student_bob.pdf`

### Option 2: Test with the Sample Files

**Step-by-Step Testing:**

1. **Start the Web Application**
   ```bash
   cd web
   python app.py
   ```
   Access at: http://localhost:5000

2. **Go to Dashboard**
   - Click "Dashboard" in navigation or go to http://localhost:5000/dashboard

3. **Create a Class**
   - Click "Add New Class"
   - Enter: "Year 10 PE Test"
   - Click "Add Class"

4. **Upload Mark Scheme**
   - In the "Upload Mark Scheme" section:
     - Select class: "Year 10 PE Test"
     - Choose your mark scheme file
     - Assessment name: "Paper 1 - Energy Systems"
     - Click "Upload Mark Scheme"

5. **Upload Student Work**
   - In the "Upload Student Work" section:
     - Select class: "Year 10 PE Test" (should have ✓)
     - Select your student script files (both Alice and Bob)
     - Click "Process Student Work"

6. **View Results**
   - You'll be redirected to the results page
   - See individual student scores
   - Download reports (TXT and CSV)
   - View class analytics

### Option 3: Use Example Data

I can create example test files in the repository:

**Would you like me to:**
1. Create sample mark scheme and student script files in the repository?
2. Create a testing script that generates dummy data?
3. Add a "Demo Mode" that uses pre-populated test data?

### Option 4: Deploy and Test Online

Follow the deployment guide to get a public URL:
1. Deploy to Render.com (see `STEP_BY_STEP_RENDER_DEPLOY.md`)
2. Access your URL (e.g., https://your-app.onrender.com)
3. Upload real or sample files through the web interface

## What Files to Test With

**Mark Scheme Requirements:**
- Format: PDF or DOCX
- Should contain:
  - Question numbers
  - Mark allocations
  - Keywords for each question
  - Acceptable answers
  - Assessment objectives (optional)

**Student Scripts Requirements:**
- Format: PDF
- Should contain:
  - Student name (can be in filename)
  - Answers to questions matching the mark scheme
  - Can be handwritten (if clear) or typed

## Expected Outputs

After processing, you'll get:
- Individual student reports (TXT and CSV)
- Class analytics report
- Traffic light indicators (Green/Amber/Red) by topic
- Identified misconceptions
- Teaching recommendations
- Performance breakdown by Assessment Objective

## Need Help?

Let me know which option you'd prefer:
- Option A: I create sample test files in the repository
- Option B: I add demo mode with pre-populated data  
- Option C: I create a data generator script
- Option D: You'll create your own files following the templates above

What would work best for you?
