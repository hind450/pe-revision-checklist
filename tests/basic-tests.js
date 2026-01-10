const PEAssessment = require('../src/index');
const assert = require('assert');

console.log('Running tests...\n');

// Test 1: Basic assessment
console.log('Test 1: Basic assessment processing');
const peAssessment = new PEAssessment();

const studentScript1 = {
  studentId: 'TEST001',
  answers: [
    {
      questionNumber: 1,
      text: 'Aerobic means with oxygen'
    }
  ]
};

const markScheme1 = {
  maxMarks: 3,
  questions: [
    {
      questionNumber: 1,
      maxMarks: 3,
      assessmentObjective: 'AO1',
      markingPoints: [
        {
          description: 'Aerobic definition',
          keywords: ['aerobic', 'oxygen'],
          marks: 1
        }
      ]
    }
  ]
};

const result1 = peAssessment.processAssessment(studentScript1, markScheme1);
assert(result1.assessment.totalMarks === 1, 'Should award 1 mark');
assert(result1.assessment.percentage === 33, 'Should calculate 33%');
console.log('✓ Basic assessment works\n');

// Test 2: Multiple questions
console.log('Test 2: Multiple questions with different AOs');
const studentScript2 = {
  studentId: 'TEST002',
  answers: [
    {
      questionNumber: 1,
      text: 'ATP is energy'
    },
    {
      questionNumber: 2,
      text: 'Training improves performance'
    }
  ]
};

const markScheme2 = {
  maxMarks: 4,
  questions: [
    {
      questionNumber: 1,
      maxMarks: 2,
      assessmentObjective: 'AO1',
      markingPoints: [
        { description: 'ATP', keywords: ['ATP', 'energy'], marks: 1 }
      ]
    },
    {
      questionNumber: 2,
      maxMarks: 2,
      assessmentObjective: 'AO2',
      markingPoints: [
        { description: 'Training', keywords: ['training', 'improve'], marks: 1 }
      ]
    }
  ]
};

const result2 = peAssessment.processAssessment(studentScript2, markScheme2);
assert(result2.assessment.totalMarks === 2, 'Should award 2 marks total');
assert(result2.assessment.aoBreakdown.AO1.marks === 1, 'Should award 1 mark for AO1');
assert(result2.assessment.aoBreakdown.AO2.marks === 1, 'Should award 1 mark for AO2');
console.log('✓ Multiple questions work correctly\n');

// Test 3: Empty answer
console.log('Test 3: Empty answer handling');
const studentScript3 = {
  studentId: 'TEST003',
  answers: [
    {
      questionNumber: 1,
      text: ''
    }
  ]
};

const result3 = peAssessment.processAssessment(studentScript3, markScheme1);
assert(result3.assessment.totalMarks === 0, 'Should award 0 marks for empty answer');
console.log('✓ Empty answers handled correctly\n');

// Test 4: Grade calculation
console.log('Test 4: Grade calculation');
const FeedbackGenerator = require('../src/feedbackGenerator');
const generator = new FeedbackGenerator();

assert(generator.calculateGrade(95) === 'A*', 'Should calculate A* for 95%');
assert(generator.calculateGrade(85) === 'A', 'Should calculate A for 85%');
assert(generator.calculateGrade(75) === 'B', 'Should calculate B for 75%');
assert(generator.calculateGrade(65) === 'C', 'Should calculate C for 65%');
assert(generator.calculateGrade(55) === 'D', 'Should calculate D for 55%');
assert(generator.calculateGrade(45) === 'E', 'Should calculate E for 45%');
assert(generator.calculateGrade(35) === 'U', 'Should calculate U for 35%');
console.log('✓ Grade calculation works correctly\n');

// Test 5: Assessment objectives info
console.log('Test 5: Assessment objectives retrieval');
const aos = peAssessment.getAssessmentObjectives();
assert(aos.AO1.name === 'Knowledge and Understanding', 'AO1 should be Knowledge and Understanding');
assert(aos.AO2.name === 'Application', 'AO2 should be Application');
assert(aos.AO3.name === 'Analysis and Evaluation', 'AO3 should be Analysis and Evaluation');
console.log('✓ Assessment objectives info correct\n');

// Test 6: Diagnostic generation
console.log('Test 6: Diagnostic insights generation');
const assessment = {
  percentage: 45,
  aoBreakdown: {
    AO1: { marks: 2, maxMarks: 5, percentage: 40 },
    AO2: { marks: 3, maxMarks: 5, percentage: 60 },
    AO3: { marks: 1, maxMarks: 5, percentage: 20 }
  }
};

const AssessmentEngine = require('../src/assessmentEngine');
const engine = new AssessmentEngine();
const diagnostics = engine.generateDiagnostics(assessment);

assert(diagnostics.weaknesses.length >= 2, 'Should identify weaknesses');
assert(diagnostics.recommendations.length >= 2, 'Should provide recommendations');
assert(diagnostics.overallMessage, 'Should have overall message');
console.log('✓ Diagnostic generation works\n');

// Test 7: Feedback report formatting
console.log('Test 7: Feedback report text formatting');
const report = generator.generateReport(result2.assessment);
const textReport = generator.formatAsText(report);
assert(textReport.includes('SUMMARY'), 'Should include summary section');
assert(textReport.includes('ASSESSMENT OBJECTIVES'), 'Should include AO section');
assert(textReport.includes('ACTION PLAN'), 'Should include action plan');
console.log('✓ Report formatting works\n');

console.log('=================================');
console.log('All tests passed! ✓');
console.log('=================================');
