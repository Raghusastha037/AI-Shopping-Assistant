import asyncio
import aiohttp
import requests
import streamlit as st
import os

# Try importing Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:      
    GEMINI_AVAILABLE = False
    st.error("⚠️ google-generativeai not installed. Run: pip install google-generativeai")

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# API KEYS - SECURE METHOD
# -------------------------
# Method 1: Streamlit Secrets (for Streamlit Cloud deployment)
# Method 2: Environment Variables (for local development)

def get_api_key(key_name, secret_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        return st.secrets[secret_name]
    except:
        # Fall back to environment variables (for local development)
        return os.getenv(key_name, "")

GEMINI_API_KEY = get_api_key("GEMINI_API_KEY", "GEMINI_API_KEY")
SERPER_KEY = get_api_key("SERPER_KEY", "SERPER_KEY")
ALIEXPRESS_KEY = get_api_key("ALIEXPRESS_KEY", "ALIEXPRESS_KEY")

# Validate API keys
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please set it in secrets.toml or environment variables.")
if not SERPER_KEY:
    st.warning("⚠️ SERPER_KEY not found. Search functionality may be limited.")
if not ALIEXPRESS_KEY:
    st.warning("⚠️ ALIEXPRESS_KEY not found. Product search may be limited.")

# -------------------------
# Gemini setup
# -------------------------       
@st.cache_resource
def setup_gemini():
    """Initialize Gemini with caching to avoid repeated setup"""
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return None, False
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        for model_name in [
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-flash-latest",
            "models/gemini-pro-latest"
        ]:
            try:
                model = genai.GenerativeModel(model_name)
                test = model.generate_content("hello", generation_config={"max_output_tokens": 5})
                if test and test.text:
                    return model_name, True
            except Exception as e:
                continue
        return None, False
    except Exception as e:
        st.error(f"❌ Gemini setup failed: {e}")
        return None, False

WORKING_MODEL, gemini_ready = setup_gemini()

# -------------------------
# API CONFIGS
# -------------------------
ALIEXPRESS_HEADERS = {
    "X-RapidAPI-Key": ALIEXPRESS_KEY,
    "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
}

async def fetch_aliexpress(query):
    if not ALIEXPRESS_KEY:
        return None
    url = "https://aliexpress-datahub.p.rapidapi.com/search"
    params = {"query": query, "limit": "8"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=ALIEXPRESS_HEADERS, params=params, timeout=10) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return [
                    {"title": i.get("title", ""), "price": i.get("price", "N/A"), "rating": i.get("rating", "N/A")}
                    for i in data.get("results", [])
                ]
    except Exception as e:
        st.error(f"AliExpress Error: {e}")
        return None

def fetch_serper_data(query):
    if not SERPER_KEY:
        return None
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 10}
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        st.error(f"Serper Error: {e}")
        return None

# -------------------------
# Natural AI Response Generator
# -------------------------
def generate_ai_response(user_query, serper_data=None):
    """Gemini generates full conversational, natural answers."""
    if not gemini_ready or not WORKING_MODEL:
        return (
            "I'm currently running in fallback mode — "
            "please check the Gemini API key or internet connection."
        )

    context_info = ""
    if serper_data:
        organic = serper_data.get("organic", [])
        snippets = [o.get("snippet", "") for o in organic[:3]]
        context_info = "\n".join(snippets)

    prompt = f"""
You are a friendly, expert AI shopping assistant.

User asked: "{user_query}"

Use your own knowledge and optionally the following info if useful:
{context_info}

Your task:
- Provide a detailed, natural, and conversational answer.
- Include technical details and comparisons where relevant.
- Write like an expert human reviewer (like ChatGPT style).
- Structure the response with headers, bullet points, and a clear conclusion.
- Avoid saying "here's what I found"; just answer directly.
- Be friendly and professional.
"""

    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        res = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
                "top_p": 0.9,
                "top_k": 40,
            },
        )
        if res and res.text:
            return res.text
        return "⚠️ Gemini returned no response."
    except Exception as e:
        return f"⚠️ Error connecting to Gemini API: {str(e)}"

# -------------------------
# STREAMLIT UI
# -------------------------

# Sidebar
with st.sidebar:
    st.title("🛍️ AI Shopping Assistant")
    st.markdown("---")
    
    # Status indicators
    st.subheader("Status")
    if gemini_ready:
        st.success(f"✅ Gemini Active")
        st.caption(f"Model: {WORKING_MODEL}")
    else:
        st.error("❌ Gemini Unavailable")
        st.caption("Running in fallback mode")
    
    st.markdown("---")
    st.subheader("About")
    st.info("""
    This AI assistant helps you:
    - Compare products
    - Find deals
    - Learn specifications
    - Get expert advice
    """)
    
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.title("🛍️ AI Shopping Assistant")
st.caption("Ask me anything about products, comparisons, or shopping advice!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            user_input = prompt.strip().lower()
            
            # Handle greetings
            greetings = ["hi", "hii", "hello", "hey", "good morning", "good evening", "good afternoon"]
            if any(word in user_input for word in greetings):
                response = (
                    "👋 Hello there! I'm your AI Shopping Assistant. "
                    "I can help you compare products, find deals, or learn specs. "
                    "What would you like to explore today?"
                )
            else:
                # Fetch data and generate response
                try:
                    serper_data = fetch_serper_data(user_input)
                    response = generate_ai_response(user_input, serper_data)
                except Exception as e:
                    response = f"⚠️ An error occurred: {str(e)}"
            
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.caption("Powered by Gemini AI & Streamlit")
