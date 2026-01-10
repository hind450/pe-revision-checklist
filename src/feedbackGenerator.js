/**
 * Feedback Generator
 * 
 * Generates detailed, actionable feedback for students and teachers
 */

class FeedbackGenerator {
  /**
   * Generate comprehensive feedback report
   * @param {Object} assessment - Assessment results from AssessmentEngine
   * @returns {Object} Formatted feedback report
   */
  generateReport(assessment) {
    const report = {
      summary: this.generateSummary(assessment),
      questionFeedback: this.generateQuestionFeedback(assessment.feedback),
      aoAnalysis: this.generateAOAnalysis(assessment.aoBreakdown),
      diagnostics: assessment.diagnostics,
      actionPlan: this.generateActionPlan(assessment.diagnostics),
      timestamp: assessment.timestamp
    };

    return report;
  }

  /**
   * Generate summary section
   * @param {Object} assessment - Assessment results
   * @returns {Object} Summary information
   */
  generateSummary(assessment) {
    const grade = this.calculateGrade(assessment.percentage);
    
    return {
      studentId: assessment.studentId,
      totalMarks: assessment.totalMarks,
      maxMarks: assessment.maxMarks,
      percentage: assessment.percentage,
      grade: grade,
      performanceLevel: this.getPerformanceLevel(assessment.percentage)
    };
  }

  /**
   * Calculate grade from percentage
   * @param {number} percentage - Score percentage
   * @returns {string} Grade
   */
  calculateGrade(percentage) {
    if (percentage >= 90) return 'A*';
    if (percentage >= 80) return 'A';
    if (percentage >= 70) return 'B';
    if (percentage >= 60) return 'C';
    if (percentage >= 50) return 'D';
    if (percentage >= 40) return 'E';
    return 'U';
  }

  /**
   * Get performance level description
   * @param {number} percentage - Score percentage
   * @returns {string} Performance level
   */
  getPerformanceLevel(percentage) {
    if (percentage >= 80) return 'Excellent';
    if (percentage >= 70) return 'Good';
    if (percentage >= 60) return 'Satisfactory';
    if (percentage >= 50) return 'Pass';
    return 'Needs Improvement';
  }

  /**
   * Generate question-by-question feedback
   * @param {Array} feedback - Feedback array from assessment
   * @returns {Array} Formatted question feedback
   */
  generateQuestionFeedback(feedback) {
    return feedback.map(item => ({
      question: item.questionNumber,
      marks: `${item.marks}/${item.maxMarks}`,
      assessmentObjective: item.ao,
      feedback: item.feedback,
      suggestions: this.generateQuestionSuggestions(item)
    }));
  }

  /**
   * Generate suggestions for a specific question
   * @param {Object} questionFeedback - Feedback for a question
   * @returns {Array} Suggestions
   */
  generateQuestionSuggestions(questionFeedback) {
    const suggestions = [];
    
    if (questionFeedback.marks < questionFeedback.maxMarks) {
      suggestions.push('Review the mark scheme for this question');
      
      if (questionFeedback.ao === 'AO1') {
        suggestions.push('Ensure you include all key terminology and concepts');
      } else if (questionFeedback.ao === 'AO2') {
        suggestions.push('Provide specific examples to demonstrate application');
      } else if (questionFeedback.ao === 'AO3') {
        suggestions.push('Include analysis and evaluation with supporting evidence');
      }
    }
    
    return suggestions;
  }

  /**
   * Generate AO analysis section
   * @param {Object} aoBreakdown - AO breakdown from assessment
   * @returns {Array} AO analysis
   */
  generateAOAnalysis(aoBreakdown) {
    const analysis = [];
    
    Object.keys(aoBreakdown).forEach(ao => {
      const data = aoBreakdown[ao];
      analysis.push({
        objective: ao,
        marks: `${data.marks}/${data.maxMarks}`,
        percentage: data.percentage,
        status: this.getAOStatus(data.percentage),
        advice: this.getAOAdvice(ao, data.percentage)
      });
    });
    
    return analysis;
  }

  /**
   * Get status for an AO based on percentage
   * @param {number} percentage - AO percentage
   * @returns {string} Status
   */
  getAOStatus(percentage) {
    if (percentage >= 70) return 'Strong';
    if (percentage >= 50) return 'Adequate';
    return 'Needs Development';
  }

  /**
   * Get advice for an AO
   * @param {string} ao - Assessment objective
   * @param {number} percentage - Performance percentage
   * @returns {string} Advice
   */
  getAOAdvice(ao, percentage) {
    if (percentage >= 70) {
      return `Excellent work on ${ao}. Continue to develop these skills further.`;
    }
    
    const advice = {
      AO1: 'Focus on learning key terms, definitions, and core concepts. Create revision cards.',
      AO2: 'Practice applying your knowledge to different scenarios. Work through example questions.',
      AO3: 'Develop your evaluation skills. Practice justifying your answers with evidence.'
    };
    
    return advice[ao] || 'Continue practicing and reviewing course materials.';
  }

