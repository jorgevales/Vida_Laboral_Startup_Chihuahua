"""
streamlit run app.py
"""
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import os
import json
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

selected = option_menu(
    menu_title=None,
    options=["Inicio", "Proyecto", "Read.me"],
    icons=["house", "braces", "person-circle"],
    orientation="horizontal",
    default_index=1
    )

if selected == "Inicio":
    col1, col2, col3 = st.columns([1,6,1])
    st.image("STARTUPSCHOOL.png", width=350)

    col1, col2 = st.columns([3,1]) 
    st.write("SON-IA, donde la excelencia empresarial \
y la toma de decisiones estratégicas se unen en un proyecto innovador. \
Le presentamos una propuesta disruptiva: una alianza estratégica entre bases de datos \
de comportamiento del empleado, pertenecientes a empresas líderes en nuestra ciudad. \
Mediante la implementación de programación analítica e inteligencia artificial, \
nos embarcamos en un viaje hacia la optimización de la contratación de empleados. \
Nuestra visión se centra en la creación de una base de datos centralizada, que alberga \
un exhaustivo registro histórico de su vida laboral. Aprovechando todo el potencial \
de la inteligencia artificial y la programación analítica, desentrañamos patrones de \
comportamiento que van más allá de la mera información sobre sus empleos anteriores. \
Nos sumergimos en sus éxitos, fracasos y comportamientos determinantes en cada etapa \
de su trayectoria profesional. Le invitamos a adentrarse en este emocionante viaje, \
donde el futuro de la contratación se transforma en una realidad. Únase a nosotros y \
descubra un mundo de posibilidades para tomar decisiones de contratación más acertadas que nunca antes.")
    
    lottie_trend = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_ZQqYEY.json")
    lottie_trend_file = load_lottiefile("trend.json")


if selected == "Proyecto":
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None or api_key == "":
        st.error("OPENAI_API_KEY is not set. Please set it in the environment variables of your Streamlit Cloud app.")
        exit(1)

    # st.set_page_config(page_title="EMPLOYEE DATA")
    # st.header("VIDA LABORAL")
    st.markdown("<p style='font-size: 64px; font-weight: bold;'>S O N I A :</p>", unsafe_allow_html=True)

    csv_file = r"Data_empleados.csv"
    fixed_file = r"Data_empleados_fixed.csv"

    # Fix accents and special characters in the CSV file
    with open(csv_file, "r", encoding="latin-1") as file:
        content = file.read()

    with open(fixed_file, "w", encoding="utf-8") as file:
        file.write(content)

    chat_model_to_use = OpenAI(temperature=0)

    agent = create_csv_agent(chat_model_to_use, fixed_file, verbose=True)

    user_question = st.text_input("Hazme una pregunta del empleado que quieras conocer:")

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
    st.write("\n")
    st.write("\n")

    with st.expander("Ejemplos de preguntas para hacer"):
        st.write("1. ¿Cuántos empleados hay en mi base de datos?")
        st.write("2. Dime el historial laboral de Jorge Vales")
        st.write("3. ¿Cuántos empleos ha tenido Esteban Carrillo?")
        st.write("4. ¿Cuál es la edad promedio dentro de mi archivo?")
    
    with st.expander("Funcionamiento"):
        st.write("La aplicación está cargada con una base de datos ejemplo")

if selected == "Read.me":
    st.title("Read.me")

    st.write("John W. Gardner decía 'La excelencia es hacer las cosas ordinarias extraordinariamente bien', \
y creo que es totalmente cierto.\n\
Desde hace tiempo, la excelencia es algo que he buscado con pasión, las ganas de querer darlo todo sin importar cual sea el proyecto.\n")
    
    st.write("")

    with st.expander("Futuro"):
        st.image("Unconditional offer.png")