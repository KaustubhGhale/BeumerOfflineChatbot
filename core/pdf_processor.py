# core/pdf_processor.py
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings # Keep this import
import os

class PDFProcessor:
    """
    Handles PDF document processing, including text extraction,
    chunking, and creating vector embeddings for RAG.
    This version explicitly uses SentenceTransformerEmbeddings for robustness.
    """
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, # Size of text chunks
            chunk_overlap=200, # Overlap between chunks for context
            length_function=len,
            add_start_index=True,
        )
        # EXPLICITLY INITIALIZE SENTENCETRANSFORMEREMBEDDINGS HERE
        # This ensures a consistent and reliable embedding model.
        self.embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        print("PDFProcessor initialized with SentenceTransformerEmbeddings.")
        self.embeddings_store = None # FAISS vector store

    # The set_embeddings_model method is no longer needed and is removed.
    # The _ensure_embeddings_model method is no longer needed and is removed.

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts all text from a given PDF file.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF document not found at: {pdf_path}")

        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() or ""
            print(f"Successfully extracted text from {pdf_path}")
            return text
        except Exception as e:
            raise RuntimeError(f"Error extracting text from PDF: {e}") from e

    def create_embeddings(self, document_text: str):
        """
        Splits the document text into chunks and creates embeddings,
        storing them in a FAISS vector store.
        """
        if not document_text:
            raise ValueError("Document text is empty. Cannot create embeddings.")

        # No need to call _ensure_embeddings_model() here anymore as it's always set in __init__

        print("Splitting text into chunks...")
        texts = self.text_splitter.split_text(document_text)
        print(f"Created {len(texts)} text chunks.")

        if not texts:
            raise ValueError("No text chunks were created from the document.")

        print("Creating embeddings and building FAISS vector store... (This may take time)")
        try:
            self.embeddings_store = FAISS.from_texts(texts, self.embeddings_model)
            print("FAISS embeddings store created successfully.")
        except Exception as e:
            error_msg = f"Error creating embeddings or FAISS store: {e}"
            print(error_msg)
            error_msg += "\nTip: Ensure 'all-MiniLM-L6-v2' model downloaded correctly by SentenceTransformer. Check internet connection for first download."
            raise RuntimeError(error_msg) from e

