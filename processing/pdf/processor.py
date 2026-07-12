"""PDF processor - handles PDF validation, page extraction, and image conversion."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from core.constants import MAX_PDF_SIZE_MB, MAX_PDF_PAGES
from core.exceptions import PDFProcessingException
from core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class PDFMetadata:
    """Metadata extracted from a PDF file."""

    filename: str = ""
    page_count: int = 0
    file_size_mb: float = 0.0
    is_valid: bool = False
    error_message: str = ""


class PDFProcessor:
    """Handles PDF file validation, metadata extraction, and page-to-image conversion."""

    def __init__(self, max_size_mb: int = MAX_PDF_SIZE_MB, max_pages: int = MAX_PDF_PAGES):
        self._max_size_mb = max_size_mb
        self._max_pages = max_pages

    def validate_pdf(self, file_path: Path) -> PDFMetadata:
        """Validate a PDF file and extract metadata."""
        metadata = PDFMetadata(filename=file_path.name)

        if not file_path.exists():
            metadata.error_message = "File does not exist."
            return metadata

        if not file_path.suffix.lower() == ".pdf":
            metadata.error_message = "File is not a PDF."
            return metadata

        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        metadata.file_size_mb = round(file_size_mb, 2)

        if file_size_mb > self._max_size_mb:
            metadata.error_message = f"File exceeds maximum size of {self._max_size_mb} MB."
            return metadata

        try:
            page_count = self.get_page_count(file_path)
            metadata.page_count = page_count
            if page_count > self._max_pages:
                metadata.error_message = f"PDF has {page_count} pages, exceeds limit of {self._max_pages}."
                return metadata
        except Exception as e:
            metadata.error_message = f"Cannot read PDF: {e}"
            return metadata

        metadata.is_valid = True
        logger.info(f"PDF validated: {file_path.name} ({metadata.file_size_mb} MB, {metadata.page_count} pages)")
        return metadata

    def extract_pages_as_images(self, file_path: Path, dpi: int = 300) -> list[Path]:
        """Convert PDF pages to images for OCR processing."""
        from pdf2image import convert_from_path

        metadata = self.validate_pdf(file_path)
        if not metadata.is_valid:
            raise PDFProcessingException(metadata.error_message)

        images = convert_from_path(str(file_path), dpi=dpi)
        image_paths: list[Path] = []

        for idx, img in enumerate(images):
            tmp = tempfile.NamedTemporaryFile(suffix=f"_page_{idx+1}.png", delete=False)
            img.save(tmp.name, "PNG")
            image_paths.append(Path(tmp.name))
            tmp.close()

        logger.info(f"Extracted {len(image_paths)} page images from {file_path.name}")
        return image_paths

    def get_page_count(self, file_path: Path) -> int:
        """Get the number of pages in a PDF."""
        import PyPDF2

        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages)

    def save_uploaded_file(self, file_bytes: bytes, filename: str) -> Path:
        """Save uploaded bytes to a temporary file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, prefix=f"{filename}_")
        tmp.write(file_bytes)
        tmp.close()
        return Path(tmp.name)
