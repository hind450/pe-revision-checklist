"""
Unit tests for data models
"""

import pytest
from src.models import (
    AssessmentObjective,
    PerformanceLevel,
    MarkCriteria,
    StudentAnswer,
    MarkedAnswer,
    Topic,
    StudentReport,
    ClassAnalytics,
    MarkScheme
)


def test_assessment_objective_enum():
    """Test AssessmentObjective enum"""
    assert AssessmentObjective.AO1.value == "Knowledge"
    assert AssessmentObjective.AO2.value == "Application"
    assert AssessmentObjective.AO3.value == "Evaluation"


def test_performance_level_enum():
    """Test PerformanceLevel enum"""
    assert PerformanceLevel.HIGH.value == "green"
    assert PerformanceLevel.MEDIUM.value == "amber"
    assert PerformanceLevel.LOW.value == "red"


def test_mark_criteria_creation():
    """Test MarkCriteria dataclass creation"""
    criteria = MarkCriteria(
        question_id="1a",
        max_marks=3,
        assessment_objective=AssessmentObjective.AO1,
        keywords=["aerobic", "oxygen"],
        acceptable_answers=["Uses oxygen to produce energy"]
    )
    
    assert criteria.question_id == "1a"
    assert criteria.max_marks == 3
    assert criteria.assessment_objective == AssessmentObjective.AO1
    assert len(criteria.keywords) == 2
    assert len(criteria.acceptable_answers) == 1


def test_student_answer_creation():
    """Test StudentAnswer dataclass creation"""
    answer = StudentAnswer(
        question_id="1a",
        answer_text="The aerobic system uses oxygen",
        student_id="S001"
    )
    
    assert answer.question_id == "1a"
    assert answer.student_id == "S001"
    assert "oxygen" in answer.answer_text


def test_marked_answer_creation():
    """Test MarkedAnswer dataclass creation"""
    marked = MarkedAnswer(
        question_id="1a",
        student_id="S001",
        answer_text="Test answer",
        marks_awarded=2,
        max_marks=3,
        assessment_objective=AssessmentObjective.AO1,
        feedback="Good answer",
        confidence_score=0.85
    )
    
    assert marked.marks_awarded == 2
    assert marked.max_marks == 3
    assert marked.confidence_score == 0.85


def test_topic_creation():
    """Test Topic dataclass creation"""
    topic = Topic(
        name="Energy Systems",
        description="Aerobic and anaerobic systems",
        threshold_concept=True
    )
    
    assert topic.name == "Energy Systems"
    assert topic.threshold_concept is True
    assert len(topic.related_questions) == 0


def test_student_report_creation():
    """Test StudentReport dataclass creation"""
    marked_answer = MarkedAnswer(
        question_id="1a",
        student_id="S001",
        answer_text="Test",
        marks_awarded=2,
        max_marks=3,
        assessment_objective=AssessmentObjective.AO1,
        feedback="Good"
    )
    
    report = StudentReport(
        student_id="S001",
        student_name="Test Student",
        marked_answers=[marked_answer],
        total_score=2,
        max_possible_score=3,
        percentage=66.7
    )
    
    assert report.student_id == "S001"
    assert report.total_score == 2
    assert report.percentage == 66.7
    assert len(report.marked_answers) == 1


def test_mark_scheme_creation():
    """Test MarkScheme dataclass creation"""
    criteria = MarkCriteria(
        question_id="1a",
        max_marks=3,
        assessment_objective=AssessmentObjective.AO1,
        keywords=["test"],
        acceptable_answers=["test answer"]
    )
    
    topic = Topic(name="Test Topic", description="Test")
    
    mark_scheme = MarkScheme(
        assessment_id="TEST_001",
        assessment_title="Test Assessment",
        mark_criteria=[criteria],
        topics=[topic],
        total_marks=3
    )
    
    assert mark_scheme.assessment_id == "TEST_001"
    assert mark_scheme.total_marks == 3
    assert len(mark_scheme.mark_criteria) == 1
    assert len(mark_scheme.topics) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
