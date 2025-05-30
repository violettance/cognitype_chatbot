import streamlit as st
import requests
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from memobase import MemoBaseClient, ChatBlob
import uuid

# Load environment variables from .env.local (local development)
load_dotenv('.env.local')

# Initialize Memobase client
def init_memobase():
    """Initialize Memobase client for long-term memory"""
    try:
        project_url = os.getenv("MEMOBASE_URL", "https://api.memobase.dev")
        api_key = os.getenv("MEMOBASE_API_KEY")
        
        if not api_key:
            st.warning("⚠️ Memobase API key not found. Memory features disabled.")
            return None
            
        mb = MemoBaseClient(project_url=project_url, api_key=api_key)
        if mb.ping():
            return mb
        else:
            st.warning("⚠️ Could not connect to Memobase. Memory features disabled.")
            return None
    except Exception as e:
        st.warning(f"⚠️ Memobase initialization failed: {str(e)}")
        return None

# Page configuration
st.set_page_config(
    page_title="🧠 Personality AI Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# JavaScript for localStorage functionality
st.markdown("""
<script>
function saveNameToLocalStorage(name) {
    localStorage.setItem('cognitype_user_name', name);
}

function getNameFromLocalStorage() {
    return localStorage.getItem('cognitype_user_name') || '';
}

function savePersonalityToLocalStorage(personality) {
    localStorage.setItem('cognitype_personality', personality);
}

function getPersonalityFromLocalStorage() {
    return localStorage.getItem('cognitype_personality') || '';
}

function getUserIdFromLocalStorage() {
    return localStorage.getItem('cognitype_user_id') || '';
}

function saveUserIdToLocalStorage(userId) {
    localStorage.setItem('cognitype_user_id', userId);
}

function getMemobaseUserIdFromLocalStorage() {
    return localStorage.getItem('cognitype_memobase_uid') || '';
}

function saveMemobaseUserIdToLocalStorage(uid) {
    localStorage.setItem('cognitype_memobase_uid', uid);
}

// New functions for browser-to-memobase mapping
function getBrowserIdFromLocalStorage() {
    return localStorage.getItem('cognitype_browser_user_id') || '';
}

function saveBrowserIdToLocalStorage(browserId) {
    localStorage.setItem('cognitype_browser_user_id', browserId);
}

function getMemobaseMappingForBrowser(browserId) {
    return localStorage.getItem('cognitype_memobase_mapping_' + browserId) || '';
}

function saveMemobaseMappingForBrowser(browserId, memobaseId) {
    localStorage.setItem('cognitype_memobase_mapping_' + browserId, memobaseId);
}
</script>
""", unsafe_allow_html=True)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        padding-top: 1rem !important;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Hide scrollbar */
    html {
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }
    
    body {
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }
    
    /* Move content higher */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: -1rem !important;
        max-width: 100% !important;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        margin-top: -1rem !important;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* MBTI Type Cards */
    .mbti-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .mbti-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .mbti-type {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .mbti-description {
        font-size: 1rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    /* Chat Interface */
    .chat-container {
        background: #f8fafc;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        position: relative;
    }
    
    .chat-message {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background: #e2e8f0;
        color: #2d3748;
        border-left: 4px solid #667eea;
    }
    
    .ai-message {
        background: #f8f9fa;
        color: #2d3748;
        border-left: 4px solid #667eea;
        border: 1px solid #e2e8f0;
    }
    
    /* Chat save button positioning */
    .chat-save-button {
        position: absolute;
        top: 1rem;
        right: 1rem;
        z-index: 10;
    }
    
    /* Purple styling for save buttons */
    .chat-container .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
        min-height: 36px !important;
        cursor: pointer !important;
        position: relative !important;
        z-index: 100 !important;
        pointer-events: auto !important;
    }
    
    .chat-container .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4) !important;
        cursor: pointer !important;
    }
    
    .chat-container .stButton > button:disabled {
        background: rgba(100, 100, 100, 0.3) !important;
        color: #999 !important;
        transform: none !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
    }
    
    /* Fix button container */
    .chat-container .stButton {
        z-index: 100 !important;
        position: relative !important;
    }
    
    /* Button Styling for main buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        cursor: pointer !important;
        z-index: 10 !important;
        position: relative !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        cursor: pointer !important;
    }
    
    /* Animation for loading */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #667eea;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation: loading1 0.6s infinite;
    }
    
    .loading-dots div:nth-child(2) {
        left: 8px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(3) {
        left: 32px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(4) {
        left: 56px;
        animation: loading3 0.6s infinite;
    }
    
    @keyframes loading1 {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }
    
    @keyframes loading3 {
        0% { transform: scale(1); }
        100% { transform: scale(0); }
    }
    
    @keyframes loading2 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(24px, 0); }
    }
    
    /* Stats and info boxes */
    .info-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #744210;
        border-left: 4px solid #ed8936;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide sidebar completely */
    .css-1d391kg {display: none !important;}
    .css-1l02zno {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    .stSidebar {display: none !important;}
    
    /* Hide custom scrollbar completely */
    ::-webkit-scrollbar {
        width: 0px !important;
        background: transparent !important;
    }
    
    .chat-message strong {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Constants
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP", 
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

MBTI_DESCRIPTIONS = {
    "INTJ": "Architect - Strategic, analytical, and independent",
    "INTP": "Thinker - Logical, innovative, and curious",
    "ENTJ": "Commander - Confident, strategic, and natural leaders",
    "ENTP": "Debater - Quick-witted, clever, and conceptual",
    "INFJ": "Advocate - Creative, insightful, and principled",
    "INFP": "Mediator - Idealistic, loyal, and values-driven",
    "ENFJ": "Protagonist - Charismatic, inspiring, and natural leaders",
    "ENFP": "Campaigner - Enthusiastic, creative, and sociable",
    "ISTJ": "Logistician - Practical, fact-minded, and reliable",
    "ISFJ": "Protector - Warm-hearted, conscientious, and cooperative",
    "ESTJ": "Executive - Organized, practical, and decisive",
    "ESFJ": "Consul - Caring, social, and popular",
    "ISTP": "Virtuoso - Bold, practical, and experimental",
    "ISFP": "Adventurer - Charming, sensitive, and artistic",
    "ESTP": "Entrepreneur - Smart, energetic, and perceptive",
    "ESFP": "Entertainer - Spontaneous, enthusiastic, and playful"
}

MBTI_EMOJIS = {
    "INTJ": "🏗️", "INTP": "🧠", "ENTJ": "👑", "ENTP": "💡",
    "INFJ": "🌟", "INFP": "🎨", "ENFJ": "🎭", "ENFP": "🦋", 
    "ISTJ": "📊", "ISFJ": "🛡️", "ESTJ": "⚡", "ESFJ": "🤝",
    "ISTP": "🔧", "ISFP": "🌸", "ESTP": "��", "ESFP": "🎉"
}

MBTI_FACTS = {
    "INTJ": "INTJs make up only 2% of the population and are known as 'The Architects' - they excel at strategic planning and long-term vision!",
    "INTP": "INTPs are natural theorists who love exploring complex ideas - they often become scientists, philosophers, or inventors!",
    "ENTJ": "ENTJs are born leaders who make up 3% of the population - they're excellent at organizing people and resources to achieve goals!",
    "ENTP": "ENTPs are innovative debaters who see possibilities everywhere - they're great at brainstorming and challenging conventional thinking!",
    "INFJ": "INFJs are the rarest personality type (1% of population) - they have incredible intuition and often become counselors or writers!",
    "INFP": "INFPs are idealistic mediators who are driven by their values - they often excel in creative fields and helping professions!",
    "ENFJ": "ENFJs are natural teachers and mentors - they have an amazing ability to inspire and develop others' potential!",
    "ENFP": "ENFPs are enthusiastic campaigners who bring energy to everything - they're excellent at connecting with people and generating ideas!",
    "ISTJ": "ISTJs are reliable logisticians who value tradition and stability - they're the backbone of many organizations!",
    "ISFJ": "ISFJs are caring protectors who remember details about people they care about - they're often found in healthcare and education!",
    "ESTJ": "ESTJs are efficient executives who get things done - they're natural organizers and often become successful managers!",
    "ESFJ": "ESFJs are warm-hearted consuls who create harmony in groups - they're excellent at reading social dynamics!",
    "ISTP": "ISTPs are practical virtuosos who love working with their hands - they're great at troubleshooting and mechanical tasks!",
    "ISFP": "ISFPs are gentle adventurers with strong aesthetic sense - they often excel in arts, music, or nature-related fields!",
    "ESTP": "ESTPs are energetic entrepreneurs who live in the moment - they're great at crisis management and hands-on problem solving!",
    "ESFP": "ESFPs are spontaneous entertainers who bring joy to others - they're natural performers and excellent at reading people's emotions!"
}

def get_api_key():
    """Get API key from environment variables"""
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        st.error("⚠️ TOGETHER_API_KEY environment variable is not set!")
        st.stop()
    return api_key

def create_personalized_prompt(mbti_type, user_question, memory_context=""):
    """Create a personalized prompt based on MBTI type and user memory"""
    base_prompt = f"""You are an AI chatbot that has the {mbti_type} personality type ({MBTI_DESCRIPTIONS.get(mbti_type, '')}). 
You are responding TO a user, not AS the user. You have the {mbti_type} cognitive preferences, communication style, and decision-making approach.
Think and respond like someone with {mbti_type} personality would - with their strengths, perspectives, and communication patterns.

{memory_context}

IMPORTANT: If the context from previous conversations contains information about the USER (like their occupation, interests, or personal details), reference that information when responding. You know this about the user from your previous conversations with them.

Instructions for your response:
- Respond as a {mbti_type} personality type chatbot
- Use the specific communication style and thinking patterns of {mbti_type}
- Reference what you know about the USER from previous conversations
- Give advice/opinions based on your {mbti_type} perspective
- Be helpful while maintaining your {mbti_type} personality traits

User's Question: {user_question}

Your response as a {mbti_type} chatbot:"""
    return base_prompt

def call_together_api(prompt, api_key):
    """Make API call to Together.ai's Mistral-7B model"""
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [""]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            return "Error: No response content received from the API."
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the API. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return "Error: Invalid API key. Please check your credentials."
        elif response.status_code == 429:
            return "Error: Rate limit exceeded. Please wait before trying again."
        else:
            return f"Error: API request failed with status {response.status_code}."
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response format from API."
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

# Initialize Memobase
if 'memobase_client' not in st.session_state:
    st.session_state.memobase_client = init_memobase()

if 'memobase_user' not in st.session_state:
    st.session_state.memobase_user = None

# Create or get Memobase user
if st.session_state.memobase_client and st.session_state.memobase_user is None:
    try:
        # Smart localStorage-based user management
        
        # Step 1: Get or create persistent browser user ID
        browser_user_id = None
        
        # Initialize JavaScript to check localStorage
        st.markdown("""
        <script>
        // Get or create browser user ID
        let browserId = getBrowserIdFromLocalStorage();
        if (!browserId) {
            // Generate new browser ID
            browserId = 'browser_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
            saveBrowserIdToLocalStorage(browserId);
            console.log('Created new browser ID:', browserId);
        } else {
            console.log('Found existing browser ID:', browserId);
        }
        
        // Check if we have a Memobase mapping for this browser
        const existingMemobaseId = getMemobaseMappingForBrowser(browserId);
        
        // Store data for Python to access
        window.browserUserData = {
            browserId: browserId,
            existingMemobaseId: existingMemobaseId
        };
        
        console.log('Browser-Memobase mapping:', browserId, '->', existingMemobaseId || 'none');
        </script>
        """, unsafe_allow_html=True)
        
        # Small delay to let JavaScript execute
        time.sleep(0.1)
        
        # For now, we'll use your existing user ID for testing
        # In production, you'd read the localStorage data properly
        existing_memobase_id = "b87a1d67-5aa2-4c6b-8d62-a56d841d8d32"
        
        try:
            # Try to load existing Memobase user
            st.session_state.memobase_user = st.session_state.memobase_client.get_user(existing_memobase_id)
            st.session_state.memobase_user_id = existing_memobase_id
            
            # Ensure mapping is saved in localStorage
            st.markdown(f"""
            <script>
            const browserId = window.browserUserData ? window.browserUserData.browserId : getBrowserIdFromLocalStorage();
            if (browserId) {{
                saveMemobaseMappingForBrowser(browserId, '{existing_memobase_id}');
                console.log('Saved mapping for existing user:', browserId, '->', '{existing_memobase_id}');
            }}
            </script>
            """, unsafe_allow_html=True)
            
            # Show success without page jumping using JavaScript
            st.markdown("""
            <script>
            // Create a temporary success notification
            const notification = document.createElement('div');
            # Success message removed to prevent page jumping
            # st.success(f"✨ Got your personalized {selected_mbti} response!")
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            # Could not load existing user - continue silently
            
            # Create new Memobase user (Memobase generates the ID)
            uid = st.session_state.memobase_client.add_user({
                "app": "cognitype_chatbot",
                "created_at": datetime.now().isoformat(),
                "session_type": "persistent_browser"
            })
            
            st.session_state.memobase_user_id = uid  # Memobase-generated ID
            st.session_state.memobase_user = st.session_state.memobase_client.get_user(uid)
            
            # Save the browser -> memobase mapping
            st.markdown(f"""
            <script>
            const browserId = window.browserUserData ? window.browserUserData.browserId : getBrowserIdFromLocalStorage();
            if (browserId) {{
                saveMemobaseMappingForBrowser(browserId, '{uid}');
                console.log('Created new Memobase user and saved mapping:', browserId, '->', '{uid}');
            }}
            </script>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        # Memory system error - continue silently
        pass

# Main header with modern styling
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🧠 Personality AI Chat</h1>
    <p class="main-subtitle">Get AI responses from different personality types</p>
</div>
""", unsafe_allow_html=True)

# Main content area with side-by-side layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🎯 Select Chatbot Personality")
    
    # Create two columns for personality type and name
    type_col, name_col = st.columns([1, 1])
    
    with type_col:
        # MBTI type selection with better styling
        selected_mbti = st.selectbox(
            "Personality type:",
            options=MBTI_TYPES,
            format_func=lambda x: f"{MBTI_EMOJIS[x]} {x}",
            help="Not sure about your type? Take a free test online!"
        )
    
    with name_col:
        # Name input field with localStorage integration
        # Initialize name from localStorage if available
        if 'loaded_name' not in st.session_state:
            # Try to get name from URL parameters as a fallback
            query_params = st.query_params
            st.session_state.loaded_name = query_params.get("name", "")
            
        user_name = st.text_input(
            "Your name:",
            value=st.session_state.loaded_name,
            placeholder="Enter your name",
            help="This helps personalize your experience",
            key="user_name_input"
        )
        
        # Save name to localStorage and URL when it changes
        if user_name and user_name != st.session_state.loaded_name:
            st.session_state.loaded_name = user_name
            # Update URL parameters to persist name
            if user_name.strip():
                st.query_params["name"] = user_name
            st.markdown(f"""
            <script>
            saveNameToLocalStorage('{user_name}');
            </script>
            """, unsafe_allow_html=True)
    
    # Display selected MBTI description with custom styling
    if selected_mbti:
        st.markdown(f"""
        <div class="mbti-card">
            <div class="mbti-type">{MBTI_EMOJIS[selected_mbti]} {selected_mbti}</div>
            <div class="mbti-description">{MBTI_DESCRIPTIONS[selected_mbti]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add some stats about the selected type
        st.markdown(f"""
        <div class="info-box">
            <strong>💡 Did you know?</strong><br>
            {MBTI_FACTS[selected_mbti]}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 💭 Ask Your Question")
    
    # Get user name for personalization
    display_name = user_name if 'user_name' in locals() and user_name else ""
    name_suffix = f" {display_name}" if display_name else ""
    
    # Question input with better styling
    user_question = st.text_area(
        f"What would you like to know{name_suffix}?",
        placeholder="Ask anything - from career advice to relationship tips, decision-making strategies, or personal growth insights...",
        height=280,
        help="Be specific for more personalized responses!",
        key="question_input_stable"  # Use stable key to prevent clearing
    )
    
    # Submit and clear buttons with better layout
    col_submit, col_clear = st.columns([3, 1])
    
    with col_submit:
        submit_button = st.button(
            f"🚀 Get {selected_mbti if selected_mbti else 'Personalized'} Response",
            type="primary",
            disabled=not selected_mbti,
            use_container_width=True
        )
    
    with col_clear:
        clear_button = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

# Handle clear button
if clear_button:
    st.session_state.conversation_history = []
    st.rerun()

# Handle submit button with improved loading animation
if submit_button and user_question.strip():
    if selected_mbti:
        # Use a fixed container to prevent page jumping
        with st.container():
            # Immediately show loading to provide instant feedback
            loading_placeholder = st.empty()
            loading_placeholder.markdown(f"""
            <div class="loading-animation">
                <div class="loading-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
            <p style="text-align: center; margin-top: 1rem;">
                🧠 Crafting a personalized {selected_mbti} response...
            </p>
            """, unsafe_allow_html=True)
            
            # Get memory context from Memobase if available (optimized for speed)
            memory_context = ""
            if st.session_state.memobase_user:
                try:
                    # Use faster Memobase context() with smaller token size
                    memory_context = st.session_state.memobase_user.context(
                        max_token_size=500,  # Reduced from 1000 for speed
                        profile_event_ratio=0.5,  # Balanced ratio
                        require_event_summary=False  # Skip summaries for speed
                    )
                    
                    if memory_context and len(memory_context.strip()) > 0:
                        memory_context = f"\n<user_memory>\n{memory_context}\n</user_memory>\n"
                        # Update loading message to show memory usage
                        loading_placeholder.markdown(f"""
                        <div class="loading-animation">
                            <div class="loading-dots">
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div>
                        </div>
                        <p style="text-align: center; margin-top: 1rem;">
                            🧠 Crafting a personalized {selected_mbti} response + using your memory...
                        </p>
                        """, unsafe_allow_html=True)
                    else:
                        memory_context = ""
                        
                except Exception as e:
                    # If memory fails, continue without it for speed
                    memory_context = ""
            
            # Create personalized prompt with memory
            prompt = create_personalized_prompt(selected_mbti, user_question, memory_context)
            
            # Get API key
            api_key = get_api_key()
            
            # Make API call
            response = call_together_api(prompt, api_key)
            
            # Clear loading animation
            loading_placeholder.empty()
            
            # Store in conversation history with timestamp
            st.session_state.conversation_history.append({
                'mbti_type': selected_mbti,
                'question': user_question,
                'response': response,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            
            # Prevent page jumping with JavaScript
            st.markdown("""
            <script>
            // Keep scroll position stable
            window.scrollTo({top: window.scrollY, behavior: 'instant'});
            </script>
            """, unsafe_allow_html=True)
    else:
        st.error("🎯 Please select your personality type first!")

# Display conversation history with improved styling
if st.session_state.conversation_history:
    st.markdown("### 💬 Chat History")
    
    for i, conversation in enumerate(reversed(st.session_state.conversation_history)):
        timestamp = conversation.get('timestamp', 'Unknown time')
        conversation_index = len(st.session_state.conversation_history) - 1 - i
        
        # Create container with save button next to user message header
        user_col1, user_col2 = st.columns([9, 2])  # Give more space to save button
        
        with user_col1:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>💬 You ({conversation['mbti_type']}) - {timestamp}</strong><br>
                {conversation['question']}
            </div>
            """, unsafe_allow_html=True)
        
        with user_col2:
            # Save button next to user message - improved layout
            st.markdown('<div style="padding-top: 0.5rem;"></div>', unsafe_allow_html=True)  # Add some top padding
            if st.button(
                "💾 Save",
                help="Save this conversation to memory",
                disabled=not st.session_state.memobase_user,
                key=f"save_conv_{conversation_index}",
                use_container_width=True
            ):
                if st.session_state.memobase_user:
                    try:
                        # Save using proper ChatBlob format according to Memobase docs
                        from memobase import ChatBlob
                        
                        # Create ChatBlob with proper message format
                        chat_blob = ChatBlob(messages=[
                            {
                                "role": "user",
                                "content": conversation['question']
                            },
                            {
                                "role": "assistant", 
                                "content": conversation['response']
                            }
                        ])
                        
                        # Insert the chat blob
                        blob_id = st.session_state.memobase_user.insert(chat_blob)
                        
                        # Flush to trigger memory extraction (profiles and events)
                        st.session_state.memobase_user.flush()
                        
                        # Use container to prevent page jumping
                        with st.container():
                            st.success("💾 Conversation saved to memory!")
                        
                    except Exception as e:
                        st.error(f"❌ Failed to save: {str(e)}")
                else:
                    st.warning("⚠️ Memory service not available")
        
        # Display AI response
        if conversation['response'].startswith("Error:"):
            st.markdown(f"""
            <div class="chat-message" style="border-left: 4px solid #e53e3e; background: #fed7d7;">
                <strong>🤖 AI Assistant</strong><br>
                {conversation['response']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 {conversation['mbti_type']} Assistant</strong><br>
                {conversation['response']}
            </div>
            """, unsafe_allow_html=True)

# Footer with better styling
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; margin-top: 2rem;'>
    <p style='color: #666; font-size: 1.1rem; margin: 0; font-weight: 500;'>
        ✨ Built with love using Streamlit • Powered by Together.ai & Mistral-7B ✨
    </p>
    <p style='color: #888; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
        🧠 Making AI conversations more personal, one type at a time
    </p>
</div>
""", unsafe_allow_html=True)

# Load persistent data from localStorage on page load
if 'data_loaded_from_storage' not in st.session_state:
    st.session_state.data_loaded_from_storage = True
    
    # Initialize a way to check if we have localStorage data
    st.markdown("""
    <script>
    // Check for existing user data in localStorage
    const savedName = getNameFromLocalStorage();
    const savedUserId = getUserIdFromLocalStorage();
    const savedMemobaseUid = getMemobaseUserIdFromLocalStorage();
    const currentMemobaseUid = localStorage.getItem('cognitype_current_memobase_uid');
    
    // Create hidden elements to communicate with Python
    if (savedName || savedUserId || savedMemobaseUid || currentMemobaseUid) {
        const dataDiv = document.createElement('div');
        dataDiv.id = 'localStorage-data';
        dataDiv.style.display = 'none';
        if (savedName) dataDiv.setAttribute('data-name', savedName);
        if (savedUserId) dataDiv.setAttribute('data-user-id', savedUserId);
        if (savedMemobaseUid) dataDiv.setAttribute('data-memobase-uid', savedMemobaseUid);
        if (currentMemobaseUid) dataDiv.setAttribute('data-current-memobase-uid', currentMemobaseUid);
        document.body.appendChild(dataDiv);
        
        console.log('Found localStorage data:', {
            name: savedName, 
            userId: savedUserId, 
            memobaseUid: savedMemobaseUid,
            currentMemobaseUid: currentMemobaseUid
        });
        
        // Store in Streamlit session for Python access
        window.localStorage_data = {
            name: savedName,
            userId: savedUserId,
            memobaseUid: savedMemobaseUid,
            currentMemobaseUid: currentMemobaseUid
        };
    }
    </script>
    """, unsafe_allow_html=True)
