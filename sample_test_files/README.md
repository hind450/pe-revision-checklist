# Sample Test Files for PE Assessment System

This directory contains sample files you can use to test the PE Assessment System without creating your own.

## Files Included

### Mark Scheme
- `mark_scheme_sample.txt` - Complete mark scheme with 5 questions covering Energy Systems and SMART targets

### Student Scripts
- `student_alice_thompson.txt` - High-performing student (expected score: ~85-90%)
- `student_bob_martinez.txt` - Low-performing student with misconceptions (expected score: ~30-40%)
- `student_emma_chen.txt` - Mid-performing student (expected score: ~70-75%)

## How to Use These Files

### Option 1: Convert to PDF (Recommended)

The web application expects PDF files for student scripts. You can convert these TXT files to PDF using:

**Online Tools:**
- https://www.ilovepdf.com/txt_to_pdf
- https://www.pdf2go.com/txt-to-pdf
- Google Docs (Open .txt → Download as PDF)

**Command Line (Linux/Mac):**
```bash
# Install pandoc if needed
sudo apt-get install pandoc  # Ubuntu/Debian
brew install pandoc  # Mac

# Convert files
pandoc mark_scheme_sample.txt -o mark_scheme_sample.pdf
pandoc student_alice_thompson.txt -o student_alice_thompson.pdf
pandoc student_bob_martinez.txt -o student_bob_martinez.pdf
pandoc student_emma_chen.txt -o student_emma_chen.pdf
```

**Using Python:**
```bash
pip install reportlab

python << 'EOF'
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def txt_to_pdf(txt_file, pdf_file):
    with open(txt_file, 'r') as f:
        content = f.read()
    
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    for line in content.split('\n'):
        if line.strip():
            p = Paragraph(line, styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)

# Convert all files
txt_to_pdf('mark_scheme_sample.txt', 'mark_scheme_sample.pdf')
txt_to_pdf('student_alice_thompson.txt', 'student_alice_thompson.pdf')
txt_to_pdf('student_bob_martinez.txt', 'student_bob_martinez.pdf')
txt_to_pdf('student_emma_chen.txt', 'student_emma_chen.pdf')
EOF
```

### Option 2: Use as Templates

Copy and paste the content into:
- Microsoft Word → Save as PDF
- Google Docs → Download as PDF
- LibreOffice Writer → Export as PDF

### Option 3: Test with TXT Files (Requires Code Modification)

To allow TXT files in the system, update `web/app.py`:

```python
# Change line ~40 from:
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# To:
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
```

Then restart the web application.

## Testing Workflow

1. **Start the Web Application:**
   ```bash
   cd web
   python app.py
   ```

2. **Access Dashboard:**
   - Go to http://localhost:5000/dashboard

3. **Create a Test Class:**
   - Click "Add New Class"
   - Enter: "Test Class - Year 10"
   - Click "Add Class"

4. **Upload Mark Scheme:**
   - Select class: "Test Class - Year 10"
   - Upload: `mark_scheme_sample.pdf` (or .txt if modified)
   - Assessment name: "Energy Systems Test"
   - Click "Upload Mark Scheme"

5. **Upload Student Work:**
   - Select class: "Test Class - Year 10"
   - Upload all 3 student files (Alice, Bob, Emma)
   - Click "Process Student Work"

6. **View Results:**
   - Check individual student scores
   - Download reports
   - View class analytics

## Expected Results

**Alice Thompson (High Performance):**
- Total Score: ~17-18/20 (85-90%)
- Performance: GREEN
- Strong understanding of all concepts
- Good use of technical terminology
- Clear SMART target example

**Bob Martinez (Low Performance):**
- Total Score: ~6-8/20 (30-40%)
- Performance: RED
- Significant misconceptions
- Lacks technical terminology
- Vague SMART target
- Next Steps: Review all topics, focus on definitions

**Emma Chen (Medium Performance):**
- Total Score: ~14-15/20 (70-75%)
- Performance: AMBER
- Good understanding, minor gaps
- Mostly correct terminology
- Room for improvement in evaluation questions

**Class Analytics:**
- Average: ~60-65%
- Common Misconceptions: Students confusing aerobic/anaerobic details
- Teaching Recommendation: Reteach SMART targets with more specific examples
- Topic needing attention: Goal Setting (Bob's weak area)

## Customizing Test Files

Feel free to modify these files to test different scenarios:

- **Add more students** - Copy and modify student files
- **Change difficulty** - Adjust mark scheme complexity
- **Test misconceptions** - Add common errors in student answers
- **Different topics** - Create mark schemes for other PE topics

## Real-World Testing

For authentic testing, create or scan:
- Actual GCSE PE mark schemes (available from exam boards)
- Real student answer scripts
- Handwritten work (as PDFs via scanning)

## Need Help?

See `TESTING_GUIDE.md` in the parent directory for more testing options and guidance.
