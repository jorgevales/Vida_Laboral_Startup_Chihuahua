"""
streamlit run app.py

"""
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import os

load_dotenv()

st.write("First message")

# Load the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None or api_key == "":
    st.error("OPENAI_API_KEY is not set. Please set it in the environment variables of your Streamlit Cloud app.")
    exit(1)

# st.set_page_config(page_title="EMPLOYEE DATA")
st.header("VIDA LABORAL")

csv_file = r"Data_empleados.csv"
fixed_file = r"Data_empleados_fixed.csv"

# Fix accents and special characters in the CSV file
with open(csv_file, "r", encoding="latin-1") as file:
    content = file.read()

with open(fixed_file, "w", encoding="utf-8") as file:
    file.write(content)

chat_model_to_use = OpenAI(temperature=0)

agent = create_csv_agent(chat_model_to_use, fixed_file, verbose=True)

user_question = st.text_input(
    "Hazme una pregunta del empleado que quieras conocer: "
)

if user_question is not None and user_question != "":
    with st.spinner(text="Procesando..."):
        # Use get_openai_callback as a context manager to track token usage
        with get_openai_callback() as cb:
            response = agent.run(user_question)
            st.write(response)

        # Printing the token usage information
        print(f"Total Tokens Used: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${format(cb.total_cost, '.50f')}")