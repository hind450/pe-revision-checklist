/**
 * PE Assessment for Learning System
 * 
 * Core assessment engine that provides automated marking and feedback
 * based on Assessment Objectives (AO1-AO3)
 */

class AssessmentEngine {
  constructor() {
    this.assessmentObjectives = {
      AO1: {
        name: 'Knowledge and Understanding',
        description: 'Demonstrate knowledge and understanding of physical education',
        weight: 0.33
      },
      AO2: {
        name: 'Application',
        description: 'Apply knowledge and understanding',
        weight: 0.33
      },
      AO3: {
        name: 'Analysis and Evaluation',
        description: 'Analyse and evaluate physical education concepts',
        weight: 0.34
      }
    };
  }

  /**
   * Assess a student script against a mark scheme
   * @param {Object} studentScript - The student's answer
   * @param {Object} markScheme - The marking criteria
   * @param {Object} examinerComments - Reference comments from examiners
   * @returns {Object} Assessment result with marks and feedback
   */
  assessScript(studentScript, markScheme, examinerComments = {}) {
    const assessment = {
      studentId: studentScript.studentId,
      totalMarks: 0,
      maxMarks: markScheme.maxMarks || 0,
      percentage: 0,
      aoBreakdown: {
        AO1: { marks: 0, maxMarks: 0, percentage: 0 },
        AO2: { marks: 0, maxMarks: 0, percentage: 0 },
        AO3: { marks: 0, maxMarks: 0, percentage: 0 }
      },
      feedback: [],
      diagnostics: {},
      timestamp: new Date().toISOString()
    };

    // Assess each question
    if (studentScript.answers && markScheme.questions) {
      markScheme.questions.forEach((question, index) => {
        const studentAnswer = studentScript.answers[index];
        if (studentAnswer) {
          const questionResult = this.assessQuestion(
            studentAnswer,
            question,
            examinerComments
          );
          
          assessment.totalMarks += questionResult.marks;
          
          // Update AO breakdown
          if (question.assessmentObjective) {
            const ao = question.assessmentObjective;
            assessment.aoBreakdown[ao].marks += questionResult.marks;
            assessment.aoBreakdown[ao].maxMarks += question.maxMarks;
          }
          
          assessment.feedback.push({
            questionNumber: index + 1,
            marks: questionResult.marks,
            maxMarks: question.maxMarks,
            feedback: questionResult.feedback,
            ao: question.assessmentObjective
          });
        }
      });
    }

    // Calculate percentages
    assessment.percentage = assessment.maxMarks > 0 
      ? Math.round((assessment.totalMarks / assessment.maxMarks) * 100)
      : 0;

    Object.keys(assessment.aoBreakdown).forEach(ao => {
      const aoData = assessment.aoBreakdown[ao];
      aoData.percentage = aoData.maxMarks > 0
        ? Math.round((aoData.marks / aoData.maxMarks) * 100)
        : 0;
    });

    // Generate diagnostic insights
    assessment.diagnostics = this.generateDiagnostics(assessment);

    return assessment;
  }

  /**
   * Assess a single question
   * @param {Object} studentAnswer - Student's answer to the question
   * @param {Object} question - Question from mark scheme
   * @param {Object} examinerComments - Reference comments
   * @returns {Object} Question assessment result
   */
  assessQuestion(studentAnswer, question, examinerComments) {
    const result = {
      marks: 0,
      feedback: []
    };

    const answerText = (studentAnswer.text || '').toLowerCase();
    const maxMarks = question.maxMarks || 0;

    // Check for key points from mark scheme
    if (question.markingPoints) {
      const pointsScored = [];
      const pointsMissed = [];

      question.markingPoints.forEach(point => {
        const keywords = point.keywords || [];
        const hasKeyword = keywords.some(keyword => 
          answerText.includes(keyword.toLowerCase())
        );

        if (hasKeyword) {
          result.marks += point.marks || 1;
          pointsScored.push(point.description);
        } else {
          pointsMissed.push(point.description);
        }
      });

      // Cap marks at maximum
      result.marks = Math.min(result.marks, maxMarks);

      // Generate feedback
      if (pointsScored.length > 0) {
        result.feedback.push({
          type: 'positive',
          message: `Good points: ${pointsScored.join(', ')}`
        });
      }

      if (pointsMissed.length > 0 && result.marks < maxMarks) {
        result.feedback.push({
          type: 'improvement',
          message: `Consider including: ${pointsMissed.join(', ')}`
        });
      }
    }

    return result;
  }

  /**
   * Generate diagnostic insights from assessment results
   * @param {Object} assessment - Complete assessment result
   * @returns {Object} Diagnostic insights with learning gaps and recommendations
   */
  generateDiagnostics(assessment) {
    const diagnostics = {
      strengths: [],
      weaknesses: [],
      learningGaps: [],
      recommendations: []
    };

    // Analyze AO performance
    Object.keys(assessment.aoBreakdown).forEach(ao => {
      const aoData = assessment.aoBreakdown[ao];
      const aoInfo = this.assessmentObjectives[ao];
      
      if (aoData.percentage >= 70) {
        diagnostics.strengths.push({
          area: ao,
          name: aoInfo.name,
          percentage: aoData.percentage,
          message: `Strong performance in ${aoInfo.name}`
        });
      } else if (aoData.percentage < 50) {
        diagnostics.weaknesses.push({
          area: ao,
          name: aoInfo.name,
          percentage: aoData.percentage,
          message: `Needs improvement in ${aoInfo.name}`
        });
        
        diagnostics.learningGaps.push({
          area: ao,
          gap: this.identifyLearningGap(ao, aoData.percentage)
        });
        
        diagnostics.recommendations.push({
          area: ao,
          recommendation: this.generateRecommendation(ao, aoData.percentage)
        });
      }
    });

    // Overall performance analysis
    if (assessment.percentage >= 70) {
      diagnostics.overallMessage = 'Good overall performance. Continue practicing to maintain this level.';
    } else if (assessment.percentage >= 50) {
      diagnostics.overallMessage = 'Satisfactory performance. Focus on identified areas for improvement.';
    } else {
      diagnostics.overallMessage = 'Significant improvement needed. Review fundamental concepts and practice regularly.';
    }

    return diagnostics;
  }

  /**
   * Identify specific learning gap for an assessment objective
   * @param {string} ao - Assessment objective (AO1, AO2, AO3)
   * @param {number} percentage - Performance percentage
   * @returns {string} Learning gap description
   */
  identifyLearningGap(ao, percentage) {
    const gaps = {
      AO1: 'Insufficient understanding of core PE concepts, terminology, and principles',
      AO2: 'Difficulty applying theoretical knowledge to practical scenarios',
      AO3: 'Limited ability to analyze and evaluate PE concepts critically'
    };

    return gaps[ao] || 'General knowledge gap identified';
  }

  /**
   * Generate recommendation for improvement
   * @param {string} ao - Assessment objective
   * @param {number} percentage - Performance percentage
   * @returns {string} Recommendation
   */
  generateRecommendation(ao, percentage) {
    const recommendations = {
      AO1: 'Review key terminology and concepts. Use flashcards and revision notes. Focus on understanding definitions and explanations.',
      AO2: 'Practice applying theory to real-world examples. Work through case studies and scenario-based questions.',
      AO3: 'Develop critical thinking skills. Practice comparing, contrasting, and evaluating different approaches. Use evaluation frameworks.'
    };

    return recommendations[ao] || 'Review course materials and practice past papers';
  }
}

module.exports = AssessmentEngine;
