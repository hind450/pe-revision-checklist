"""
PE Assessment System - Main Application
Automated marking and feedback system for GCSE PE assessments
"""

import logging
from pathlib import Path
from typing import List, Optional
import sys

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))

try:
    from parsers import MarkSchemeParser, StudentScriptParser
    from marking import MarkingEngine
    from feedback import FeedbackGenerator
    from analytics import ClassAnalyticsEngine
    from utils import ExportManager, FileValidator, AuditLogger
    from models import (
        MarkScheme, StudentAnswer, MarkedAnswer, 
        StudentReport, ClassAnalytics
    )
except ImportError:
    # Try relative imports (when used as package)
    from .parsers import MarkSchemeParser, StudentScriptParser
    from .marking import MarkingEngine
    from .feedback import FeedbackGenerator
    from .analytics import ClassAnalyticsEngine
    from .utils import ExportManager, FileValidator, AuditLogger
    from .models import (
        MarkScheme, StudentAnswer, MarkedAnswer, 
        StudentReport, ClassAnalytics
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class PEAssessmentSystem:
    """
    Main system for PE assessment marking and feedback
    
    This system provides:
    - Automated marking aligned to mark schemes
    - Individual student feedback with actionable next steps
    - Class-level analytics and teaching recommendations
    - GDPR-compliant data handling
    """
    
    def __init__(
        self,
        output_dir: str = "./output",
        enable_audit: bool = True
    ):
        """
        Initialize the PE Assessment System
        
        Args:
            output_dir: Directory for output files
            enable_audit: Enable audit logging for compliance
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.mark_scheme_parser = MarkSchemeParser()
        self.student_parser = StudentScriptParser()
        self.export_manager = ExportManager()
        self.file_validator = FileValidator()
        
        self.mark_scheme: Optional[MarkScheme] = None
        self.marking_engine: Optional[MarkingEngine] = None
        self.feedback_generator: Optional[FeedbackGenerator] = None
        self.analytics_engine: Optional[ClassAnalyticsEngine] = None
        
        if enable_audit:
            self.audit_logger = AuditLogger(str(self.output_dir / "audit.log"))
        else:
            self.audit_logger = None
        
        logger.info("PE Assessment System initialized")
    
    def load_mark_scheme(self, file_path: str) -> MarkScheme:
        """
        Load and parse mark scheme
        
        Args:
            file_path: Path to mark scheme PDF or DOCX
            
        Returns:
            Parsed MarkScheme object
        """
        logger.info(f"Loading mark scheme from: {file_path}")
        
        if not self.file_validator.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        self.mark_scheme = self.mark_scheme_parser.parse_file(file_path)
        
        # Initialize engines with mark scheme
        self.marking_engine = MarkingEngine(self.mark_scheme)
        self.feedback_generator = FeedbackGenerator(self.mark_scheme)
        self.analytics_engine = ClassAnalyticsEngine(self.mark_scheme)
        
        logger.info(f"Mark scheme loaded: {self.mark_scheme.assessment_title}")
        logger.info(f"Total marks: {self.mark_scheme.total_marks}")
        logger.info(f"Number of questions: {len(self.mark_scheme.mark_criteria)}")
        
        if self.audit_logger:
            self.audit_logger.log_file_access("system", file_path, "LOAD_MARKSCHEME")
        
        return self.mark_scheme
    
    def process_student_script(
        self,
        file_path: str,
        student_id: str,
        student_name: Optional[str] = None
    ) -> StudentReport:
        """
        Process a single student script and generate report
        
        Args:
            file_path: Path to student script PDF
            student_id: Student identifier
            student_name: Student name (optional)
            
        Returns:
            StudentReport with marks and feedback
        """
        if not self.marking_engine:
            raise RuntimeError("Mark scheme not loaded. Call load_mark_scheme() first.")
        
        logger.info(f"Processing student script: {student_id}")
        
        if not self.file_validator.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        # Parse student answers
        student_answers = self.student_parser.parse_script(file_path, student_id)
        logger.info(f"Extracted {len(student_answers)} answers")
        
        # Mark answers
        marked_answers = self.marking_engine.mark_batch(student_answers)
        logger.info(f"Marked {len(marked_answers)} answers")
        
        # Generate report
        report = self.feedback_generator.generate_student_report(
            student_id,
            student_name or student_id,
            marked_answers
        )
        
        logger.info(f"Student {student_id} score: {report.total_score}/{report.max_possible_score} ({report.percentage:.1f}%)")
        
        if self.audit_logger:
            self.audit_logger.log_file_access(student_id, file_path, "PROCESS_SCRIPT")
        
        return report
    
    def process_batch(
        self,
        file_paths: List[str],
        student_ids: List[str],
        student_names: Optional[List[str]] = None
    ) -> List[StudentReport]:
        """
        Process multiple student scripts in batch
        
        Args:
            file_paths: List of paths to student script PDFs
            student_ids: List of student identifiers
            student_names: Optional list of student names
            
        Returns:
            List of StudentReport objects
        """
        if len(file_paths) != len(student_ids):
            raise ValueError("Number of files must match number of student IDs")
        
        if student_names and len(student_names) != len(student_ids):
            raise ValueError("Number of names must match number of student IDs")
        
        logger.info(f"Processing batch of {len(file_paths)} student scripts")
        
        reports = []
        for i, (file_path, student_id) in enumerate(zip(file_paths, student_ids)):
            try:
                name = student_names[i] if student_names else None
                report = self.process_student_script(file_path, student_id, name)
                reports.append(report)
            except Exception as e:
                logger.error(f"Error processing {student_id}: {e}")
        
        logger.info(f"Successfully processed {len(reports)}/{len(file_paths)} scripts")
        
        return reports
    
    def generate_class_analytics(
        self,
        class_id: str,
        student_reports: List[StudentReport]
    ) -> ClassAnalytics:
        """
        Generate class-level analytics
        
        Args:
            class_id: Class identifier
            student_reports: List of student reports
            
        Returns:
            ClassAnalytics with aggregated insights
        """
        if not self.analytics_engine:
            raise RuntimeError("Mark scheme not loaded. Call load_mark_scheme() first.")
        
        logger.info(f"Generating analytics for class: {class_id}")
        
        analytics = self.analytics_engine.generate_class_analytics(
            class_id,
            student_reports
        )
        
        logger.info(f"Class {class_id} average: {analytics.average_score:.1f}%")
        
        return analytics
    
    def export_reports(
        self,
        student_reports: List[StudentReport],
        class_analytics: Optional[ClassAnalytics] = None,
        format: str = "both"  # "text", "csv", or "both"
    ):
        """
        Export reports to files
        
        Args:
            student_reports: List of student reports to export
            class_analytics: Optional class analytics to export
            format: Export format ("text", "csv", or "both")
        """
        logger.info(f"Exporting {len(student_reports)} student reports")
        
        # Export individual student reports
        for report in student_reports:
            if format in ["text", "both"]:
                text_path = self.output_dir / f"student_{report.student_id}_report.txt"
                text = self.feedback_generator.format_student_report_text(report)
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"Exported text report: {text_path}")
            
            if format in ["csv", "both"]:
                csv_path = self.output_dir / f"student_{report.student_id}_report.csv"
                self.export_manager.export_student_report_csv(report, str(csv_path))
        
        # Export student summary list
        if format in ["csv", "both"]:
            summary_path = self.output_dir / "class_student_summary.csv"
            self.export_manager.export_student_list_csv(student_reports, str(summary_path))
            logger.info(f"Exported student summary: {summary_path}")
        
        # Export class analytics
        if class_analytics:
            if format in ["text", "both"]:
                text_path = self.output_dir / f"class_{class_analytics.class_id}_analytics.txt"
                text = self.analytics_engine.format_class_report_text(class_analytics)
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"Exported class analytics text: {text_path}")
            
            if format in ["csv", "both"]:
                csv_path = self.output_dir / f"class_{class_analytics.class_id}_analytics.csv"
                self.export_manager.export_class_analytics_csv(class_analytics, str(csv_path))
                logger.info(f"Exported class analytics CSV: {csv_path}")
        
        if self.audit_logger:
            self.audit_logger.log_data_export(
                "system",
                "student_reports",
                len(student_reports)
            )
        
        logger.info("Export complete")


def main():
    """Example usage of the PE Assessment System"""
    
    print("=" * 80)
    print("PE Assessment for Learning System")
    print("OCR GCSE PE Automated Marking and Feedback")
    print("=" * 80)
    print()
    
    # Initialize system
    system = PEAssessmentSystem(output_dir="./output")
    
    print("System initialized successfully!")
    print()
    print("Usage Example:")
    print("-" * 80)
    print("""
# 1. Load mark scheme
mark_scheme = system.load_mark_scheme('path/to/markscheme.pdf')

# 2. Process student scripts
reports = system.process_batch(
    file_paths=['student1.pdf', 'student2.pdf'],
    student_ids=['S001', 'S002'],
    student_names=['John Doe', 'Jane Smith']
)

# 3. Generate class analytics
analytics = system.generate_class_analytics('Class10A', reports)

# 4. Export reports
system.export_reports(reports, analytics, format='both')
""")
    print("-" * 80)
    print()
    print("For more information, see the documentation in /examples")
    print()


if __name__ == "__main__":
    main()
