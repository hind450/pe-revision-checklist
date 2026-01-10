# User Guide

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hind450/pe-revision-checklist.git
cd pe-revision-checklist
```

2. No additional dependencies required - uses Node.js built-in modules.

### Quick Start

Run the included example:
```bash
npm run example
```

This will assess a sample student script and display a detailed feedback report.

---

## Using the Command Line Interface

### Basic Usage

```bash
node src/cli.js --student <student-file> --markscheme <markscheme-file>
```

### Command Options

- `--student, -s`: Path to student script JSON file (required)
- `--markscheme, -m`: Path to mark scheme JSON file (required)
- `--examiner, -e`: Path to examiner comments JSON file (optional)
- `--output, -o`: Path to save output report (optional)
- `--json`: Output in JSON format instead of text
- `--help, -h`: Show help message

### Examples

**Assess a student script:**
```bash
node src/cli.js -s examples/student-script.json -m examples/mark-scheme.json
```

**Save report to file:**
```bash
node src/cli.js -s student.json -m scheme.json -o report.txt
```

**Include examiner comments:**
```bash
node src/cli.js -s student.json -m scheme.json -e comments.json
```

**Output as JSON:**
```bash
node src/cli.js -s student.json -m scheme.json --json -o report.json
```

---

## Using the JavaScript API

### Basic Example

```javascript
const PEAssessment = require('./src/index');

// Create assessment instance
const peAssessment = new PEAssessment();

// Load your data
const studentScript = {
  studentId: 'STUDENT001',
  answers: [
    {
      questionNumber: 1,
      text: 'Student answer here...'
    }
  ]
};

const markScheme = {
  maxMarks: 10,
  questions: [
    {
      questionNumber: 1,
      maxMarks: 10,
      assessmentObjective: 'AO1',
      markingPoints: [
        {
          description: 'Key concept',
          keywords: ['concept', 'term'],
          marks: 2
        }
      ]
    }
  ]
};

// Process assessment
const result = peAssessment.processAssessment(studentScript, markScheme);

// Display results
console.log(result.textReport);
```

### Accessing Different Result Formats

```javascript
const result = peAssessment.processAssessment(studentScript, markScheme);

// Text report (human-readable)
console.log(result.textReport);

// Raw assessment data
console.log(result.assessment.totalMarks);
console.log(result.assessment.percentage);
console.log(result.assessment.aoBreakdown);

// Structured feedback report
console.log(result.feedbackReport.summary);
console.log(result.feedbackReport.actionPlan);
```

---

## Creating Data Files

### Student Script

Create a JSON file with the student's answers:

```json
{
  "studentId": "STUDENT001",
  "examDate": "2026-01-10",
  "answers": [
    {
      "questionNumber": 1,
      "text": "The student's written answer goes here..."
    },
    {
      "questionNumber": 2,
      "text": "Answer to question 2..."
    }
  ]
}
```

### Mark Scheme

Create a JSON file with marking criteria:

```json
{
  "examTitle": "GCSE Physical Education - Paper 1",
  "maxMarks": 20,
  "questions": [
    {
      "questionNumber": 1,
      "questionText": "Describe aerobic respiration.",
      "maxMarks": 6,
      "assessmentObjective": "AO1",
      "markingPoints": [
        {
          "description": "Uses oxygen",
          "keywords": ["oxygen", "aerobic"],
          "marks": 1
        },
        {
          "description": "Produces ATP",
          "keywords": ["ATP", "energy"],
          "marks": 1
        }
      ]
    }
  ]
}
```

### Tips for Creating Mark Schemes

1. **Choose relevant keywords**: Select words that students are likely to use
2. **Be specific**: More specific keywords reduce false positives
3. **Include variations**: Add synonyms (e.g., "cardiovascular", "heart")
4. **Use lowercase**: All keywords are converted to lowercase for matching
5. **Award appropriate marks**: Typically 1 mark per key point

---

## Understanding Assessment Objectives

### AO1: Knowledge and Understanding
- Tests recall of facts, concepts, and terminology
- Looks for definitions and explanations
- Keywords: define, describe, state, identify

**Example Question**: "Describe the components of fitness."

### AO2: Application
- Tests ability to apply knowledge to scenarios
- Looks for practical examples and real-world application
- Keywords: apply, explain how, give an example

**Example Question**: "Explain how a warm-up prepares the body for exercise."

### AO3: Analysis and Evaluation
- Tests critical thinking and judgement
- Looks for comparisons, evaluation, and justified conclusions
- Keywords: evaluate, assess, compare, justify

**Example Question**: "Evaluate the effectiveness of different training methods."

---

## Interpreting Results

### Grade Boundaries

The system uses standard GCSE grade boundaries:
- **A* (90%+)**: Outstanding performance
- **A (80-89%)**: Excellent understanding
- **B (70-79%)**: Good grasp of content
- **C (60-69%)**: Satisfactory knowledge
- **D (50-59%)**: Basic understanding
- **E (40-49%)**: Limited knowledge
- **U (<40%)**: Unclassified

### Performance Levels

Each AO is assessed separately:
- **Strong (70%+)**: Continue current approach
- **Adequate (50-69%)**: Some improvement needed
- **Needs Development (<50%)**: Significant work required

### Using Feedback

1. **Review overall performance**: Check summary and grade
2. **Analyze AO breakdown**: Identify weak assessment objectives
3. **Read question feedback**: Understand what was missed
4. **Check learning gaps**: Focus on specific weaknesses
5. **Follow action plan**: Implement recommended improvements
6. **Use suggested resources**: Access appropriate materials

---

## Best Practices

### For Teachers

1. **Create detailed mark schemes**: More marking points = better accuracy
2. **Review results manually**: Automated marking is a tool, not replacement
3. **Use examiner comments**: Provide context and guidance
4. **Track progress over time**: Compare multiple assessments
5. **Customize feedback**: Add personal notes to generated reports

### For Students

1. **Read feedback carefully**: Understand what marks were lost
2. **Focus on weak AOs**: Prioritize areas needing improvement
3. **Use specific terminology**: Include key words in answers
4. **Practice regularly**: Use past papers with mark schemes
5. **Seek clarification**: Ask teachers about unclear feedback

---

## Troubleshooting

### Issue: Low marks despite good answer

**Possible causes:**
- Keywords not matching (use different terminology)
- Missing specific points from mark scheme
- Answer too vague or general

**Solutions:**
- Review mark scheme keywords
- Be more specific in answers
- Include technical terminology

### Issue: Incorrect assessment

**Possible causes:**
- Mark scheme keywords too broad
- Keyword matching false positives
- Complex answers not parsed correctly

**Solutions:**
- Refine mark scheme keywords
- Make keywords more specific
- Consider manual review for complex questions

---

## Advanced Usage

### Batch Processing

Process multiple students:

```javascript
const students = [student1, student2, student3];
const markScheme = loadMarkScheme();

students.forEach(student => {
  const result = peAssessment.processAssessment(student, markScheme);
  saveReport(student.studentId, result);
});
```

### Custom Reporting

Create custom reports:

```javascript
const result = peAssessment.processAssessment(studentScript, markScheme);

// Extract specific data
const aoPerformance = result.assessment.aoBreakdown;
const recommendations = result.feedbackReport.diagnostics.recommendations;

// Generate custom output
generateCustomReport(aoPerformance, recommendations);
```

### Integration

Integrate with existing systems:

```javascript
// Export to database
saveToDatabase(result.assessment);

// Send email notifications
sendEmailReport(studentEmail, result.textReport);

// Generate PDF
generatePDF(result.feedbackReport);
```
