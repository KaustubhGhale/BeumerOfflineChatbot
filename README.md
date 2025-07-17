<div align="center">
  <img src="https://placehold.co/150x50/004080/ffffff?text=BEUMER+LOGO" alt="Beumer Group Logo Placeholder" style="background-color: #004080; padding: 10px; border-radius: 5px;">
  <h1>Beumer Offline Chatbot Application</h1>
  <p>
    <em>An intelligent, offline chatbot for managing airport operations data,
    built for Beumer Group internship project.</em>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
    <img src="https://img.shields.io/badge/Tkinter-GUI-lightgrey.svg?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter GUI">
    <img src="https://img.shields.io/badge/LLM-Offline-red.svg?style=for-the-badge" alt="Offline LLM">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
  </p>
</div>

---

## Overview

The **Beumer Offline Chatbot Application** is a robust, locally-runnable desktop tool designed to assist with airport database management. Developed as a proof-of-concept for a Beumer Group internship, this application allows users to query information from uploaded PDF documents (such as baggage handling systems, pipelines, and flight details) using a powerful Large Language Model (LLM) that runs entirely offline.

Beyond intelligent Q&A, the app features a dedicated interface for manually managing and editing structured flight data, ensuring comprehensive data handling capabilities.

---

## Features

* **Offline LLM Integration:** Utilizes `llama-cpp-python` to run GGUF-formatted Large Language Models (e.g., Mistral 7B) locally, ensuring privacy and no internet dependency for inference.
* **Retrieval-Augmented Generation (RAG):** Reads and processes PDF documents, creating embeddings to provide context-aware answers from the document content.
* **Manual Table Data Editor:** A dedicated page to view, add, and delete structured data (e.g., flight schedules, IATA codes), with data persistence via local JSON files.
* **Intuitive Multi-Page GUI:** Built with Tkinter, featuring a clean, responsive design with a login page, chatbot interface, table editor, and an "About Us" section.
* **Beumer Brand Theming:** Designed with a color palette and aesthetic inspired by Beumer Group's corporate branding for a consistent user experience.
* **Robust Error Handling:** Designed to provide clear feedback and prevent silent crashes during LLM loading and inference.

---

## Prerequisites

Before you begin, ensure you have the following installed on your **Windows** machine:

