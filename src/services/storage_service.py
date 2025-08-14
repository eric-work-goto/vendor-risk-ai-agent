"""
Storage Service for managing document files and data persistence
"""

import os
import asyncio
from typing import Optional, List, Dict, Any
from pathlib import Path

from ..config.settings import settings


class StorageService:
    """Service for handling file storage and document management"""
    
    def __init__(self):
        self.base_path = Path(settings.document_storage_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.base_path / "documents").mkdir(exist_ok=True)
        (self.base_path / "temp").mkdir(exist_ok=True)
        (self.base_path / "processed").mkdir(exist_ok=True)
    
    async def save_document(self, filename: str, content: bytes) -> str:
        """
        Save document content to storage
        
        Args:
            filename: Name of the file to save
            content: File content as bytes
            
        Returns:
            Full path to the saved file
        """
        file_path = self.base_path / "documents" / filename
        
        # Write file asynchronously
        async with asyncio.to_thread(open, file_path, 'wb') as f:
            await asyncio.to_thread(f.write, content)
        
        return str(file_path)
    
    async def read_document(self, file_path: str) -> Optional[bytes]:
        """
        Read document content from storage
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as bytes, or None if file doesn't exist
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            async with asyncio.to_thread(open, path, 'rb') as f:
                return await asyncio.to_thread(f.read)
        except Exception:
            return None
    
    def get_document_path(self, vendor_id: int, document_hash: str, extension: str = ".pdf") -> str:
        """Generate standardized document path"""
        filename = f"vendor_{vendor_id}_{document_hash}{extension}"
        return str(self.base_path / "documents" / filename)
    
    def list_vendor_documents(self, vendor_id: int) -> List[str]:
        """List all documents for a specific vendor"""
        pattern = f"vendor_{vendor_id}_*"
        document_dir = self.base_path / "documents"
        
        matching_files = []
        for file_path in document_dir.glob(pattern):
            if file_path.is_file():
                matching_files.append(str(file_path))
        
        return matching_files
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """Clean up temporary files older than specified hours"""
        import time
        
        temp_dir = self.base_path / "temp"
        current_time = time.time()
        deleted_count = 0
        
        for file_path in temp_dir.iterdir():
            if file_path.is_file():
                file_age_hours = (current_time - file_path.stat().st_mtime) / 3600
                if file_age_hours > max_age_hours:
                    file_path.unlink()
                    deleted_count += 1
        
        return deleted_count
