"""Security utilities for GDPR compliance and data protection"""

import hashlib
import secrets
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataAnonymizer:
    """Anonymize student data for GDPR compliance"""
    
    @staticmethod
    def anonymize_student_id(student_id: str, salt: Optional[str] = None) -> str:
        """
        Create anonymized student ID using hashing
        
        Args:
            student_id: Original student ID
            salt: Optional salt for hashing (use consistent salt for same mapping)
            
        Returns:
            Anonymized student ID
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        combined = f"{student_id}{salt}"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        # Return first 12 characters as anonymized ID
        return f"ANON_{hashed[:12].upper()}"
    
    @staticmethod
    def mask_personal_info(text: str) -> str:
        """
        Mask potential personal information in text
        
        Args:
            text: Text that may contain personal info
            
        Returns:
            Text with masked personal info
        """
        # This is a simple implementation
        # In production, use more sophisticated NER (Named Entity Recognition)
        
        import re
        
        # Mask email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                     '[EMAIL]', text)
        
        # Mask phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        # Mask potential names (very basic - would need improvement)
        # This is intentionally conservative to avoid false positives
        
        return text


class SecureStorage:
    """Secure storage utilities"""
    
    @staticmethod
    def generate_secure_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password securely"""
        # In production, use bcrypt or argon2
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode(), 
                                       salt.encode(), 
                                       100000)
        return f"{salt}${pwd_hash.hex()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against a hash"""
        try:
            salt, pwd_hash = hashed.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode(), 
                                          salt.encode(), 
                                          100000)
            return new_hash.hex() == pwd_hash
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False


class AuditLogger:
    """Audit logging for compliance"""
    
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.logger = logging.getLogger('audit')
        
        # Configure audit logger
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_file_access(self, user_id: str, file_path: str, action: str):
        """Log file access for audit trail"""
        self.logger.info(f"USER:{user_id} ACTION:{action} FILE:{file_path}")
    
    def log_data_export(self, user_id: str, data_type: str, record_count: int):
        """Log data export for audit trail"""
        self.logger.info(f"USER:{user_id} EXPORT:{data_type} RECORDS:{record_count}")
    
    def log_authentication(self, user_id: str, success: bool):
        """Log authentication attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"AUTH:{status} USER:{user_id}")