  /**
   * Generate action plan based on diagnostics
   * @param {Object} diagnostics - Diagnostic information
   * @returns {Object} Action plan
   */
  generateActionPlan(diagnostics) {
    const plan = {
      priorityAreas: [],
      shortTerm: [],
      longTerm: [],
      resources: []
    };

    // Identify priority areas from weaknesses
    diagnostics.weaknesses.forEach(weakness => {
      plan.priorityAreas.push({
        area: weakness.area,
        focus: weakness.name
      });
    });

    // Generate short-term actions
    if (diagnostics.recommendations && diagnostics.recommendations.length > 0) {
      diagnostics.recommendations.forEach(rec => {
        plan.shortTerm.push({
          action: rec.recommendation,
          area: rec.area
        });
      });
    }

    // Generate long-term actions
    plan.longTerm.push({
      action: 'Complete practice papers under timed conditions',
      benefit: 'Improve exam technique and time management'
    });
    
    plan.longTerm.push({
      action: 'Review examiner reports and grade boundaries',
      benefit: 'Understand assessment criteria and expectations'
    });

    // Suggest resources
    plan.resources.push('Past papers and mark schemes');
    plan.resources.push('Revision guides and textbooks');
    plan.resources.push('Online PE revision resources');
    plan.resources.push('Teacher feedback and one-to-one sessions');

    return plan;
  }

  /**
   * Format report as readable text
   * @param {Object} report - Feedback report
   * @returns {string} Formatted text report
   */
  formatAsText(report) {
    let text = '=== PE ASSESSMENT FEEDBACK REPORT ===\n\n';
    
    // Summary
    text += '--- SUMMARY ---\n';
    text += `Student ID: ${report.summary.studentId}\n`;
    text += `Score: ${report.summary.totalMarks}/${report.summary.maxMarks} (${report.summary.percentage}%)\n`;
    text += `Grade: ${report.summary.grade}\n`;
    text += `Performance Level: ${report.summary.performanceLevel}\n\n`;
    
    // AO Analysis
    text += '--- ASSESSMENT OBJECTIVES ANALYSIS ---\n';
    report.aoAnalysis.forEach(ao => {
      text += `${ao.objective}: ${ao.marks} (${ao.percentage}%) - ${ao.status}\n`;
      text += `  Advice: ${ao.advice}\n`;
    });
    text += '\n';
    
    // Diagnostics
    if (report.diagnostics.overallMessage) {
      text += '--- OVERALL PERFORMANCE ---\n';
      text += `${report.diagnostics.overallMessage}\n\n`;
    }
    
    if (report.diagnostics.strengths && report.diagnostics.strengths.length > 0) {
      text += '--- STRENGTHS ---\n';
      report.diagnostics.strengths.forEach(strength => {
        text += `• ${strength.message} (${strength.percentage}%)\n`;
      });
      text += '\n';
    }
    
    if (report.diagnostics.weaknesses && report.diagnostics.weaknesses.length > 0) {
      text += '--- AREAS FOR IMPROVEMENT ---\n';
      report.diagnostics.weaknesses.forEach(weakness => {
        text += `• ${weakness.message} (${weakness.percentage}%)\n`;
      });
      text += '\n';
    }
    
    if (report.diagnostics.learningGaps && report.diagnostics.learningGaps.length > 0) {
      text += '--- LEARNING GAPS IDENTIFIED ---\n';
      report.diagnostics.learningGaps.forEach(gap => {
        text += `• ${gap.area}: ${gap.gap}\n`;
      });
      text += '\n';
    }
    
    // Action Plan
    text += '--- ACTION PLAN ---\n';
    if (report.actionPlan.priorityAreas.length > 0) {
      text += 'Priority Areas:\n';
      report.actionPlan.priorityAreas.forEach(area => {
        text += `  • Focus on ${area.focus}\n`;
      });
      text += '\n';
    }
    
    if (report.actionPlan.shortTerm.length > 0) {
      text += 'Short-term Actions:\n';
      report.actionPlan.shortTerm.forEach(action => {
        text += `  • ${action.action}\n`;
      });
      text += '\n';
    }
    
    if (report.actionPlan.longTerm.length > 0) {
      text += 'Long-term Actions:\n';
      report.actionPlan.longTerm.forEach(action => {
        text += `  • ${action.action}\n`;
      });
      text += '\n';
    }
    
    text += 'Recommended Resources:\n';
    report.actionPlan.resources.forEach(resource => {
      text += `  • ${resource}\n`;
    });
    
    return text;
  }
}

module.exports = FeedbackGenerator;
