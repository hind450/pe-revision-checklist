"""Feedback generation for students and teachers"""

from typing import List, Dict
from collections import Counter, defaultdict

from models.data_models import (
    MarkedAnswer, StudentReport, PerformanceLevel,
    AssessmentObjective, MarkScheme, Topic
)


class FeedbackGenerator:
    """Generate individual and class-level feedback"""
    
    def __init__(self, mark_scheme: MarkScheme):
        self.mark_scheme = mark_scheme
        self.topic_map = self._build_topic_map()
    
    def _build_topic_map(self) -> Dict[str, Topic]:
        """Build a map of question IDs to topics"""
        topic_map = {}
        for topic in self.mark_scheme.topics:
            for question_id in topic.related_questions:
                topic_map[question_id] = topic
        
        # If no explicit mapping, create generic topics from criteria
        if not topic_map:
            for criteria in self.mark_scheme.mark_criteria:
                # Use AO as topic if no specific topic
                topic_name = f"{criteria.assessment_objective.value}"
                if criteria.question_id not in topic_map:
                    topic_map[criteria.question_id] = Topic(
                        name=topic_name,
                        description=f"Questions assessing {topic_name}"
                    )
        
        return topic_map
    
    def generate_student_report(
        self,
        student_id: str,
        student_name: str,
        marked_answers: List[MarkedAnswer]
    ) -> StudentReport:
        """Generate comprehensive student performance report"""
        
        # Calculate total score
        total_score = sum(answer.marks_awarded for answer in marked_answers)
        max_possible = sum(answer.max_marks for answer in marked_answers)
        percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
        
        # Calculate AO scores by topic
        ao1_score = defaultdict(lambda: {'scored': 0, 'max': 0})
        ao2_score = defaultdict(lambda: {'scored': 0, 'max': 0})
        ao3_score = defaultdict(lambda: {'scored': 0, 'max': 0})
        
        for answer in marked_answers:
            topic = self.topic_map.get(answer.question_id)
            topic_name = topic.name if topic else "General"
            
            if answer.assessment_objective == AssessmentObjective.AO1:
                ao1_score[topic_name]['scored'] += answer.marks_awarded
                ao1_score[topic_name]['max'] += answer.max_marks
            elif answer.assessment_objective == AssessmentObjective.AO2:
                ao2_score[topic_name]['scored'] += answer.marks_awarded
                ao2_score[topic_name]['max'] += answer.max_marks
            elif answer.assessment_objective == AssessmentObjective.AO3:
                ao3_score[topic_name]['scored'] += answer.marks_awarded
                ao3_score[topic_name]['max'] += answer.max_marks
        
        # Calculate traffic light system by topic
        traffic_light = {}
        all_topics = set()
        
        for answer in marked_answers:
            topic = self.topic_map.get(answer.question_id)
            if topic:
                all_topics.add(topic.name)
        
        for topic_name in all_topics:
            topic_total = 0
            topic_max = 0
            
            # Sum across all AOs for this topic
            for ao_dict in [ao1_score, ao2_score, ao3_score]:
                if topic_name in ao_dict:
                    topic_total += ao_dict[topic_name]['scored']
                    topic_max += ao_dict[topic_name]['max']
            
            if topic_max > 0:
                topic_percentage = (topic_total / topic_max) * 100
                
                if topic_percentage >= 70:
                    traffic_light[topic_name] = PerformanceLevel.HIGH
                elif topic_percentage >= 50:
                    traffic_light[topic_name] = PerformanceLevel.MEDIUM
                else:
                    traffic_light[topic_name] = PerformanceLevel.LOW
        
        # Collect all misconceptions
        all_misconceptions = []
        for answer in marked_answers:
            all_misconceptions.extend(answer.identified_misconceptions)
        
        # Generate priority next steps
        priority_next_steps = self._generate_priority_next_steps(
            marked_answers,
            traffic_light
        )
        
        # Convert AO scores to simple format
        ao1_simple = {k: v['scored'] for k, v in ao1_score.items()}
        ao2_simple = {k: v['scored'] for k, v in ao2_score.items()}
        ao3_simple = {k: v['scored'] for k, v in ao3_score.items()}
        
        return StudentReport(
            student_id=student_id,
            student_name=student_name,
            marked_answers=marked_answers,
            total_score=total_score,
            max_possible_score=max_possible,
            percentage=percentage,
            ao1_score=ao1_simple,
            ao2_score=ao2_simple,
            ao3_score=ao3_simple,
            traffic_light_by_topic=traffic_light,
            priority_next_steps=priority_next_steps,
            identified_misconceptions=list(set(all_misconceptions))
        )
    
    def _generate_priority_next_steps(
        self,
        marked_answers: List[MarkedAnswer],
        traffic_light: Dict[str, PerformanceLevel]
    ) -> List[str]:
        """Generate prioritized next steps based on performance"""
        next_steps = []
        
        # Prioritize red (low performance) topics
        red_topics = [topic for topic, level in traffic_light.items() 
                     if level == PerformanceLevel.LOW]
        
        if red_topics:
            for topic in red_topics[:2]:  # Top 2 weakest topics
                next_steps.append(f"Priority: Review and revise {topic} - significant gaps identified")
        
        # Add specific next steps from low-scoring questions
        low_scoring = [answer for answer in marked_answers 
                      if answer.marks_awarded < answer.max_marks * 0.5]
        
        for answer in low_scoring[:3]:  # Top 3 lowest scoring
            if answer.next_steps:
                next_steps.append(answer.next_steps[0])
        
        # Add steps to address misconceptions
        misconceptions = []
        for answer in marked_answers:
            misconceptions.extend(answer.identified_misconceptions)
        
        if misconceptions:
            most_common = Counter(misconceptions).most_common(1)[0][0]
            next_steps.append(f"Address misconception: {most_common}")
        
        return next_steps[:5]  # Limit to top 5
    
    def format_student_report_text(self, report: StudentReport) -> str:
        """Format student report as readable text"""
        lines = []
        
        lines.append("=" * 60)
        lines.append(f"STUDENT PERFORMANCE REPORT")
        lines.append(f"Student: {report.student_name} (ID: {report.student_id})")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"Overall Score: {report.total_score}/{report.max_possible_score} ({report.percentage:.1f}%)")
        lines.append("")
        
        # Traffic light by topic
        lines.append("PERFORMANCE BY TOPIC (Traffic Light System):")
        lines.append("-" * 60)
        for topic, level in sorted(report.traffic_light_by_topic.items()):
            icon = "🟢" if level == PerformanceLevel.HIGH else "🟡" if level == PerformanceLevel.MEDIUM else "🔴"
            lines.append(f"{icon} {topic}: {level.value}")
        lines.append("")
        
        # Assessment Objectives
        lines.append("PERFORMANCE BY ASSESSMENT OBJECTIVE:")
        lines.append("-" * 60)
        
        if report.ao1_score:
            total_ao1 = sum(report.ao1_score.values())
            lines.append(f"AO1 (Knowledge): {total_ao1} marks")
            for topic, score in report.ao1_score.items():
                lines.append(f"  - {topic}: {score}")
        
        if report.ao2_score:
            total_ao2 = sum(report.ao2_score.values())
            lines.append(f"AO2 (Application): {total_ao2} marks")
            for topic, score in report.ao2_score.items():
                lines.append(f"  - {topic}: {score}")
        
        if report.ao3_score:
            total_ao3 = sum(report.ao3_score.values())
            lines.append(f"AO3 (Evaluation): {total_ao3} marks")
            for topic, score in report.ao3_score.items():
                lines.append(f"  - {topic}: {score}")
        lines.append("")
        
        # Misconceptions
        if report.identified_misconceptions:
            lines.append("IDENTIFIED MISCONCEPTIONS:")
            lines.append("-" * 60)
            for misconception in report.identified_misconceptions:
                lines.append(f"⚠️  {misconception}")
            lines.append("")
        
        # Priority next steps
        lines.append("PRIORITY NEXT STEPS:")
        lines.append("-" * 60)
        for i, step in enumerate(report.priority_next_steps, 1):
            lines.append(f"{i}. {step}")
        lines.append("")
        
        # Individual question feedback
        lines.append("DETAILED QUESTION FEEDBACK:")
        lines.append("-" * 60)
        for answer in report.marked_answers:
            lines.append(f"\nQuestion {answer.question_id}: {answer.marks_awarded}/{answer.max_marks} marks")
            lines.append(f"Assessment Objective: {answer.assessment_objective.value}")
            lines.append(f"Feedback: {answer.feedback}")
            if answer.next_steps:
                lines.append("Next steps:")
                for step in answer.next_steps:
                    lines.append(f"  - {step}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
