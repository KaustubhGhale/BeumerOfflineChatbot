import os
import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pdfplumber
from ctransformers import AutoModelForCausalLM


class PDFChatbot:
    def __init__(self):
        # Load embedding model
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_chunks = []
        self.index = None
        self.flight_text_chunks = []
        self.flight_index = None

        # Initialize DB path
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'project_data.db')

        # Load LLM (GGUF model) using ctransformers
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'mistral-7b-instruct-v0.1.Q4_K_M.gguf')
        self.llm = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="mistral",
            gpu_layers=0  # Set >0 if using GPU acceleration
        )

    def extract_text(self, pdf_path):
        all_text = ''
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + '\n'
        except Exception as e:
            print("Error reading PDF:", e)
        return all_text

    def chunk_text(self, text, max_len=500):
        sentences = text.split('. ')
        chunks = []
        chunk = ''
        for sentence in sentences:
            if len(chunk) + len(sentence) < max_len:
                chunk += sentence + '. '
            else:
                chunks.append(chunk.strip())
                chunk = sentence + '. '
        if chunk:
            chunks.append(chunk.strip())
        return chunks

    def build_pdf_index(self, pdf_path):
        text = self.extract_text(pdf_path)
        self.text_chunks = self.chunk_text(text)
        if self.text_chunks:
            embeddings = self.embed_model.encode(self.text_chunks, convert_to_numpy=True)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

    def load_flight_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT serial_no, flight_name, destination, iata FROM flights")
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()

        self.flight_text_chunks = [
            f"Flight {r[1]} with serial no {r[0]} goes to {r[2]} with IATA code {r[3]}."
            for r in rows
        ]

        if self.flight_text_chunks:
            embeddings = self.embed_model.encode(self.flight_text_chunks, convert_to_numpy=True)
            self.flight_index = faiss.IndexFlatL2(embeddings.shape[1])
            self.flight_index.add(embeddings)

    def semantic_search(self, query, top_k=3):
        query_vec = self.embed_model.encode([query], convert_to_numpy=True)
        context_pdf, context_flt = "", ""

        if self.index:
            D_pdf, I_pdf = self.index.search(query_vec, top_k)
            context_pdf = ' '.join([self.text_chunks[i] for i in I_pdf[0] if i < len(self.text_chunks)])

        if self.flight_index:
            D_flt, I_flt = self.flight_index.search(query_vec, top_k)
            context_flt = ' '.join([self.flight_text_chunks[i] for i in I_flt[0] if i < len(self.flight_text_chunks)])

        return context_pdf + "\n" + context_flt

    def generate_answer(self, context, query):
        prompt = f"""You are an intelligent assistant. Based on the following context, answer the user's question.

Context:
{context}

Question: {query}

Answer:"""
        response = self.llm(prompt, max_new_tokens=512)
        return response.strip()

    def ask(self, query):
        context = self.semantic_search(query)

        if context.strip():
            return self.generate_answer(context, query)
        else:
            # Fallback to general LLM knowledge
            prompt = f"""You are a smart and helpful assistant. Answer the following question clearly and concisely.

Question: {query}

Answer:"""
            response = self.llm(prompt, max_new_tokens=512)
            return response.strip()
