from openai import OpenAI
import streamlit as st
import pickledb

# with st.sidebar:
openai_api_key = st.secrets["OPENAI_KEY"]

db = pickledb.load('llm_prompts.db', True)
db.set('prompt1', 'what is love')
get_prompt = db.get('prompt1')
print(get_prompt)


st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

gpt_choice = st.radio(
    "Which GPT do you want to use?",
    ["GPT3.5", ":rainbow[GPT4.0]"],
    captions = ["Most economical", "Best of the best"])

if gpt_choice == "GPT3.5" : 
    use_model = "gpt-3.5-turbo"
else : 
    use_model = "gpt-4-1106-preview"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=use_model, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(use_model + " : " + msg)
