"""Data models for PE Assessment System"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class AssessmentObjective(Enum):
    """Assessment objectives for GCSE PE"""
    AO1 = "Knowledge"
    AO2 = "Application"
    AO3 = "Evaluation"


class PerformanceLevel(Enum):
    """Performance level indicators"""
    HIGH = "green"     # 70%+
    MEDIUM = "amber"   # 50-69%
    LOW = "red"        # <50%


class Topic(Enum):
    """PE GCSE Topics"""
    ENERGY_SYSTEMS = "Energy Systems"
    GOAL_SETTING = "Goal Setting and SMART Targets"
    INJURY_PREVENTION = "Injury Prevention"
    TRAINING_METHODS = "Training Methods"
    FITNESS_COMPONENTS = "Components of Fitness"
    SKILL_ACQUISITION = "Skill Acquisition"
    SPORTS_PSYCHOLOGY = "Sports Psychology"
    ANATOMY_PHYSIOLOGY = "Anatomy and Physiology"
    OTHER = "Other"


@dataclass
class MarkCriteria:
    """Mark criteria for a question"""
    question_id: str
    max_marks: int
    assessment_objective: AssessmentObjective
    keywords: List[str] = field(default_factory=list)
    acceptable_answers: List[str] = field(default_factory=list)
    topic: Optional[Topic] = None
    guidance: str = ""


@dataclass
class MarkScheme:
    """Complete mark scheme"""
    assessment_id: str
    title: str
    mark_criteria: List[MarkCriteria]
    total_marks: int
    topics: List[Topic] = field(default_factory=list)
    examiner_comments: Dict[str, str] = field(default_factory=dict)


@dataclass
class StudentAnswer:
    """Student's answer to a question"""
    question_id: str
    answer_text: str
    student_id: str


@dataclass
class MarkedAnswer:
    """Marked student answer"""
    question_id: str
    marks_awarded: int
    max_marks: int
    feedback: str
    confidence_score: float
    assessment_objective: AssessmentObjective
    identified_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)


@dataclass
class StudentReport:
    """Complete student report"""
    student_id: str
    student_name: str
    marked_answers: List[MarkedAnswer]
    total_score: int
    total_possible: int
    percentage: float
    performance_by_topic: Dict[str, PerformanceLevel] = field(default_factory=dict)
    misconceptions: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    traffic_light_summary: Dict[str, str] = field(default_factory=dict)


@dataclass
class ClassAnalytics:
    """Class-level analytics"""
    class_id: str
    student_reports: List[StudentReport]
    average_score: float
    highest_score: float
    lowest_score: float
    question_performance: Dict[str, float] = field(default_factory=dict)
    topic_performance: Dict[str, float] = field(default_factory=dict)
    common_misconceptions: List[Dict[str, any]] = field(default_factory=list)
    teaching_recommendations: List[str] = field(default_factory=list)
    threshold_concepts: List[str] = field(default_factory=list)
