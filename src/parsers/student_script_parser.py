"""Student script parser for extracting answers from PDF uploads"""

import re
from typing import List, Dict, Optional
from pathlib import Path
import logging

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

from models.data_models import StudentAnswer

logger = logging.getLogger(__name__)


class StudentScriptParser:
    """Parser for student answer scripts in PDF format"""
    
    def __init__(self):
        self.question_patterns = [
            r'(?:Question|Q)\s*(\d+[a-z]?)',
            r'^(\d+[a-z]?)[\.\)]\s',
            r'Question\s+(\d+[a-z]?)\s*:',
        ]
    
    def parse_script(self, file_path: str, student_id: str) -> List[StudentAnswer]:
        """Parse a student's answer script"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() != '.pdf':
            raise ValueError(f"Only PDF format is supported for student scripts")
        
        return self._extract_answers_from_pdf(file_path, student_id)
    
    def _extract_answers_from_pdf(self, file_path: str, student_id: str) -> List[StudentAnswer]:
        """Extract student answers from PDF"""
        if pdfplumber is None:
            raise ImportError("pdfplumber is required. Install with: pip install pdfplumber")
        
        text_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise
        
        full_text = "\n".join(text_content)
        return self._segment_answers(full_text, student_id)
    
    def _segment_answers(self, text: str, student_id: str) -> List[StudentAnswer]:
        """Segment text into individual question answers"""
        answers = []
        lines = text.split('\n')
        
        current_question = None
        current_answer_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line starts a new question
            question_found = False
            for pattern in self.question_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous answer if exists
                    if current_question and current_answer_lines:
                        answer_text = ' '.join(current_answer_lines).strip()
                        if answer_text:
                            answers.append(StudentAnswer(
                                question_id=current_question,
                                answer_text=answer_text,
                                student_id=student_id
                            ))
                    
                    # Start new question
                    current_question = match.group(1)
                    current_answer_lines = []
                    
                    # Include rest of line after question number
                    rest_of_line = line[match.end():].strip()
                    if rest_of_line and not rest_of_line.startswith(':'):
                        current_answer_lines.append(rest_of_line)
                    
                    question_found = True
                    break
            
            # If not a new question, add to current answer
            if not question_found and current_question:
                current_answer_lines.append(line)
        
        # Add last answer
        if current_question and current_answer_lines:
            answer_text = ' '.join(current_answer_lines).strip()
            if answer_text:
                answers.append(StudentAnswer(
                    question_id=current_question,
                    answer_text=answer_text,
                    student_id=student_id
                ))
        
        return answers
    
    def parse_batch(self, file_paths: List[str], student_ids: List[str]) -> Dict[str, List[StudentAnswer]]:
        """Parse multiple student scripts in batch"""
        if len(file_paths) != len(student_ids):
            raise ValueError("Number of files must match number of student IDs")
        
        results = {}
        
        for file_path, student_id in zip(file_paths, student_ids):
            try:
                answers = self.parse_script(file_path, student_id)
                results[student_id] = answers
                logger.info(f"Successfully parsed script for student {student_id}")
            except Exception as e:
                logger.error(f"Error parsing script for student {student_id}: {e}")
                results[student_id] = []
        
        return results
