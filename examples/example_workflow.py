"""
Example Usage: Complete Workflow
Demonstrates the full PE Assessment System workflow
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import PEAssessmentSystem


def example_complete_workflow():
    """Complete workflow example"""
    
    print("PE Assessment System - Complete Workflow Example")
    print("=" * 80)
    
    # Step 1: Initialize the system
    print("\n1. Initializing system...")
    system = PEAssessmentSystem(output_dir="./example_output")
    print("✓ System initialized")
    
    # Step 2: Load mark scheme
    print("\n2. Loading mark scheme...")
    # In real usage: mark_scheme = system.load_mark_scheme('path/to/markscheme.pdf')
    print("ℹ  In production, you would load: system.load_mark_scheme('markscheme.pdf')")
    print("   For this example, we'll simulate the process")
    
    # For demonstration, we'll create a mock mark scheme
    from models import MarkScheme, MarkCriteria, Topic, AssessmentObjective
    
    mock_mark_scheme = MarkScheme(
        assessment_id="PE_Paper1_2024",
        assessment_title="OCR GCSE PE Paper 1: Physical factors affecting performance",
        mark_criteria=[
            MarkCriteria(
                question_id="1a",
                max_marks=2,
                assessment_objective=AssessmentObjective.AO1,
                keywords=["aerobic", "oxygen", "energy"],
                acceptable_answers=[
                    "Uses oxygen to produce energy",
                    "Occurs in the presence of oxygen",
                    "Produces ATP with oxygen"
                ]
            ),
            MarkCriteria(
                question_id="1b",
                max_marks=3,
                assessment_objective=AssessmentObjective.AO2,
                keywords=["marathon", "endurance", "aerobic"],
                acceptable_answers=[
                    "Marathon requires sustained energy production",
                    "Aerobic system provides energy over long duration",
                    "Oxygen is readily available for prolonged exercise"
                ]
            ),
            MarkCriteria(
                question_id="2",
                max_marks=4,
                assessment_objective=AssessmentObjective.AO3,
                keywords=["smart", "specific", "measurable", "achievable"],
                acceptable_answers=[
                    "SMART targets are Specific, Measurable, Achievable, Relevant, Time-bound",
                    "Specific - clearly defined goal",
                    "Measurable - can track progress",
                    "Achievable - realistic and attainable"
                ]
            )
        ],
        topics=[
            Topic(
                name="Energy Systems",
                description="Aerobic and anaerobic energy systems",
                related_questions=["1a", "1b"],
                threshold_concept=True
            ),
            Topic(
                name="Goal Setting",
                description="SMART targets and motivation",
                related_questions=["2"],
                threshold_concept=True
            )
        ],
        total_marks=9
    )
    
    # Manually set the mark scheme
    system.mark_scheme = mock_mark_scheme
    from marking import MarkingEngine
    from feedback import FeedbackGenerator
    from analytics import ClassAnalyticsEngine
    
    system.marking_engine = MarkingEngine(mock_mark_scheme)
    system.feedback_generator = FeedbackGenerator(mock_mark_scheme)
    system.analytics_engine = ClassAnalyticsEngine(mock_mark_scheme)
    
    print("✓ Mark scheme loaded")
    print(f"  - Assessment: {mock_mark_scheme.assessment_title}")
    print(f"  - Total marks: {mock_mark_scheme.total_marks}")
    print(f"  - Questions: {len(mock_mark_scheme.mark_criteria)}")
    
    # Step 3: Create sample student answers
    print("\n3. Processing student scripts...")
    from models import StudentAnswer
    
    # Student 1 - Good performance
    student1_answers = [
        StudentAnswer(
            question_id="1a",
            answer_text="The aerobic system uses oxygen to produce energy in the body",
            student_id="S001"
        ),
        StudentAnswer(
            question_id="1b",
            answer_text="A marathon runner needs the aerobic system because it provides energy over long duration and oxygen is available",
            student_id="S001"
        ),
        StudentAnswer(
            question_id="2",
            answer_text="SMART targets are Specific so you know exactly what to achieve, Measurable so you can track progress, and Achievable so they are realistic",
            student_id="S001"
        )
    ]
    
    # Student 2 - Mixed performance with misconception
    student2_answers = [
        StudentAnswer(
            question_id="1a",
            answer_text="Aerobic means without oxygen",  # Misconception!
            student_id="S002"
        ),
        StudentAnswer(
            question_id="1b",
            answer_text="Marathon uses aerobic system for endurance",
            student_id="S002"
        ),
        StudentAnswer(
            question_id="2",
            answer_text="SMART means making easy goals",  # Misconception!
            student_id="S002"
        )
    ]
    
    # Mark the answers
    marked1 = system.marking_engine.mark_batch(student1_answers)
    marked2 = system.marking_engine.mark_batch(student2_answers)
    
    # Generate student reports
    report1 = system.feedback_generator.generate_student_report(
        "S001", "Emma Johnson", marked1
    )
    report2 = system.feedback_generator.generate_student_report(
        "S002", "Liam Brown", marked2
    )
    
    print("✓ Processed 2 student scripts")
    print(f"  - Emma Johnson: {report1.total_score}/{report1.max_possible_score} ({report1.percentage:.1f}%)")
    print(f"  - Liam Brown: {report2.total_score}/{report2.max_possible_score} ({report2.percentage:.1f}%)")
    
    # Step 4: Generate class analytics
    print("\n4. Generating class analytics...")
    analytics = system.analytics_engine.generate_class_analytics(
        "Year10_PE",
        [report1, report2]
    )
    
    print("✓ Class analytics generated")
    print(f"  - Class average: {analytics.average_score:.1f}%")
    print(f"  - Common misconceptions: {len(analytics.common_misconceptions)}")
    
    # Step 5: Display sample reports
    print("\n5. Sample Student Report:")
    print("-" * 80)
    print(system.feedback_generator.format_student_report_text(report1))
    
    print("\n6. Class Analytics Report:")
    print("-" * 80)
    print(system.analytics_engine.format_class_report_text(analytics))
    
    # Step 6: Export reports
    print("\n7. Exporting reports...")
    system.export_reports([report1, report2], analytics, format='both')
    print("✓ Reports exported to ./example_output/")
    
    print("\n" + "=" * 80)
    print("Example workflow complete!")
    print("Check ./example_output/ for generated reports")
    print("=" * 80)


if __name__ == "__main__":
    example_complete_workflow()
