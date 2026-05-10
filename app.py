import streamlit as st
import tensorflow_hub as hub
import chromadb
import ollama
import json
import time

# --- Configuration ---
DATASET_PATH = "gita_knowledge_base.json" 
OLLAMA_MODEL = "gemma:2b" 

# --- Page Configuration ---
st.set_page_config(
    page_title="GitaGPT: Inner Peace Edition",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Caching Functions for Performance (Now Silent) ---

@st.cache_resource
def load_tf_model():
    """Loads the Universal Sentence Encoder model from TensorFlow Hub."""
    model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(model_url)
    return model

@st.cache_resource
def setup_vector_db(path):
    """Sets up the ChromaDB vector store with Gita verses."""
    embed_model = load_tf_model() 

    client = chromadb.Client()
    # Using a new collection name to ensure the new metadata is loaded
    collection = client.get_or_create_collection(name="gita_verses_telugu")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            gita_data = json.load(f)
    except FileNotFoundError:
        st.error(f"Error: The dataset file '{path}' was not found. Please make sure it's in the same folder as app.py.")
        return None

    # Only load data if the collection is empty
    if collection.count() == 0:
        documents = []
        metadatas = []
        ids = []
        
        for verse in gita_data:
            documents.append(f"Themes: {', '.join(verse['themes'])}. Commentary: {verse['modern_commentary']}")
            # *** NEW: ADDING TELUGU TRANSLATION TO METADATA ***
            metadatas.append({
                "chapter": verse['chapter'],
                "verse": verse['verse'],
                "translation_sivananda": verse['translation_sivananda'],
                "translation_telugu": verse['translation_telugu'], # Added this field
                "sanskrit": verse['sanskrit']
            })
            ids.append(verse['id'])
        
        embeddings = embed_model(documents).numpy().tolist()
        
        collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    return collection

# --- Main Application Logic ---

gita_collection = setup_vector_db(DATASET_PATH)
embed_model = load_tf_model() 

# --- Streamlit UI ---

st.title("🕉️ GitaGPT: Inner Peace Edition")
st.caption(f"Your spiritual guide to life's questions, powered by the Bhagavad Gita and Gemma. Currently serving from Hyderabad, India on {time.strftime('%Y-%m-%d')}.")

# *** NEW: ADDED SIDEBAR TOGGLE FOR TELUGU ***
st.sidebar.title("Display Options")
show_telugu = st.sidebar.toggle("Show Telugu & Sanskrit (తెలుగు & సంస్కృతం చూపండి)", value=False)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste. I am GitaGPT, your compassionate guide. How may I help you find clarity or peace today?"}]
    st.session_state.last_verse_metadata = None # To store metadata of the last retrieved verse

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about purpose, struggle, or inner peace..."):
    if not gita_collection:
        st.error("Vector database not loaded. Cannot process query.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Seeking wisdom from the Gita..."):
                prompt_embedding = embed_model([prompt]).numpy().tolist()
                
                results = gita_collection.query(
                    query_embeddings=prompt_embedding,
                    n_results=1
                )
                
                retrieved_verse_metadata = None
                if not results['ids'][0]:
                    retrieved_context = "No specific verse found, please answer based on general Gita teachings."
                    st.session_state.last_verse_metadata = None
                else:
                    retrieved_verse_metadata = results['metadatas'][0][0]
                    st.session_state.last_verse_metadata = retrieved_verse_metadata # Save for later use
                    
                    verse_text = retrieved_verse_metadata['translation_sivananda']
                    verse_info = f"From Bhagavad Gita, Chapter {retrieved_verse_metadata['chapter']}, Verse {retrieved_verse_metadata['verse']}"
                    retrieved_context = f"Relevant Verse ({verse_info}): \"{verse_text}\""

                augmented_prompt = f"""
                You are GitaGPT, a compassionate, wise, and spiritual guide based on the teachings of the Bhagavad Gita. Your persona is calm, empathetic, and you never give direct solutions, but rather philosophical insights. You are not preachy or robotic.
                A user is asking for guidance. Their question is: "{prompt}"
                Here is the most relevant verse from the Gita to guide your response:
                {retrieved_context}

                Your task is to provide a response that follows these steps:
                1. Start with empathy, acknowledging the user's feelings.
                2. Gently introduce the wisdom from the provided verse, explaining its meaning in a modern, relatable context.
                3. Guide the user to reflect on their situation through the lens of this wisdom.
                4. Conclude your response by quoting the full English verse text and its reference. Do not add any extra commentary after quoting the verse.
                """

                try:
                    stream = ollama.chat(
                        model=OLLAMA_MODEL, 
                        messages=[{'role': 'user', 'content': augmented_prompt}],
                        stream=True
                    )
                    
                    for chunk in stream:
                        full_response += chunk['message']['content']
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"I apologize, I am facing a technical difficulty and cannot connect to my core wisdom. Please try again later. (Error: {e})"
                    message_placeholder.markdown(full_response)

            # *** NEW: APPEND TELUGU AND SANSKRIT IF TOGGLE IS ON ***
            if show_telugu and st.session_state.last_verse_metadata:
                sanskrit_text = st.session_state.last_verse_metadata.get('sanskrit', 'Sanskrit text not available.')
                telugu_text = st.session_state.last_verse_metadata.get('translation_telugu', 'Telugu translation not available.')
                
                additional_info = f"""
                ---
                **Original Sanskrit (संस्कृतम्):**
                > {sanskrit_text}

                **Telugu Translation (తెలుగు అనువాదం):**
                > {telugu_text}
                """
                full_response += additional_info
                message_placeholder.markdown(full_response)


        st.session_state.messages.append({"role": "assistant", "content": full_response})