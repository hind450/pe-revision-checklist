# PE Assessment for Learning

An automated marking and feedback system for Physical Education assessments that provides accurate, actionable insights for students and teachers.

## Overview

This system delivers granular diagnostic insights by Assessment Objective (AO1–Knowledge, AO2–Application, AO3–Evaluation), helping learners and teachers identify learning gaps and improve performance.

## Features

- **Automated Marking**: Processes student scripts against mark schemes with keyword-based assessment
- **Assessment Objectives Analysis**: Breaks down performance by AO1 (Knowledge), AO2 (Application), and AO3 (Evaluation)
- **Diagnostic Insights**: Identifies strengths, weaknesses, and learning gaps
- **Actionable Feedback**: Provides specific recommendations for improvement
- **Comprehensive Reports**: Generates detailed feedback reports in JSON and text formats

## Installation

```bash
# Clone the repository
git clone https://github.com/hind450/pe-revision-checklist.git
cd pe-revision-checklist

# Install dependencies (if any added in future)
npm install
```

## Usage

### Running the Example

```bash
npm start
```

This will run a demonstration with sample student answers, mark scheme, and examiner comments.

### Using in Your Code

```javascript
const PEAssessment = require('./src/index');

// Create assessment instance
const peAssessment = new PEAssessment();

// Prepare student script
const studentScript = {
  studentId: 'STUDENT001',
  answers: [
    {
      questionNumber: 1,
      text: 'Your student answer here...'
    }
    // ... more answers
  ]
};

// Prepare mark scheme
const markScheme = {
  maxMarks: 15,
  questions: [
    {
      questionNumber: 1,
      maxMarks: 6,
      assessmentObjective: 'AO1',
      markingPoints: [
        {
          description: 'Key point description',
          keywords: ['keyword1', 'keyword2'],
          marks: 1
        }
        // ... more marking points
      ]
    }
    // ... more questions
  ]
};

// Process assessment
const result = peAssessment.processAssessment(studentScript, markScheme);

// Access results
console.log(result.textReport); // Human-readable report
console.log(result.assessment); // Raw assessment data
console.log(result.feedbackReport); // Structured feedback
```

## Assessment Objectives

### AO1: Knowledge and Understanding (33%)
Demonstrate knowledge and understanding of physical education concepts, terminology, and principles.

### AO2: Application (33%)
Apply knowledge and understanding to practical scenarios and real-world examples.

### AO3: Analysis and Evaluation (34%)
Analyse and evaluate physical education concepts, making judgements supported by evidence.

## Data Format

### Student Script Format
```json
{
  "studentId": "STUDENT001",
  "answers": [
    {
      "questionNumber": 1,
      "text": "Student's answer text..."
    }
  ]
}
```

### Mark Scheme Format
```json
{
  "maxMarks": 15,
  "questions": [
    {
      "questionNumber": 1,
      "maxMarks": 6,
      "assessmentObjective": "AO1",
      "markingPoints": [
        {
          "description": "Description of marking point",
          "keywords": ["keyword1", "keyword2"],
          "marks": 1
        }
      ]
    }
  ]
}
```

## Examples

See the `/examples` directory for:
- `student-script.json` - Sample student answers
- `mark-scheme.json` - Sample marking criteria
- `examiner-comments.json` - Sample examiner feedback

## Output

The system generates comprehensive feedback including:

- **Summary**: Overall score, grade, and performance level
- **Question Feedback**: Marks and feedback for each question
- **AO Analysis**: Performance breakdown by assessment objective
- **Diagnostics**: Strengths, weaknesses, and learning gaps
- **Action Plan**: Short-term and long-term improvement recommendations
- **Resources**: Suggested materials for revision

## Architecture

The system consists of three main components:

1. **AssessmentEngine** (`src/assessmentEngine.js`): Core marking logic
2. **FeedbackGenerator** (`src/feedbackGenerator.js`): Report generation
3. **PEAssessment** (`src/index.js`): Main interface

## Grading Scale

| Percentage | Grade |
|------------|-------|
| 90%+       | A*    |
| 80-89%     | A     |
| 70-79%     | B     |
| 60-69%     | C     |
| 50-59%     | D     |
| 40-49%     | E     |
| <40%       | U     |

## Future Enhancements

- Web interface for easy upload and viewing
- Support for image-based answer scripts (OCR)
- Advanced NLP for better answer analysis
- Integration with learning management systems
- Historical performance tracking
- Custom mark scheme builder

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
