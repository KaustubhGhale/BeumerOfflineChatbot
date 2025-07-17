# core/llm_handler.py
import os
from llama_cpp import Llama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS # Still using FAISS for vector store

class LLMHandler:
    """
    Handles the loading and inference of the Large Language Model using llama-cpp-python.
    Also integrates with LangChain for RAG capabilities.
    """
    def __init__(self):
        self.llm = None
        self.qa_chain = None
        self.pdf_processor = None # Link to PDFProcessor instance

        # Define a standard prompt template for RAG
        self.prompt_template = PromptTemplate(
            template="""Use the following pieces of context to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}

            Question: {question}
            Answer:""",
            input_variables=["context", "question"]
        )

    def load_model(self, model_path: str, config: dict):
        """
        Loads the LLM model using llama-cpp-python.

        Args:
            model_path (str): Path to the GGUF model file.
            config (dict): Configuration dictionary for Llama.
                           Example: {'n_ctx': 4096, 'n_batch': 512, 'n_threads': 8, 'n_gpu_layers': 0}
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"LLM model not found at: {model_path}")

        print(f"Attempting to load LLM model from: {model_path} with config: {config}")
        try:
            self.llm = Llama(
                model_path=model_path,
                **config # Unpack the config dictionary
            )
            print("LLM model loaded successfully with llama-cpp-python.")

        except Exception as e:
            error_msg = f"Error loading LLM model with llama-cpp-python: {e}" # Simplified error message
            print(error_msg)
            # Provide more specific guidance for common llama-cpp-python errors
            if "out of memory" in str(e).lower() or "bad allocation" in str(e).lower():
                error_msg += "\nTip: The model might be too large for your available RAM/VRAM. Try a smaller model or ensure 'n_gpu_layers' is 0."
            elif "failed to load model" in str(e).lower() or "invalid model file" in str(e).lower():
                error_msg += "\nTip: Check if the model file is corrupted or if it's a valid GGUF file."
            elif "unknown model type" in str(e).lower():
                 error_msg += "\nTip: Ensure the GGUF model is compatible with your llama-cpp-python version."
            raise RuntimeError(error_msg) from e

    def set_pdf_processor(self, processor):
        """
        Sets the PDF processor instance for retrieving document context.
        """
        self.pdf_processor = processor


    def get_response(self, query: str) -> str:
        """
        Generates a response to the user's query, using PDF context if available.

        Args:
            query (str): The user's question.

        Returns:
            str: The chatbot's generated response.
        """
        if not self.llm:
            raise RuntimeError("LLM model not loaded. Please initialize the chatbot first.")

        if self.pdf_processor and self.pdf_processor.embeddings_store:
            # Use RAG if PDF context is available
            print("Retrieving context from PDF...")
            retriever = self.pdf_processor.embeddings_store.as_retriever()

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": self.prompt_template},
                return_source_documents=False
            )
            try:
                response = self.qa_chain.invoke({"query": query})
                return response.get("result", "Could not generate a response.")
            except Exception as e:
                error_msg = f"Error during RAG response generation: {e}"
                print(error_msg)
                if "out of memory" in str(e).lower():
                    error_msg += "\nTip: Model might be running out of memory during inference. Try a shorter query or reduce context window."
                raise RuntimeError(error_msg) from e
        else:
            # Direct LLM inference if no PDF context
            print("No PDF context available. Answering directly with LLM.")
            try:
                direct_prompt = f"Question: {query}\nAnswer:"
                
                # Default max_tokens if n_ctx is not available or not an int
                max_tokens_to_generate = 512 # A reasonable default

                if hasattr(self.llm, 'n_ctx') and isinstance(self.llm.n_ctx, int):
                    max_tokens_to_generate = self.llm.n_ctx // 2
                elif callable(getattr(self.llm, 'n_ctx', None)): # Check if it's a callable method
                    try:
                        max_tokens_to_generate = self.llm.n_ctx() // 2 # Call it if it's a method
                    except TypeError:
                        print("Warning: self.llm.n_ctx is a method but returned unexpected type. Using default max_tokens.")
                else:
                    print("Warning: self.llm.n_ctx is not an integer attribute or a callable method. Using default max_tokens.")


                output = self.llm.create_completion(
                    prompt=direct_prompt,
                    max_tokens=max_tokens_to_generate, # Use the determined max_tokens
                    temperature=0.7,
                    stop=["\nQuestion:", "\nUser:"], # Stop sequences
                    stream=False # No streaming for this direct call
                )
                return output['choices'][0]['text'].strip()
            except Exception as e:
                error_msg = f"Error during direct LLM response generation: {e}"
                print(error_msg)
                raise RuntimeError(error_msg) from e

