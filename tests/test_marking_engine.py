"""
Unit tests for marking engine
"""

import pytest
from src.models import (
    MarkScheme, MarkCriteria, StudentAnswer,
    AssessmentObjective, Topic
)
from src.marking import MarkingEngine


@pytest.fixture
def sample_mark_scheme():
    """Create a sample mark scheme for testing"""
    criteria1 = MarkCriteria(
        question_id="1a",
        max_marks=2,
        assessment_objective=AssessmentObjective.AO1,
        keywords=["aerobic", "oxygen", "energy"],
        acceptable_answers=[
            "Uses oxygen to produce energy",
            "Occurs in the presence of oxygen"
        ]
    )
    
    criteria2 = MarkCriteria(
        question_id="1b",
        max_marks=3,
        assessment_objective=AssessmentObjective.AO2,
        keywords=["marathon", "endurance"],
        acceptable_answers=[
            "Marathon requires sustained energy production",
            "Aerobic system provides energy over long duration"
        ]
    )
    
    return MarkScheme(
        assessment_id="TEST_001",
        assessment_title="Test Assessment",
        mark_criteria=[criteria1, criteria2],
        topics=[],
        total_marks=5
    )


def test_marking_engine_initialization(sample_mark_scheme):
    """Test marking engine initialization"""
    engine = MarkingEngine(sample_mark_scheme)
    
    assert engine.mark_scheme == sample_mark_scheme
    assert engine.confidence_threshold == 0.7
    assert len(engine.criteria_map) == 2


def test_mark_answer_good_match(sample_mark_scheme):
    """Test marking a good answer"""
    engine = MarkingEngine(sample_mark_scheme)
    
    student_answer = StudentAnswer(
        question_id="1a",
        answer_text="The aerobic system uses oxygen to produce energy in the body",
        student_id="S001"
    )
    
    marked = engine.mark_answer(student_answer)
    
    assert marked.question_id == "1a"
    assert marked.marks_awarded > 0
    assert marked.max_marks == 2
    assert marked.confidence_score > 0.6


def test_mark_answer_poor_match(sample_mark_scheme):
    """Test marking a poor answer"""
    engine = MarkingEngine(sample_mark_scheme)
    
    student_answer = StudentAnswer(
        question_id="1a",
        answer_text="This is not related to the question",
        student_id="S001"
    )
    
    marked = engine.mark_answer(student_answer)
    
    assert marked.question_id == "1a"
    assert marked.marks_awarded <= 1  # Low or zero marks for poor answer
    assert marked.max_marks == 2


def test_mark_answer_with_keywords(sample_mark_scheme):
    """Test marking answer with good keyword coverage"""
    engine = MarkingEngine(sample_mark_scheme)
    
    student_answer = StudentAnswer(
        question_id="1a",
        answer_text="Aerobic means with oxygen and produces energy",
        student_id="S001"
    )
    
    marked = engine.mark_answer(student_answer)
    
    assert marked.marks_awarded > 0
    # Should get partial credit for keywords even if not exact match


def test_mark_batch(sample_mark_scheme):
    """Test batch marking"""
    engine = MarkingEngine(sample_mark_scheme)
    
    answers = [
        StudentAnswer("1a", "Uses oxygen for energy", "S001"),
        StudentAnswer("1b", "Marathon needs aerobic system", "S001")
    ]
    
    marked_answers = engine.mark_batch(answers)
    
    assert len(marked_answers) == 2
    assert all(isinstance(m.marks_awarded, int) for m in marked_answers)


def test_ao3_evaluation_marking(sample_mark_scheme):
    """Test that AO3 (evaluation) answers require analytical language"""
    criteria = MarkCriteria(
        question_id="2",
        max_marks=4,
        assessment_objective=AssessmentObjective.AO3,
        keywords=["compare", "contrast"],
        acceptable_answers=["Comparison of two methods"]
    )
    
    mark_scheme = MarkScheme(
        assessment_id="TEST_002",
        assessment_title="Test",
        mark_criteria=[criteria],
        topics=[],
        total_marks=4
    )
    
    engine = MarkingEngine(mark_scheme)
    
    # Answer without analytical language
    answer1 = StudentAnswer(
        "2",
        "Method A is good. Method B is also good.",
        "S001"
    )
    marked1 = engine.mark_answer(answer1)
    
    # Answer with analytical language
    answer2 = StudentAnswer(
        "2",
        "Method A is effective because it provides immediate results. However, Method B is more sustainable in the long term.",
        "S002"
    )
    marked2 = engine.mark_answer(answer2)
    
    # Answer with analytical language should score better
    assert marked2.marks_awarded >= marked1.marks_awarded


def test_unknown_question_handling(sample_mark_scheme):
    """Test handling of questions not in mark scheme"""
    engine = MarkingEngine(sample_mark_scheme)
    
    answer = StudentAnswer(
        question_id="99",  # Not in mark scheme
        answer_text="Some answer",
        student_id="S001"
    )
    
    marked = engine.mark_answer(answer)
    
    assert marked.marks_awarded == 0
    assert marked.max_marks == 0
    assert "No marking criteria" in marked.feedback


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
