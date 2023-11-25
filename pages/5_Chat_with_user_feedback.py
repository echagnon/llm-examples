from openai import OpenAI
import streamlit as st
# from streamlit_feedback import streamlit_feedback
from trubrics.integrations.streamlit import FeedbackCollector

openai_api_key = st.secrets["OPENAI_KEY"]

st.title("📝 Chat with feedback (Trubrics)")

gpt_choice = st.radio(
    "Which GPT do you want to use?",
    ["GPT3.5", ":rainbow[GPT4.0]"],
    captions = ["Most economical", "Best of the best"])

if gpt_choice == "GPT3.5" : 
    use_model = "gpt-3.5-turbo"
else : 
    use_model = "gpt-4-1106-preview"

"""
In this example, we're using [streamlit-feedback](https://github.com/trubrics/streamlit-feedback) and Trubrics to collect and store feedback
from the user about the LLM responses.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model=use_model, messages=messages)
    st.session_state["response"] = response.choices[0].message.content
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])

if "response" in st.session_state and st.session_state["response"]:
    collector = FeedbackCollector(
    email=st.secrets.TRUBRICS_EMAIL,
    password=st.secrets.TRUBRICS_PASSWORD,
    project="default")

    user_feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        model=use_model,
        prompt_id=None,  # checkout collector.log_prompt() to log your user prompts
        )
    
    if user_feedback:
        st.toast("Feedback recorded!", icon="📝")

        
        
