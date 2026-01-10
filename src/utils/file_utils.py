"""Utility functions for file handling and data export"""

import csv
from typing import List, Dict
from pathlib import Path
import logging

from models.data_models import StudentReport, ClassAnalytics

logger = logging.getLogger(__name__)


class ExportManager:
    """Handle export of reports to various formats"""
    
    def export_student_report_csv(
        self,
        report: StudentReport,
        output_path: str
    ) -> None:
        """Export student report to CSV"""
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Student Report'])
            writer.writerow(['Student ID', report.student_id])
            writer.writerow(['Student Name', report.student_name])
            writer.writerow(['Total Score', f"{report.total_score}/{report.max_possible_score}"])
            writer.writerow(['Percentage', f"{report.percentage:.1f}%"])
            writer.writerow([])
            
            # Question details
            writer.writerow(['Question', 'Marks', 'Max Marks', 'AO', 'Feedback'])
            for answer in report.marked_answers:
                writer.writerow([
                    answer.question_id,
                    answer.marks_awarded,
                    answer.max_marks,
                    answer.assessment_objective.value,
                    answer.feedback
                ])
            
            writer.writerow([])
            
            # Next steps
            writer.writerow(['Priority Next Steps'])
            for step in report.priority_next_steps:
                writer.writerow([step])
        
        logger.info(f"Exported student report to {output_path}")
    
    def export_class_analytics_csv(
        self,
        analytics: ClassAnalytics,
        output_path: str
    ) -> None:
        """Export class analytics to CSV"""
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Class Analytics Report'])
            writer.writerow(['Class ID', analytics.class_id])
            writer.writerow(['Number of Students', len(analytics.student_reports)])
            writer.writerow(['Average Score', f"{analytics.average_score:.1f}%"])
            writer.writerow([])
            
            # Question performance
            writer.writerow(['Question Performance'])
            writer.writerow(['Question', 'Percentage Correct'])
            for question_id, percentage in sorted(analytics.question_performance.items()):
                writer.writerow([question_id, f"{percentage:.1f}%"])
            
            writer.writerow([])
            
            # Topic performance
            writer.writerow(['Topic Performance'])
            writer.writerow(['Topic', 'Percentage'])
            for topic, percentage in sorted(analytics.topic_performance.items()):
                writer.writerow([topic, f"{percentage:.1f}%"])
            
            writer.writerow([])
            
            # Common misconceptions
            writer.writerow(['Common Misconceptions'])
            writer.writerow(['Misconception', 'Student Count'])
            for misconception, count in analytics.common_misconceptions:
                writer.writerow([misconception, count])
            
            writer.writerow([])
            
            # Teaching recommendations
            writer.writerow(['Teaching Recommendations'])
            for recommendation in analytics.teaching_recommendations:
                writer.writerow([recommendation])
        
        logger.info(f"Exported class analytics to {output_path}")
    
    def export_student_list_csv(
        self,
        reports: List[StudentReport],
        output_path: str
    ) -> None:
        """Export summary list of all students to CSV"""
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Student ID', 'Student Name', 'Total Score', 
                'Max Score', 'Percentage', 'Red Topics', 'Amber Topics', 'Green Topics'
            ])
            
            # Student rows
            for report in reports:
                from models.data_models import PerformanceLevel
                
                red = sum(1 for level in report.traffic_light_by_topic.values() 
                         if level == PerformanceLevel.LOW)
                amber = sum(1 for level in report.traffic_light_by_topic.values() 
                           if level == PerformanceLevel.MEDIUM)
                green = sum(1 for level in report.traffic_light_by_topic.values() 
                           if level == PerformanceLevel.HIGH)
                
                writer.writerow([
                    report.student_id,
                    report.student_name,
                    report.total_score,
                    report.max_possible_score,
                    f"{report.percentage:.1f}%",
                    red,
                    amber,
                    green
                ])
        
        logger.info(f"Exported student list to {output_path}")


class FileValidator:
    """Validate uploaded files"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        """Validate a file for processing"""
        path = Path(file_path)
        
        # Check exists
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        # Check extension
        if path.suffix.lower() not in FileValidator.ALLOWED_EXTENSIONS:
            logger.error(f"Unsupported file extension: {path.suffix}")
            return False
        
        # Check size
        if path.stat().st_size > FileValidator.MAX_FILE_SIZE:
            logger.error(f"File too large: {path.stat().st_size} bytes")
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize a filename for security"""
        # Remove path components
        filename = Path(filename).name
        
        # Remove dangerous characters
        safe_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._- ')
        sanitized = ''.join(c if c in safe_chars else '_' for c in filename)
        
        return sanitized
