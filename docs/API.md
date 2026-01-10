# API Documentation

## PEAssessment Class

Main interface for the PE Assessment system.

### Constructor

```javascript
const peAssessment = new PEAssessment();
```

Creates a new instance of the PE Assessment system.

### Methods

#### processAssessment(studentScript, markScheme, examinerComments)

Process a complete assessment with student answers and mark scheme.

**Parameters:**
- `studentScript` (Object): Student's answers
  - `studentId` (string): Unique student identifier
  - `answers` (Array): Array of answer objects
    - `questionNumber` (number): Question number
    - `text` (string): Student's answer text
- `markScheme` (Object): Marking criteria
  - `maxMarks` (number): Total marks available
  - `questions` (Array): Array of question objects
    - `questionNumber` (number): Question number
    - `maxMarks` (number): Maximum marks for this question
    - `assessmentObjective` (string): AO1, AO2, or AO3
    - `markingPoints` (Array): Array of marking point objects
      - `description` (string): Description of the point
      - `keywords` (Array<string>): Keywords to look for
      - `marks` (number): Marks awarded for this point
- `examinerComments` (Object, optional): Reference examiner comments

**Returns:** Object containing:
- `assessment` (Object): Raw assessment data with marks and breakdown
- `feedbackReport` (Object): Structured feedback report
- `textReport` (string): Human-readable text report

**Example:**
```javascript
const result = peAssessment.processAssessment(studentScript, markScheme);
console.log(result.textReport);
```

#### getAssessmentObjectives()

Get information about assessment objectives.

**Returns:** Object with AO1, AO2, AO3 definitions

**Example:**
```javascript
const aos = peAssessment.getAssessmentObjectives();
console.log(aos.AO1.description);
```

---

## AssessmentEngine Class

Core marking engine (used internally by PEAssessment).

### Constructor

```javascript
const engine = new AssessmentEngine();
```

### Methods

#### assessScript(studentScript, markScheme, examinerComments)

Assess a student script against a mark scheme.

**Returns:** Assessment result object with:
- `studentId` (string): Student identifier
- `totalMarks` (number): Total marks achieved
- `maxMarks` (number): Maximum possible marks
- `percentage` (number): Score percentage
- `aoBreakdown` (Object): Marks breakdown by AO1, AO2, AO3
- `feedback` (Array): Question-by-question feedback
- `diagnostics` (Object): Diagnostic insights
- `timestamp` (string): ISO timestamp

#### assessQuestion(studentAnswer, question, examinerComments)

Assess a single question.

**Returns:** Question result object with:
- `marks` (number): Marks awarded
- `feedback` (Array): Feedback messages

#### generateDiagnostics(assessment)

Generate diagnostic insights from assessment results.

**Returns:** Diagnostics object with:
- `strengths` (Array): Areas of strong performance
- `weaknesses` (Array): Areas needing improvement
- `learningGaps` (Array): Identified learning gaps
- `recommendations` (Array): Improvement recommendations
- `overallMessage` (string): Overall performance summary

---

## FeedbackGenerator Class

Generates detailed feedback reports (used internally by PEAssessment).

### Constructor

```javascript
const generator = new FeedbackGenerator();
```

### Methods

#### generateReport(assessment)

Generate comprehensive feedback report from assessment results.

**Returns:** Report object with:
- `summary` (Object): Overall summary with grade and performance level
- `questionFeedback` (Array): Question-by-question feedback
- `aoAnalysis` (Array): Analysis by assessment objective
- `diagnostics` (Object): Diagnostic insights
- `actionPlan` (Object): Improvement action plan
- `timestamp` (string): Report timestamp

#### formatAsText(report)

Format a report as human-readable text.

**Returns:** String containing formatted text report

**Example:**
```javascript
const textReport = generator.formatAsText(report);
console.log(textReport);
```

#### calculateGrade(percentage)

Calculate grade from percentage score.

**Returns:** Grade string (A*, A, B, C, D, E, U)

---

## Data Structures

### Student Script Format

```json
{
  "studentId": "STUDENT001",
  "examDate": "2026-01-10",
  "answers": [
    {
      "questionNumber": 1,
      "text": "Answer text..."
    }
  ]
}
```

### Mark Scheme Format

```json
{
  "examTitle": "GCSE Physical Education - Paper 1",
  "maxMarks": 15,
  "questions": [
    {
      "questionNumber": 1,
      "questionText": "Question text...",
      "maxMarks": 6,
      "assessmentObjective": "AO1",
      "markingPoints": [
        {
          "description": "Point description",
          "keywords": ["keyword1", "keyword2"],
          "marks": 1
        }
      ]
    }
  ]
}
```

### Assessment Result Format

```json
{
  "studentId": "STUDENT001",
  "totalMarks": 10,
  "maxMarks": 15,
  "percentage": 67,
  "aoBreakdown": {
    "AO1": {
      "marks": 4,
      "maxMarks": 6,
      "percentage": 67
    },
    "AO2": {
      "marks": 3,
      "maxMarks": 4,
      "percentage": 75
    },
    "AO3": {
      "marks": 3,
      "maxMarks": 5,
      "percentage": 60
    }
  },
  "feedback": [...],
  "diagnostics": {...},
  "timestamp": "2026-01-10T10:00:00.000Z"
}
```

### Feedback Report Format

```json
{
  "summary": {
    "studentId": "STUDENT001",
    "totalMarks": 10,
    "maxMarks": 15,
    "percentage": 67,
    "grade": "B",
    "performanceLevel": "Satisfactory"
  },
  "questionFeedback": [...],
  "aoAnalysis": [...],
  "diagnostics": {...},
  "actionPlan": {
    "priorityAreas": [...],
    "shortTerm": [...],
    "longTerm": [...],
    "resources": [...]
  },
  "timestamp": "2026-01-10T10:00:00.000Z"
}
```

---

## Constants

### Assessment Objectives

- **AO1**: Knowledge and Understanding (33% weight)
- **AO2**: Application (33% weight)
- **AO3**: Analysis and Evaluation (34% weight)

### Grade Boundaries

| Percentage | Grade |
|------------|-------|
| 90%+       | A*    |
| 80-89%     | A     |
| 70-79%     | B     |
| 60-69%     | C     |
| 50-59%     | D     |
| 40-49%     | E     |
| <40%       | U     |

### Performance Levels

- **Excellent**: 80%+
- **Good**: 70-79%
- **Satisfactory**: 60-69%
- **Pass**: 50-59%
- **Needs Improvement**: <50%

### AO Status Levels

- **Strong**: 70%+
- **Adequate**: 50-69%
- **Needs Development**: <50%