* **Python 3.11:** It's crucial to use Python 3.11 for compatibility with the specified libraries.
    * Download from [python.org](https://www.python.org/downloads/windows/).
* **Microsoft Visual C++ Build Tools:** Required for compiling native Python packages like `llama-cpp-python` and `faiss-cpu`.
    * Download **"Build Tools for Visual Studio 2022"** from [Visual Studio Downloads](https://visualstudio.microsoft.com/downloads/).
    * During installation, select the **"Desktop development with C++"** workload. Ensure "MSVC v143 - VS 2022 C++ x64/x86 build tools" and "Windows 10/11 SDK" are selected.
    * **Restart your computer after installation.**
* **Git:** For cloning the repository and managing versions.
    * Download from [git-scm.com](https://git-scm.com/download/win).
* **CMake:** Required for building `llama-cpp-python` from source.
    * Download from [cmake.org/download](https://cmake.org/download/). Ensure you add it to your system PATH during installation.
* **Rust Toolchain (Rustup):** Essential for compiling some underlying components of `llama-cpp-python`.
    * Download `rustup-init.exe` from [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install).
    * Run it and choose option `1` for default installation.
    * **Restart your computer after installation.**

---

## Setup Instructions

Follow these steps to get the application running on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/KaustubhGhale/BeumerChatbotApp.git](https://github.com/KaustubhGhale/BeumerChatbotApp.git)
    cd BeumerChatbotApp
    ```

2.  **Create and Activate a Python Virtual Environment:**
    Open a **new integrated terminal in VS Code** (or a standard Command Prompt/PowerShell).

    ```bash
    python -m venv venv
    ```
    *Activate the virtual environment:*
    * **PowerShell:** `.\venv\Scripts\Activate.ps1`
    * **Command Prompt:** `.\venv\Scripts\activate.bat`
    * *(Your prompt should now show `(venv)` at the beginning.)*

3.  **Install Dependencies (Crucial Step for `llama-cpp-python`):**
    This step requires compiling `llama-cpp-python` from source to ensure compatibility with your AMD Ryzen 390 AI MAX processor.

    * **Close your current VS Code terminal.**
    * Search for and open **"x64 Native Tools Command Prompt for VS 2022"** from your Windows Start Menu.
    * Navigate to your `BeumerChatbotApp` directory in this new command prompt:
        ```bash
        cd C:\Path\To\Your\BeumerChatbotApp
        ```
        (Replace `C:\Path\To\Your\BeumerChatbotApp` with your actual path).
    * **Activate your virtual environment within this command prompt:**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        (If it's a standard Command Prompt, use `.\venv\Scripts\activate.bat`)
    * **Install `llama-cpp-python` from source:**
        ```powershell
        $env:CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS -DBUILD_SHARED_LIBS=ON" ; pip install llama-cpp-python==0.2.70 --force-reinstall --no-binary llama-cpp-python
        ```
        *This step will take a considerable amount of time (10-30+ minutes) as it compiles native code. Do not interrupt it.*

    * **After `llama-cpp-python` finishes, install the remaining dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
        *This will install `pandas` and ensure all other libraries are correctly set up.*

4.  **Download Your LLM Model:**
    * Download a GGUF-formatted LLM model, such as `mistral-7b-instruct-v0.2.Q4_K_M.gguf` (recommended quantization for balance of performance and quality).
        * You can find this model here: [TheBloke/Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/tree/main)
    * Place the downloaded `.gguf` file into the `models/` directory within your `BeumerChatbotApp` project.
        * Example: `BeumerChatbotApp/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf`

---

## Usage

1.  **Run the Application:**
    From your **activated virtual environment** in the **"x64 Native Tools Command Prompt for VS 2022"** (the same one you used for installation), run:
    ```bash
    python main.py
    ```

2.  **Login Page:**
    * The application will start with a login screen.
    * **Username:** `admin`
    * **Password:** `password`
    * Click "Login" to proceed.

3.  **Chatbot Page:**
    * **Select PDF Document:** Click "Browse PDF" and choose the PDF you want the chatbot to read (e.g., your airport database document).
    * **Select LLM Model:** Click "Browse Model" and select your downloaded `.gguf` model from the `models/` folder.
    * **Initialize Chatbot:** Click this button. The status bar at the bottom will guide you through PDF text extraction, embedding creation, and LLM loading.
        * *Note: The first time embeddings are created, `sentence-transformers` will download the `all-MiniLM-L6-v2` model (approx. 100-200 MB) silently. Ensure you have an internet connection for this first-time download.*
        * *Model loading is memory-intensive and may take some time. The UI is designed to remain responsive.*
    * Once the status bar shows "Chatbot ready!", type your questions related to the PDF content into the input box and press **Enter** or click "Send".
    * The input box will clear, and the chatbot's response will appear in the chat area.

4.  **Navigation:**
    * Use the navigation buttons in the top right (`Table Editor`, `About Us`, `Logout`) to switch between different sections of the application.

5.  **Table Editor Page:**
    * This page allows you to manually add, view, and delete rows of structured data (e.g., flight numbers, destinations, IATA codes).
    * Data entered here is automatically saved to `data/flight_data.json` for persistence.
    * *Note: This is a manual editor; it does not automatically extract tables from PDFs.*

---

## ⚠️ Troubleshooting

* **Silent Crashes / App Closes Abruptly:**
    * This usually indicates a low-level issue with the LLM loading or inference. Ensure you followed the `llama-cpp-python` source build instructions precisely in the "x64 Native Tools Command Prompt for VS 2022" after installing Rust.
    * Verify your `.gguf` model file is not corrupted by redownloading it.
    * Try a smaller LLM model (e.g., `TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf`) from TheBloke's Hugging Face page to rule out model size as a factor.
* **"Error loading LLM model or initializing embeddings..."**:
    * Ensure the `.gguf` model file is in the `models/` directory and its name is typed exactly as selected.
    * Confirm `llama-cpp-python` was built from source successfully.
* **"Could not import faiss-python package"**:
    * Ensure `faiss-cpu` was installed correctly. Re-run `pip uninstall faiss-cpu` and then `pip install -r requirements.txt` from the "x64 Native Tools Command Prompt".
* **"unsupported operand type(s) for //: 'method' and 'int'"**:
    * This specific error should be resolved by the latest `core/llm_handler.py` code. Ensure you have copied the full, updated version.
* **"ModuleNotFoundError: No module named 'langchain'" (or similar for other packages):**
    * This means you are not running the application from your activated virtual environment. Always ensure `(venv)` appears in your terminal prompt before running `python main.py`.

---

## License

This project is open-source and available under the **MIT License**. This means you're free to use, modify, and distribute it for pretty much any purpose, as long as you include the original copyright and license notice. Check out the `LICENSE` file in the repository for all the details!

---

## 📧 Let's Connect!

Got questions? Need a hand with something? Or just want to chat about the project? Don't hesitate to reach out!

* **Kaustubh Ghale:** Feel free to connect on [GitHub](https://github.com/KaustubhGhale)! Your insights are always welcome.

