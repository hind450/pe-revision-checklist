"""Mark scheme parser for PDF and DOCX files"""

import re
from typing import List, Dict, Optional
from pathlib import Path
import logging

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    PyPDF2 = None
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None

from models.data_models import MarkScheme, MarkCriteria, Topic, AssessmentObjective

logger = logging.getLogger(__name__)


class MarkSchemeParser:
    """Parser for mark schemes in PDF and DOCX format"""
    
    def __init__(self):
        self.ao_keywords = {
            'AO1': ['knowledge', 'recall', 'describe', 'state', 'identify', 'define', 'name'],
            'AO2': ['application', 'apply', 'explain', 'demonstrate', 'use', 'calculate'],
            'AO3': ['evaluation', 'evaluate', 'analyse', 'assess', 'justify', 'compare', 'discuss']
        }
    
    def parse_file(self, file_path: str) -> MarkScheme:
        """Parse a mark scheme file (PDF or DOCX)"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() == '.pdf':
            return self.parse_pdf(file_path)
        elif path.suffix.lower() in ['.docx', '.doc']:
            return self.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def parse_pdf(self, file_path: str) -> MarkScheme:
        """Parse PDF mark scheme"""
        if pdfplumber is None:
            raise ImportError("pdfplumber is required for PDF parsing. Install with: pip install pdfplumber")
        
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
        return self._extract_mark_scheme(full_text, Path(file_path).stem)
    
    def parse_docx(self, file_path: str) -> MarkScheme:
        """Parse DOCX mark scheme"""
        if Document is None:
            raise ImportError("python-docx is required for DOCX parsing. Install with: pip install python-docx")
        
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            full_text = "\n".join(paragraphs)
        except Exception as e:
            logger.error(f"Error parsing DOCX: {e}")
            raise
        
        return self._extract_mark_scheme(full_text, Path(file_path).stem)
    
    def _extract_mark_scheme(self, text: str, assessment_id: str) -> MarkScheme:
        """Extract mark scheme structure from text"""
        # Extract title
        lines = text.split('\n')
        title = lines[0] if lines else "Untitled Assessment"
        
        # Extract mark criteria
        mark_criteria = self._extract_mark_criteria(text)
        
        # Extract topics
        topics = self._extract_topics(text)
        
        # Extract examiner comments
        examiner_comments = self._extract_examiner_comments(text)
        
        # Calculate total marks
        total_marks = sum(criteria.max_marks for criteria in mark_criteria)
        
        return MarkScheme(
            assessment_id=assessment_id,
            assessment_title=title.strip(),
            mark_criteria=mark_criteria,
            topics=topics,
            examiner_comments=examiner_comments,
            total_marks=total_marks
        )
    
    def _extract_mark_criteria(self, text: str) -> List[MarkCriteria]:
        """Extract marking criteria from text"""
        criteria_list = []
        
        # Pattern to match questions: Q1, Question 1, 1., etc.
        question_pattern = r'(?:Question|Q)\s*(\d+[a-z]?)|^(\d+[a-z]?)[\.\)]\s'
        
        # Pattern to match marks: [3 marks], (3), 3 marks
        marks_pattern = r'\[(\d+)\s*marks?\]|\((\d+)\s*marks?\)|(\d+)\s*marks?'
        
        lines = text.split('\n')
        current_question = None
        current_marks = 0
        current_ao = AssessmentObjective.AO1
        acceptable_answers = []
        keywords = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for question number
            q_match = re.search(question_pattern, line, re.IGNORECASE)
            if q_match:
                # Save previous question if exists
                if current_question and acceptable_answers:
                    criteria_list.append(MarkCriteria(
                        question_id=current_question,
                        max_marks=current_marks,
                        assessment_objective=current_ao,
                        keywords=keywords,
                        acceptable_answers=acceptable_answers
                    ))
                
                # Start new question
                current_question = q_match.group(1) or q_match.group(2)
                acceptable_answers = []
                keywords = []
                
                # Check for marks in same line
                marks_match = re.search(marks_pattern, line)
                if marks_match:
                    current_marks = int(next(g for g in marks_match.groups() if g))
                else:
                    current_marks = 1  # Default
                
                # Determine AO
                current_ao = self._determine_ao(line)
            
            # Extract acceptable answers (bullet points, numbered lists, etc.)
            if current_question and (line.startswith('•') or line.startswith('-') or 
                                    line.startswith('*') or re.match(r'^\d+[\.\)]', line)):
                answer = re.sub(r'^[•\-\*\d\.\)]\s*', '', line).strip()
                if answer and len(answer) > 3:
                    acceptable_answers.append(answer)
                    # Extract keywords
                    words = answer.lower().split()
                    keywords.extend([w for w in words if len(w) > 4])
        
        # Add last question
        if current_question and acceptable_answers:
            criteria_list.append(MarkCriteria(
                question_id=current_question,
                max_marks=current_marks,
                assessment_objective=current_ao,
                keywords=list(set(keywords)),
                acceptable_answers=acceptable_answers
            ))
        
        return criteria_list
    
    def _determine_ao(self, text: str) -> AssessmentObjective:
        """Determine assessment objective from text"""
        text_lower = text.lower()
        
        # Count keyword matches for each AO
        ao_scores = {}
        for ao, keywords in self.ao_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            ao_scores[ao] = score
        
        # Return AO with highest score
        if ao_scores['AO3'] > 0:
            return AssessmentObjective.AO3
        elif ao_scores['AO2'] > 0:
            return AssessmentObjective.AO2
        else:
            return AssessmentObjective.AO1
    
    def _extract_topics(self, text: str) -> List[Topic]:
        """Extract topics from mark scheme"""
        # Common PE GCSE topics
        pe_topics = [
            "Energy Systems", "Aerobic System", "Anaerobic System",
            "Skeletal System", "Muscular System", "Cardiovascular System",
            "Respiratory System", "Movement Analysis", "Levers",
            "Planes and Axes", "Fitness Components", "Training Methods",
            "Principles of Training", "Goal Setting", "SMART Targets",
            "Motivation", "Sports Psychology", "Skill Acquisition",
            "Feedback", "Guidance", "Mental Preparation",
            "Diet and Nutrition", "Health and Wellbeing"
        ]
        
        topics = []
        text_lower = text.lower()
        
        for topic in pe_topics:
            if topic.lower() in text_lower:
                topics.append(Topic(
                    name=topic,
                    description=f"GCSE PE topic: {topic}",
                    threshold_concept=(topic in ["Energy Systems", "Levers", "SMART Targets"])
                ))
        
        return topics
    
    def _extract_examiner_comments(self, text: str) -> Optional[str]:
        """Extract examiner comments section"""
        # Look for examiner comments section
        patterns = [
            r'examiner comments?:(.+?)(?=\n\n|\Z)',
            r'chief examiner report:(.+?)(?=\n\n|\Z)',
            r'examiner\'s report:(.+?)(?=\n\n|\Z)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
