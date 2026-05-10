#  GitaGPT: Inner Peace Edition

A Streamlit-powered conversational AI that offers philosophical guidance and a space for reflection based on the timeless wisdom of the Bhagavad Gita.

##  Demo Video

🔗 [Click here to watch the GitaGPT demo video](https://drive.google.com/file/d/1MThcY_Ok7jIbBLl1tfDeY8AurlMMwyHL/view?usp=sharing)



---

##  About The Project

In our fast-paced world, finding a moment for deep reflection can be challenging. GitaGPT was created to bridge the gap between ancient spiritual philosophy and modern technology. It's not just a Q&A bot; it's designed to be a compassionate, spiritual guide.

Instead of providing simple, direct answers, GitaGPT uses the wisdom of the Bhagavad Gita to offer philosophical insights, helping users explore complex questions about life, purpose, struggle, and inner peace in a calm, reflective manner.

The AI is powered by a custom **Retrieval-Augmented Generation (RAG)** pipeline, ensuring that every response is grounded in the scripture's actual teachings.

###  Key Features

- **Conversational AI Interface:** A clean, simple, and interactive chat interface built with Streamlit.
- **Wisdom from the Gita:** Answers questions using a RAG pipeline to find and interpret relevant verses.
- **110+ Verse Knowledge Base:** The AI's wisdom is sourced from a curated, copyright-free dataset of over 110 of the most significant verses from the Bhagavad Gita.
- **Multilingual Verse Display:** Includes a sidebar toggle to display the original **Sanskrit** and its **Telugu translation** for any retrieved verse, making the core wisdom more accessible.
- **Empathetic Persona:** The AI is designed to be calm, empathetic, and spiritual, avoiding a preachy or robotic tone.

---

##  Tech Stack & Architecture

This project was built using a 100% open-source, Python-based stack, allowing it to run entirely on a local machine.

- **Frontend:** **Streamlit**
- **LLM:** **Gemma:2b** (served locally via **Ollama**)
- **Embedding Model:** **TensorFlow & TensorFlow Hub** (`universal-sentence-encoder`)
- **Vector Database:** **ChromaDB**
- **Core Architecture:** Retrieval-Augmented Generation (RAG)

The RAG pipeline works as follows:
1.  A user's query is converted into a numerical vector (embedding) using the TensorFlow model.
2.  ChromaDB performs a semantic search to find the most philosophically similar verse in the knowledge base.
3.  The user's query and the retrieved verse are combined into a detailed prompt.
4.  This augmented prompt is sent to the Gemma LLM to generate a thoughtful, context-aware response.

---

##  Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running on your system.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/GitaGPT.git](https://github.com/your-username/GitaGPT.git)
    cd GitaGPT
    ```

2.  **Create and activate a Python virtual environment:**
    ```powershell
    # Create the virtual environment
    python -m venv gita

    # Activate it (for Windows PowerShell)
    .\gita\Scripts\Activate.ps1
    ```

3.  **Install the required packages:**
    Create a `requirements.txt` file with the following content:
    ```txt
    streamlit
    tensorflow
    tensorflow-hub
    chromadb
    ollama
    ```
    Then, run the installation command:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Download the LLM:**
    Pull the Gemma model that the application is configured to use.
    ```sh
    ollama pull gemma:2b
    ```

5.  **Place the Dataset:**
    Ensure your dataset file, `gita_knowledge_base.json` (containing the 110+ verses), is in the root directory of the project.

6.  **Run the Streamlit App:**
    ```sh
    streamlit run app.py
    ```
    Open your browser and navigate to `http://localhost:8501`.

---

##  Roadmap & Future Plans

This version of GitaGPT is a robust proof of concept. The vision is to make it an even more accessible and immersive tool.

-   **Full Telugu Language Immersion:** The current priority is to make the app **fully functional in Telugu**. This is a significant undertaking that involves:
    -   Translating the entire UI into conversational Telugu.
    -   Creating high-quality Telugu commentaries for the entire 110+ verse dataset.
    -   Updating the AI's prompt and logic to process queries and generate responses entirely in Telugu.

-   **Expand the Knowledge Base:** Grow the dataset to include all ~700 verses of the Gita with multilingual commentaries.

-   **User Feedback Mechanism:** Implement a feature for users to rate the quality and relevance of the AI's responses, which can be used to improve the retrieval process.

-   **Voice-to-Text Support:** Add a microphone input to allow users to ask their questions by speaking, improving accessibility.

---

##  How to Contribute

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. We welcome your help warmly, and as the guiding principle of this project suggests: **any help is good help.**

Whether you are a developer, a writer, a scholar of the Gita, or just someone passionate about the project's mission, there are many ways to contribute.

#### How You Can Help

* ** Verse & Translation Contributions:**
    * Help expand the dataset by identifying important verses that are missing(Main Focus).
    * Proofread the existing Sanskrit, English, or Telugu texts for any errors.
    * Contribute translations of verses into other languages, especially those in the public domain(Add your regional Languages).

* ** Commentary & Thematic Analysis:**
    * This is a crucial area! Help write the `modern_commentary` and `modern_commentary_telugu` for verses in the dataset. Your philosophical insights are invaluable and also add your regional languages to the `gita_knowledge_base.json` Eg.. `modern_commentary_hindi` etc.
    * Suggest new `themes` or keywords for existing verses to improve the AI's retrieval accuracy.

* ** Code Contributions:**
    * Help tackle items on our **Roadmap**, such as implementing the full Telugu language immersion.
    * Find and fix bugs in the application.
    * Suggest performance improvements or code refactoring.

* ** Bug Reports & Feedback:**
    * Use the app and report any issues or unexpected behavior by opening an issue on GitHub.
    * Provide feedback on the quality of the AI's responses. Does it feel empathetic? Is the wisdom relevant?

* ** Documentation Improvements:**
    * Help make this `README.md` clearer or add more detailed setup instructions.
    * Add comments to the code to make it easier for others to understand.


Every contribution, no matter how small, helps bring this project's vision to life. Thank you for your interest!

---

##  Acknowledgements

-   The English translations of the Bhagavad Gita are from the public domain work of **Swami Sivananda**.
-   The Telugu translations are based on widely accepted, traditional interpretations.
-   This project runs on the incredible open-source work from the teams behind **Streamlit, TensorFlow, Ollama, and ChromaDB**.
