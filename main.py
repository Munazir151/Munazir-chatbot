import streamlit as st
import json
import random
import csv
from datetime import datetime
import pandas as pd

# Set Streamlit theme and styling at startup
st.set_page_config(
    page_title="Munazir Ansari",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with better color scheme and styling
st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #2e7d32;
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 0;
    }
    
    .bot-message {
        background-color: #1976d2;
        color: white;
        align-self: flex-start;
        border-bottom-left-radius: 0;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
    }
    
    .stButton button:hover {
        background-color: #45a049;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e1e1e;
    }
    
    /* Title styling */
    h1 {
        color: #fafafa;
        text-align: center;
        padding: 1rem;
    }
    
    .avatar {
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def load_intents():
    """Load intents from JSON file"""
    try:
        with open('intents.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading intents: {e}")
        return {}

def get_bot_response(user_input, intents_data):
    """Get bot response based on user input"""
    if not user_input:
        return "Please ask me something!"
    
    user_input = user_input.lower().strip()
    
    # Check greetings and basic conversations first
    basic_patterns = ['greetings', 'goodbyes', 'thanks', 'how_are_you']
    for category in basic_patterns:
        patterns = intents_data['responses'][category]['patterns']
        if any(pattern in user_input for pattern in patterns):
            responses = intents_data['responses'][category]['responses']
            return random.choice(responses)
    
    # Check other responses
    responses = {
        "name": lambda: f"I am {intents_data.get('name', 'Munazir Ansari')}",
        "education": lambda: f"I am pursuing {intents_data.get('academic', {}).get('degree')} at {intents_data.get('academic', {}).get('college')} with a CGPA of {intents_data.get('academic', {}).get('CGPA')}",
        "skills": lambda: f"My skills include: {', '.join(intents_data.get('skills', []))}",
        "project": lambda: f"My main project is {intents_data.get('projects', [{}])[0].get('name')}: {intents_data.get('projects', [{}])[0].get('description')}" if intents_data.get('projects') else "No projects listed yet",
        "email": lambda: f"You can reach me at {intents_data.get('email')}",
        "contact": lambda: f"You can reach me via:\nMobile: {intents_data.get('mobile')}\nEmail: {intents_data.get('email')}\nLinkedIn: {intents_data.get('linkedin')}",
        "linkedin": lambda: f"Connect with me on LinkedIn: {intents_data.get('linkedin')}",
        "location": lambda: f"I'm based in {intents_data.get('location')}",
        "age": lambda: f"I am {intents_data.get('age')} years old",
        "about": lambda: f"I am {intents_data.get('name')}, an {intents_data.get('age')}-year-old student based in {intents_data.get('location')}. I'm pursuing {intents_data.get('academic', {}).get('degree')} at {intents_data.get('academic', {}).get('college')}.",
        "social": lambda: f"You can find me on LinkedIn: {intents_data.get('linkedin')}",
        "job": lambda: f"I am actively seeking Software Engineering opportunities! Feel free to reach out via:\nMobile: {intents_data.get('mobile')}\nEmail: {intents_data.get('email')}\nLinkedIn: {intents_data.get('linkedin')}"
    }
    
    for key, response_fn in responses.items():
        if key in user_input:
            return response_fn()
    
    return "I'm still learning. You can ask about my education, skills, projects, or contact information!"

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'intents_data' not in st.session_state:
        st.session_state.intents_data = load_intents()

def main():
    initialize_session_state()

    st.title("🤖 Munazir Ansari's Portfolio Chat")
    
    tabs = st.tabs(["💬 Chat", "📚 History", "ℹ️ About"])
    
    with tabs[0]:
        chat_container = st.container()
        
        with chat_container:
            for chat in st.session_state.chat_history:
                with st.container():
                    st.markdown(f"""
                        <div class="chat-message user-message">
                            👤 You: {chat['user']}
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="chat-message bot-message">
                            🤖 Munazir: {chat['bot']}
                        </div>
                    """, unsafe_allow_html=True)
        
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Ask me anything about my skills, education, or projects:", 
                                     placeholder="E.g., What are your skills?")
            cols = st.columns([4, 1])
            with cols[1]:
                submit_button = st.form_submit_button("Send 📤")
            
            if submit_button and user_input:
                response = get_bot_response(user_input, st.session_state.intents_data)
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('chat_history.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([user_input, response, timestamp])
                
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response
                })
                
                st.rerun()

    with tabs[1]:
        try:
            df = pd.read_csv('chat_history.csv', names=['Question', 'Response', 'Timestamp'])
            st.dataframe(df.style.set_properties(**{'background-color': '#262730', 'color': 'white'}), 
                        use_container_width=True)
        except:
            st.info("No conversation history yet. Start chatting to create history!")

    with tabs[2]:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://avatars.githubusercontent.com/u/your_github_username", width=200)
        with col2:
            st.write(f"### {st.session_state.intents_data.get('name')}")
            st.write(f"🎓 {st.session_state.intents_data['academic']['degree']} Student")
            st.write(f"🏫 {st.session_state.intents_data['academic']['college']}")
            st.write(f"📧 {st.session_state.intents_data.get('email')}")
            
        st.write("### Skills")
        for skill in st.session_state.intents_data.get('skills', []):
            st.markdown(f"- {skill}")

if __name__ == '__main__':
    main()
