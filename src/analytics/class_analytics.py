"""Analytics and reporting for class-level performance"""

from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import statistics

from models.data_models import (
    StudentReport, ClassAnalytics, AssessmentObjective,
    MarkScheme, PerformanceLevel
)


class ClassAnalyticsEngine:
    """Generate class-level analytics and insights"""
    
    def __init__(self, mark_scheme: MarkScheme, mastery_threshold: float = 60.0):
        """
        Initialize analytics engine
        
        Args:
            mark_scheme: The mark scheme used for assessment
            mastery_threshold: Percentage threshold for mastery (default 60%)
        """
        self.mark_scheme = mark_scheme
        self.mastery_threshold = mastery_threshold
    
    def generate_class_analytics(
        self,
        class_id: str,
        student_reports: List[StudentReport]
    ) -> ClassAnalytics:
        """Generate comprehensive class analytics"""
        
        if not student_reports:
            return self._empty_analytics(class_id)
        
        # Calculate average score
        total_scores = [report.total_score for report in student_reports]
        max_scores = [report.max_possible_score for report in student_reports]
        
        avg_total = statistics.mean(total_scores)
        avg_max = statistics.mean(max_scores)
        average_score = (avg_total / avg_max * 100) if avg_max > 0 else 0
        
        # Question performance analysis
        question_performance = self._analyze_question_performance(student_reports)
        
        # Topic performance analysis
        topic_performance = self._analyze_topic_performance(student_reports)
        
        # AO performance analysis
        ao_performance = self._analyze_ao_performance(student_reports)
        
        # Common misconceptions
        common_misconceptions = self._identify_common_misconceptions(student_reports)
        
        # Threshold concepts below mastery
        threshold_concepts = self._identify_threshold_concepts_below_mastery(
            topic_performance
        )
        
        # Generate teaching recommendations
        teaching_recommendations = self._generate_teaching_recommendations(
            question_performance,
            topic_performance,
            common_misconceptions,
            threshold_concepts
        )
        
        return ClassAnalytics(
            class_id=class_id,
            student_reports=student_reports,
            average_score=average_score,
            question_performance=question_performance,
            topic_performance=topic_performance,
            ao_performance=ao_performance,
            common_misconceptions=common_misconceptions,
            threshold_concepts_below_mastery=threshold_concepts,
            teaching_recommendations=teaching_recommendations
        )
    
    def _analyze_question_performance(
        self,
        student_reports: List[StudentReport]
    ) -> Dict[str, float]:
        """Calculate % correct per question"""
        question_stats = defaultdict(lambda: {'total': 0, 'max': 0})
        
        for report in student_reports:
            for answer in report.marked_answers:
                question_stats[answer.question_id]['total'] += answer.marks_awarded
                question_stats[answer.question_id]['max'] += answer.max_marks
        
        performance = {}
        for question_id, stats in question_stats.items():
            if stats['max'] > 0:
                percentage = (stats['total'] / stats['max']) * 100
                performance[question_id] = percentage
        
        return performance
    
    def _analyze_topic_performance(
        self,
        student_reports: List[StudentReport]
    ) -> Dict[str, float]:
        """Calculate % correct per topic"""
        topic_stats = defaultdict(lambda: {'total': 0, 'max': 0})
        
        for report in student_reports:
            # Aggregate from traffic light system
            for topic, level in report.traffic_light_by_topic.items():
                # Estimate scores from performance level
                if level == PerformanceLevel.HIGH:
                    score = 80
                elif level == PerformanceLevel.MEDIUM:
                    score = 60
                else:
                    score = 40
                
                topic_stats[topic]['total'] += score
                topic_stats[topic]['max'] += 100
        
        performance = {}
        for topic, stats in topic_stats.items():
            if stats['max'] > 0:
                percentage = (stats['total'] / stats['max']) * 100
                performance[topic] = percentage
        
        return performance
    
    def _analyze_ao_performance(
        self,
        student_reports: List[StudentReport]
    ) -> Dict[AssessmentObjective, float]:
        """Calculate performance by Assessment Objective"""
        ao_stats = {
            AssessmentObjective.AO1: {'total': 0, 'count': 0},
            AssessmentObjective.AO2: {'total': 0, 'count': 0},
            AssessmentObjective.AO3: {'total': 0, 'count': 0}
        }
        
        for report in student_reports:
            # AO1
            if report.ao1_score:
                ao1_total = sum(report.ao1_score.values())
                ao_stats[AssessmentObjective.AO1]['total'] += ao1_total
                ao_stats[AssessmentObjective.AO1]['count'] += 1
            
            # AO2
            if report.ao2_score:
                ao2_total = sum(report.ao2_score.values())
                ao_stats[AssessmentObjective.AO2]['total'] += ao2_total
                ao_stats[AssessmentObjective.AO2]['count'] += 1
            
            # AO3
            if report.ao3_score:
                ao3_total = sum(report.ao3_score.values())
                ao_stats[AssessmentObjective.AO3]['total'] += ao3_total
                ao_stats[AssessmentObjective.AO3]['count'] += 1
        
        performance = {}
        for ao, stats in ao_stats.items():
            if stats['count'] > 0:
                # Calculate average marks per student for this AO
                avg_marks = stats['total'] / stats['count']
                # Normalize to percentage (assuming max ~10 marks per AO per student)
                performance[ao] = min(100, (avg_marks / 10) * 100)
        
        return performance
    
    def _identify_common_misconceptions(
        self,
        student_reports: List[StudentReport]
    ) -> List[Tuple[str, int]]:
        """Identify most common misconceptions with counts"""
        all_misconceptions = []
        
        for report in student_reports:
            all_misconceptions.extend(report.identified_misconceptions)
        
        misconception_counts = Counter(all_misconceptions)
        
        # Return top 5 most common
        return misconception_counts.most_common(5)
    
    def _identify_threshold_concepts_below_mastery(
        self,
        topic_performance: Dict[str, float]
    ) -> List[str]:
        """Identify threshold concepts performing below mastery level"""
        below_mastery = []
        
        # Get threshold concepts from mark scheme
        threshold_topics = [
            topic.name for topic in self.mark_scheme.topics 
            if topic.threshold_concept
        ]
        
        for topic in threshold_topics:
            if topic in topic_performance:
                if topic_performance[topic] < self.mastery_threshold:
                    below_mastery.append(topic)
        
        # Also check any topic below mastery
        for topic, percentage in topic_performance.items():
            if percentage < self.mastery_threshold and topic not in below_mastery:
                below_mastery.append(topic)
        
        return below_mastery
    
    def _generate_teaching_recommendations(
        self,
        question_performance: Dict[str, float],
        topic_performance: Dict[str, float],
        common_misconceptions: List[Tuple[str, int]],
        threshold_concepts: List[str]
    ) -> List[str]:
        """Generate AI-powered teaching recommendations"""
        recommendations = []
        
        # Priority 1: Threshold concepts
        if threshold_concepts:
            top_threshold = threshold_concepts[0]
            recommendations.append(
                f"HIGH PRIORITY: Reteach '{top_threshold}' - This is a threshold concept "
                f"and is below mastery level ({self.mastery_threshold}%)"
            )
        
        # Priority 2: Weakest topics
        if topic_performance:
            sorted_topics = sorted(topic_performance.items(), key=lambda x: x[1])
            weakest_topic, percentage = sorted_topics[0]
            recommendations.append(
                f"FOCUS: '{weakest_topic}' needs attention - Class average is {percentage:.1f}%"
            )
        
        # Priority 3: Common misconceptions
        if common_misconceptions:
            top_misconception, count = common_misconceptions[0]
            percentage_affected = (count / len(self.mark_scheme.mark_criteria)) * 100
            recommendations.append(
                f"ADDRESS MISCONCEPTION: '{top_misconception}' - Affects {count} students "
                f"({percentage_affected:.0f}% of class)"
            )
        
        # Priority 4: Weakest questions
        if question_performance:
            sorted_questions = sorted(question_performance.items(), key=lambda x: x[1])
            weakest_q, q_percentage = sorted_questions[0]
            recommendations.append(
                f"REVIEW: Question {weakest_q} - Only {q_percentage:.1f}% average score. "
                f"Consider revisiting this topic in class."
            )
        
        # Priority 5: AO-specific recommendations
        # (Would analyze AO performance here if passed)
        recommendations.append(
            "INTERVENTION: Consider small group work for students scoring below 40% overall"
        )
        
        return recommendations
    
    def _empty_analytics(self, class_id: str) -> ClassAnalytics:
        """Return empty analytics when no student reports"""
        return ClassAnalytics(
            class_id=class_id,
            student_reports=[],
            average_score=0.0
        )
    
    def format_class_report_text(self, analytics: ClassAnalytics) -> str:
        """Format class analytics as readable text"""
        lines = []
        
        lines.append("=" * 80)
        lines.append("CLASS PERFORMANCE REPORT")
        lines.append(f"Class ID: {analytics.class_id}")
        lines.append(f"Number of Students: {len(analytics.student_reports)}")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append(f"CLASS AVERAGE: {analytics.average_score:.1f}%")
        lines.append("")
        
        # Question performance
        if analytics.question_performance:
            lines.append("PERFORMANCE BY QUESTION:")
            lines.append("-" * 80)
            for question_id, percentage in sorted(analytics.question_performance.items()):
                bar = "█" * int(percentage / 5)  # Visual bar
                lines.append(f"Question {question_id}: {percentage:.1f}% {bar}")
            lines.append("")
        
        # Topic performance
        if analytics.topic_performance:
            lines.append("PERFORMANCE BY TOPIC:")
            lines.append("-" * 80)
            for topic, percentage in sorted(analytics.topic_performance.items(), 
                                          key=lambda x: x[1]):
                icon = "🟢" if percentage >= 70 else "🟡" if percentage >= 50 else "🔴"
                lines.append(f"{icon} {topic}: {percentage:.1f}%")
            lines.append("")
        
        # AO performance
        if analytics.ao_performance:
            lines.append("PERFORMANCE BY ASSESSMENT OBJECTIVE:")
            lines.append("-" * 80)
            for ao, percentage in analytics.ao_performance.items():
                lines.append(f"{ao.value} ({ao.name}): {percentage:.1f}%")
            lines.append("")
        
        # Common misconceptions
        if analytics.common_misconceptions:
            lines.append("TOP MISCONCEPTIONS:")
            lines.append("-" * 80)
            for misconception, count in analytics.common_misconceptions:
                lines.append(f"⚠️  {misconception} ({count} students)")
            lines.append("")
        
        # Threshold concepts below mastery
        if analytics.threshold_concepts_below_mastery:
            lines.append("THRESHOLD CONCEPTS BELOW MASTERY:")
            lines.append("-" * 80)
            for concept in analytics.threshold_concepts_below_mastery:
                lines.append(f"❗ {concept}")
            lines.append("")
        
        # Teaching recommendations
        lines.append("TEACHING RECOMMENDATIONS:")
        lines.append("-" * 80)
        for i, recommendation in enumerate(analytics.teaching_recommendations, 1):
            lines.append(f"{i}. {recommendation}")
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
