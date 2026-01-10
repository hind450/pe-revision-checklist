"""AI-powered marking engine for student assessments"""

import re
from typing import List, Dict, Optional, Tuple
import logging
from difflib import SequenceMatcher

from models.data_models import (
    MarkCriteria, StudentAnswer, MarkedAnswer, 
    AssessmentObjective, MarkScheme
)

logger = logging.getLogger(__name__)


class MarkingEngine:
    """Core marking engine with NLP-based assessment"""
    
    def __init__(self, mark_scheme: MarkScheme, confidence_threshold: float = 0.7):
        """
        Initialize marking engine
        
        Args:
            mark_scheme: The mark scheme to use for marking
            confidence_threshold: Minimum confidence score to accept marking without review
        """
        self.mark_scheme = mark_scheme
        self.confidence_threshold = confidence_threshold
        self.criteria_map = {criteria.question_id: criteria for criteria in mark_scheme.mark_criteria}
    
    def mark_answer(self, student_answer: StudentAnswer) -> MarkedAnswer:
        """
        Mark a single student answer
        
        Args:
            student_answer: The student's answer to mark
            
        Returns:
            MarkedAnswer with score and feedback
        """
        criteria = self.criteria_map.get(student_answer.question_id)
        
        if not criteria:
            logger.warning(f"No criteria found for question {student_answer.question_id}")
            return self._create_unmarked_answer(student_answer)
        
        # Perform initial marking
        marks, confidence, matched_criteria = self._assess_answer(
            student_answer.answer_text,
            criteria
        )
        
        # If confidence is low, perform additional analysis
        if confidence < self.confidence_threshold:
            marks, confidence, matched_criteria = self._recheck_with_enhanced_analysis(
                student_answer.answer_text,
                criteria,
                marks,
                confidence,
                matched_criteria
            )
        
        # Identify misconceptions
        misconceptions = self._identify_misconceptions(
            student_answer.answer_text,
            criteria
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            marks,
            criteria.max_marks,
            criteria.assessment_objective,
            matched_criteria,
            misconceptions
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(
            marks,
            criteria,
            misconceptions
        )
        
        return MarkedAnswer(
            question_id=student_answer.question_id,
            student_id=student_answer.student_id,
            answer_text=student_answer.answer_text,
            marks_awarded=marks,
            max_marks=criteria.max_marks,
            assessment_objective=criteria.assessment_objective,
            feedback=feedback,
            identified_misconceptions=misconceptions,
            confidence_score=confidence,
            next_steps=next_steps
        )
    
    def mark_batch(self, student_answers: List[StudentAnswer]) -> List[MarkedAnswer]:
        """Mark multiple student answers"""
        return [self.mark_answer(answer) for answer in student_answers]
    
    def _assess_answer(self, answer_text: str, criteria: MarkCriteria) -> Tuple[int, float, List[str]]:
        """
        Assess a student answer against marking criteria
        
        Returns:
            Tuple of (marks_awarded, confidence_score, matched_criteria)
        """
        answer_lower = answer_text.lower()
        matched_criteria = []
        keyword_matches = 0
        total_keywords = len(criteria.keywords)
        
        # Check for keyword matches
        for keyword in criteria.keywords:
            if keyword.lower() in answer_lower:
                keyword_matches += 1
        
        # Check for acceptable answer matches
        acceptable_matches = []
        for acceptable in criteria.acceptable_answers:
            similarity = self._calculate_similarity(answer_text, acceptable)
            if similarity > 0.6:  # 60% similarity threshold
                acceptable_matches.append((acceptable, similarity))
                matched_criteria.append(acceptable)
        
        # Calculate marks based on matches
        marks = 0
        confidence = 0.0
        
        if acceptable_matches:
            # Sort by similarity
            acceptable_matches.sort(key=lambda x: x[1], reverse=True)
            
            # Award marks based on best matches and partial credit
            best_similarity = acceptable_matches[0][1]
            num_matches = len(acceptable_matches)
            
            if best_similarity > 0.85 and num_matches >= criteria.max_marks:
                marks = criteria.max_marks
                confidence = 0.9
            elif best_similarity > 0.75:
                marks = min(num_matches, criteria.max_marks)
                confidence = 0.8
            elif best_similarity > 0.6:
                marks = min(num_matches, criteria.max_marks - 1)
                confidence = 0.7
            else:
                marks = 1
                confidence = 0.5
        
        # Adjust for keyword coverage
        if total_keywords > 0:
            keyword_coverage = keyword_matches / total_keywords
            confidence = (confidence + keyword_coverage) / 2
            
            # Give partial credit for good keyword coverage even without exact matches
            if marks == 0 and keyword_coverage > 0.5:
                marks = 1
                confidence = max(confidence, 0.6)
        
        # Assessment objective specific adjustments
        if criteria.assessment_objective == AssessmentObjective.AO1:
            # AO1 requires specific factual content
            if keyword_matches < total_keywords * 0.5:
                confidence *= 0.8
        elif criteria.assessment_objective == AssessmentObjective.AO3:
            # AO3 requires more analytical depth
            analytical_words = ['because', 'therefore', 'however', 'although', 'whereas', 
                              'consequently', 'furthermore', 'moreover', 'nevertheless']
            has_analysis = any(word in answer_lower for word in analytical_words)
            if not has_analysis and marks > 0:
                marks = max(1, marks - 1)
                confidence *= 0.9
        
        return marks, confidence, matched_criteria
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _recheck_with_enhanced_analysis(
        self, 
        answer_text: str, 
        criteria: MarkCriteria,
        initial_marks: int,
        initial_confidence: float,
        initial_matched: List[str]
    ) -> Tuple[int, float, List[str]]:
        """
        Perform enhanced analysis when initial confidence is low
        """
        logger.info(f"Rechecking answer for question {criteria.question_id} - low confidence")
        
        # Break answer into sentences for more granular analysis
        sentences = re.split(r'[.!?]+', answer_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Check each sentence against criteria
        sentence_scores = []
        all_matches = []
        
        for sentence in sentences:
            for acceptable in criteria.acceptable_answers:
                similarity = self._calculate_similarity(sentence, acceptable)
                if similarity > 0.5:
                    sentence_scores.append(similarity)
                    if acceptable not in all_matches:
                        all_matches.append(acceptable)
        
        if sentence_scores:
            avg_similarity = sum(sentence_scores) / len(sentence_scores)
            max_similarity = max(sentence_scores)
            
            # Recalculate marks
            new_marks = min(len(set(all_matches)), criteria.max_marks)
            new_confidence = (avg_similarity + max_similarity) / 2
            
            # Use better result
            if new_confidence > initial_confidence:
                return new_marks, new_confidence, all_matches
        
        return initial_marks, initial_confidence, initial_matched
    
    def _identify_misconceptions(self, answer_text: str, criteria: MarkCriteria) -> List[str]:
        """Identify common misconceptions in student answer"""
        misconceptions = []
        answer_lower = answer_text.lower()
        
        # Check against known misconceptions
        for misconception in criteria.common_misconceptions:
            if misconception.lower() in answer_lower:
                misconceptions.append(misconception)
        
        # Check for common PE GCSE misconceptions
        common_misconceptions = {
            "Confused aerobic and anaerobic processes": [
                ("aerobic", "without oxygen"), ("anaerobic", "with oxygen")
            ],
            "Confused voluntary and involuntary muscles": [
                ("cardiac", "voluntary"), ("skeletal", "involuntary")
            ],
            "Confused arteries and veins": [
                ("arteries", "deoxygenated"), ("veins", "oxygenated")
            ],
            "Misapplied SMART target principles": [
                ("smart", "easy"), ("specific", "general")
            ]
        }
        
        for misconception, patterns in common_misconceptions.items():
            for term1, term2 in patterns:
                if term1 in answer_lower and term2 in answer_lower:
                    misconceptions.append(misconception)
                    break
        
        return misconceptions
    
    def _generate_feedback(
        self,
        marks: int,
        max_marks: int,
        ao: AssessmentObjective,
        matched_criteria: List[str],
        misconceptions: List[str]
    ) -> str:
        """Generate actionable feedback for student"""
        feedback_parts = []
        
        # Score feedback
        percentage = (marks / max_marks * 100) if max_marks > 0 else 0
        if percentage >= 80:
            feedback_parts.append(f"Excellent answer! You scored {marks}/{max_marks} marks.")
        elif percentage >= 60:
            feedback_parts.append(f"Good answer. You scored {marks}/{max_marks} marks.")
        elif percentage >= 40:
            feedback_parts.append(f"Satisfactory answer. You scored {marks}/{max_marks} marks.")
        else:
            feedback_parts.append(f"You scored {marks}/{max_marks} marks. There is room for improvement.")
        
        # AO-specific feedback
        if ao == AssessmentObjective.AO1:
            if marks < max_marks:
                feedback_parts.append("To improve, ensure you include all key facts and concepts.")
        elif ao == AssessmentObjective.AO2:
            if marks < max_marks:
                feedback_parts.append("To improve, demonstrate how you apply knowledge to the context given.")
        elif ao == AssessmentObjective.AO3:
            if marks < max_marks:
                feedback_parts.append("To improve, provide more analytical depth and critical evaluation.")
        
        # Misconception feedback
        if misconceptions:
            feedback_parts.append(f"Note: {misconceptions[0]}. Review this concept carefully.")
        
        # Positive reinforcement
        if matched_criteria:
            feedback_parts.append(f"Well done on including: {matched_criteria[0]}")
        
        return " ".join(feedback_parts)
    
    def _generate_next_steps(
        self,
        marks: int,
        criteria: MarkCriteria,
        misconceptions: List[str]
    ) -> List[str]:
        """Generate actionable next steps for improvement"""
        next_steps = []
        
        if marks < criteria.max_marks:
            # Generate specific next steps based on missing content
            if criteria.assessment_objective == AssessmentObjective.AO1:
                next_steps.append(f"Review and memorize the key characteristics related to question {criteria.question_id}")
                if criteria.keywords:
                    sample_keywords = criteria.keywords[:3]
                    next_steps.append(f"Focus on understanding: {', '.join(sample_keywords)}")
            
            elif criteria.assessment_objective == AssessmentObjective.AO2:
                next_steps.append(f"Practice applying concepts to different scenarios and contexts")
                next_steps.append(f"Work through example questions that require application of knowledge")
            
            elif criteria.assessment_objective == AssessmentObjective.AO3:
                next_steps.append(f"Practice analytical writing with evaluative language")
                next_steps.append(f"Compare and contrast different viewpoints in your answers")
        
        # Address misconceptions
        if misconceptions:
            next_steps.append(f"Review the topic to correct understanding of: {misconceptions[0]}")
        
        return next_steps[:3]  # Limit to top 3 actionable steps
    
    def _create_unmarked_answer(self, student_answer: StudentAnswer) -> MarkedAnswer:
        """Create a marked answer object for questions without criteria"""
        return MarkedAnswer(
            question_id=student_answer.question_id,
            student_id=student_answer.student_id,
            answer_text=student_answer.answer_text,
            marks_awarded=0,
            max_marks=0,
            assessment_objective=AssessmentObjective.AO1,
            feedback="No marking criteria available for this question.",
            confidence_score=0.0
        )
