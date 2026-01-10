/**
 * PE Assessment for Learning - Main Entry Point
 * 
 * This module provides the main interface for the PE assessment system
 */

const AssessmentEngine = require('./assessmentEngine');
const FeedbackGenerator = require('./feedbackGenerator');

class PEAssessment {
  constructor() {
    this.engine = new AssessmentEngine();
    this.feedbackGenerator = new FeedbackGenerator();
  }

  /**
   * Process a complete assessment
   * @param {Object} studentScript - Student's answers
   * @param {Object} markScheme - Marking criteria
   * @param {Object} examinerComments - Optional examiner comments
   * @returns {Object} Complete assessment with feedback
   */
  processAssessment(studentScript, markScheme, examinerComments = {}) {
    // Perform assessment
    const assessment = this.engine.assessScript(
      studentScript,
      markScheme,
      examinerComments
    );

    // Generate feedback report
    const feedbackReport = this.feedbackGenerator.generateReport(assessment);

    return {
      assessment,
      feedbackReport,
      textReport: this.feedbackGenerator.formatAsText(feedbackReport)
    };
  }

  /**
   * Get assessment objectives information
   * @returns {Object} AO definitions
   */
  getAssessmentObjectives() {
    return this.engine.assessmentObjectives;
  }
}

// Example usage
function runExample() {
  console.log('PE Assessment for Learning System\n');
  console.log('==================================\n');

  const peAssessment = new PEAssessment();

  // Example student script
  const studentScript = {
    studentId: 'STUDENT001',
    answers: [
      {
        questionNumber: 1,
        text: 'Aerobic respiration uses oxygen to produce energy. It happens in the mitochondria and produces ATP which is used for muscle contraction.'
      },
      {
        questionNumber: 2,
        text: 'A warm-up helps prevent injury and prepares the body for exercise.'
      },
      {
        questionNumber: 3,
        text: 'Training improves performance by making muscles stronger and improving cardiovascular fitness.'
      }
    ]
  };

  // Example mark scheme
  const markScheme = {
    maxMarks: 15,
    questions: [
      {
        questionNumber: 1,
        maxMarks: 6,
        assessmentObjective: 'AO1',
        markingPoints: [
          {
            description: 'Aerobic respiration definition',
            keywords: ['aerobic', 'oxygen'],
            marks: 1
          },
          {
            description: 'Location in mitochondria',
            keywords: ['mitochondria'],
            marks: 1
          },
          {
            description: 'ATP production',
            keywords: ['ATP', 'energy'],
            marks: 1
          },
          {
            description: 'Use in muscle contraction',
            keywords: ['muscle', 'contraction'],
            marks: 1
          },
          {
            description: 'Chemical equation',
            keywords: ['glucose', 'carbon dioxide', 'water'],
            marks: 2
          }
        ]
      },
      {
        questionNumber: 2,
        maxMarks: 4,
        assessmentObjective: 'AO2',
        markingPoints: [
          {
            description: 'Injury prevention',
            keywords: ['injury', 'prevent'],
            marks: 1
          },
          {
            description: 'Increases heart rate gradually',
            keywords: ['heart rate', 'gradual'],
            marks: 1
          },
          {
            description: 'Increases blood flow to muscles',
            keywords: ['blood flow', 'muscle'],
            marks: 1
          },
          {
            description: 'Improves flexibility',
            keywords: ['flexibility', 'stretch'],
            marks: 1
          }
        ]
      },
      {
        questionNumber: 3,
        maxMarks: 5,
        assessmentObjective: 'AO3',
        markingPoints: [
          {
            description: 'Muscle strength adaptation',
            keywords: ['muscle', 'strong'],
            marks: 1
          },
          {
            description: 'Cardiovascular improvement',
            keywords: ['cardiovascular', 'fitness', 'heart'],
            marks: 1
          },
          {
            description: 'Progressive overload principle',
            keywords: ['progressive', 'overload', 'increase'],
            marks: 1
          },
          {
            description: 'Specific adaptations',
            keywords: ['specific', 'adaptation', 'SAID'],
            marks: 1
          },
          {
            description: 'Evaluation of training methods',
            keywords: ['evaluate', 'effective', 'compare'],
            marks: 1
          }
        ]
      }
    ]
  };

  // Process assessment
  const result = peAssessment.processAssessment(studentScript, markScheme);

  // Display results
  console.log(result.textReport);
  console.log('\n--- JSON ASSESSMENT DATA ---');
  console.log(JSON.stringify(result.assessment, null, 2));
}

// Run example if executed directly
if (require.main === module) {
  runExample();
}

module.exports = PEAssessment;
