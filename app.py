import streamlit as st
from core.chatbot_core import ChatbotCore
from router import route, agent_map

# chatbot initialisation
bot_core = ChatbotCore()
#side bar 
# side bar style 
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #f7f7f8;
            padding: 2rem 1rem;
        }
        button{
            border: none !important;
            background-color: #f7f7f8 !important;
        }
         .stChatMessage.user {
            text-align: right;
        }
        .stChatMessage.user .stMarkdown {
            background-color: #e8f0fe;
            padding: 10px 16px;
            border-radius: 12px;
            display: inline-block;
            max-width: 80%;
        }
        .stChatMessage.assistant .stMarkdown {
            background-color: #f1f1f1;
            padding: 10px 16px;
            border-radius: 12px;
            display: inline-block;
            max-width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

# sidebar content
with st.sidebar:
    # new chat button
    if st.button("🔄 Nouveau chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Comment puis-je t’aider aujourd’hui ?"}]

# page config
st.set_page_config(page_title="Assistant conversationnel", page_icon="🤖", layout="centered")
st.title("Assistant conversationnel")
st.markdown("Pose une question juridique, RH, ou liée au CV. L’agent adapté te répondra automatiquement.")

# conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Comment puis-je t’aider aujourd’hui ?"}]

# display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# user input
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            try:
                agent_name = route(prompt)
                agent_info = agent_map.get(agent_name)
                response = bot_core.identify_use_case(prompt, agent_info)
            except Exception as e:
                response = "Je ne suis pas certain de pouvoir répondre à cette question pour le moment."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})