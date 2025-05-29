import streamlit as st
import requests
import json
import os
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🧠 Personality AI Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        margin-top: -0.5rem !important;
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
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
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
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
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

def create_personalized_prompt(mbti_type, user_question):
    """Create a personalized prompt based on MBTI type"""
    mbti_context = f"""You are responding to someone with the {mbti_type} personality type ({MBTI_DESCRIPTIONS.get(mbti_type, '')}). 
Please tailor your response to match their cognitive preferences, communication style, and decision-making approach. 
Consider their strengths, potential blind spots, and preferred way of processing information.

Question: {user_question}

Response:"""
    return mbti_context

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

# Main header with modern styling
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🧠 Personality AI Chat</h1>
    <p class="main-subtitle">Get AI responses tailored to your unique personality type</p>
</div>
""", unsafe_allow_html=True)

# Main content area with side-by-side layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🎯 Your Personality Type")
    
    # MBTI type selection with better styling
    selected_mbti = st.selectbox(
        "Choose your personality type:",
        options=MBTI_TYPES,
        format_func=lambda x: f"{MBTI_EMOJIS[x]} {x}",
        help="Not sure about your type? Take a free test online!"
    )
    
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
    
    # Question input with better styling
    user_question = st.text_area(
        "What would you like to know?",
        placeholder="Ask anything - from career advice to relationship tips, decision-making strategies, or personal growth insights...",
        height=280,
        help="Be specific for more personalized responses!",
        key=f"question_input_{len(st.session_state.conversation_history)}"
    )
    
    # Submit and clear buttons with better layout
    col_submit, col_clear = st.columns([2, 1])
    
    with col_submit:
        submit_button = st.button(
            f"🚀 Get {selected_mbti if selected_mbti else 'Personalized'} Response",
            type="primary",
            disabled=not selected_mbti,
            use_container_width=True
        )
    
    with col_clear:
        clear_button = st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        )

# Handle clear button
if clear_button:
    st.session_state.conversation_history = []
    st.rerun()

# Handle submit button with improved loading animation
if submit_button and user_question.strip():
    if selected_mbti:
        # Custom loading animation
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
        
        # Create personalized prompt
        prompt = create_personalized_prompt(selected_mbti, user_question)
        
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
        
        # Success message
        st.success(f"✨ Got your personalized {selected_mbti} response!")
    else:
        st.error("🎯 Please select your personality type first!")

# Display conversation history with improved styling
if st.session_state.conversation_history:
    st.markdown("### 💬 Chat History")
    
    for i, conversation in enumerate(reversed(st.session_state.conversation_history)):
        timestamp = conversation.get('timestamp', 'Unknown time')
        
        # Create a more chat-like interface
        st.markdown(f"""
        <div class="chat-container">
            <div class="chat-message user-message">
                <strong>💬 You ({conversation['mbti_type']}) - {timestamp}</strong><br>
                {conversation['question']}
            </div>
        """, unsafe_allow_html=True)
        
        # Display AI response
        if conversation['response'].startswith("Error:"):
            st.markdown(f"""
            <div class="chat-message" style="border-left: 4px solid #e53e3e; background: #fed7d7;">
                <strong>🤖 AI Assistant</strong><br>
                {conversation['response']}
            </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI Assistant ({conversation['mbti_type']} focused)</strong><br>
                {conversation['response']}
            </div>
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
