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
    options=["Inicio", "NIA", "Read.me"],
    icons=["house", "braces", "person-circle"],
    orientation="horizontal",
    default_index=0
    )

# Initialize the session state if it doesn't exist
if "page" not in st.session_state:
    st.session_state.page = "inicio"

if selected == "Inicio":
    col1, col2, col3 = st.columns([1,6,1])
    st.image("NIA Analytics 2.png")

    col1, col2 = st.columns([3,1]) 
    st.write("En la era de la información, donde los datos reinan, presentamos una solución innovadora \
para optimizar el proceso de contratación: una base de datos unificada y centralizada del \
comportamiento laboral de los empleados de todas las empresas de la ciudad.")
    
    st.write("A través de esta plataforma, logramos capturar y reflejar un historial laboral completo, \
detallado y en constante actualización, desde el inicio hasta el final de cada empleo. Pero no nos detenemos allí, llevamos la gestión de recursos humanos \
al siguiente nivel al implementar técnicas avanzadas de programación analítica e inteligencia artificial. \
Nuestra meta es hacer que la toma de decisiones en el proceso de contratación sea más eficiente, certera y \
efectiva.")
    
    st.write("Prepárese para transformar la forma en que selecciona y contrata talento. Bienvenidos al futuro \
de la contratación.")
    
    lottie_trend = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_ZQqYEY.json")
    lottie_trend_file = load_lottiefile("trend.json")


elif selected == "NIA":
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None or api_key == "":
        st.error("OPENAI_API_KEY is not set. Please set it in the environment variables of your Streamlit Cloud app.")
        exit(1)

    # st.set_page_config(page_title="EMPLOYEE DATA")
    # st.header("VIDA LABORAL")
    st.markdown("<p style='font-size: 64px; font-weight: bold;'>NIA</p>", unsafe_allow_html=True)
    st.write("NIA fue entrenada con una base de datos de 35 empleados ejemplo, y es posible hacer preguntas sobre \
su historial de trabajo (vida laboral) utilizando lenguaje natural. \
NIA utilizará programación analítica e inteligencia artificial para brindar la mejor respuesta posible.")

    csv_file = r"Data_empleados.csv"
    fixed_file = r"Data_empleados_fixed.csv"

    # Fix accents and special characters in the CSV file
    with open(csv_file, "r", encoding="latin-1") as file:
        content = file.read()

    with open(fixed_file, "w", encoding="utf-8") as file:
        file.write(content)

    chat_model_to_use = OpenAI(temperature=0)

    agent = create_csv_agent(chat_model_to_use, 
                             fixed_file, 
                             verbose=True, 
                             prefix = "You are working with a pandas dataframe in Python. \
The name of the dataframe is `df`. Your final answer must be in Spanish language. If you don't know the answer say that, don't try to answer either way.\n\
You should use the tools below to answer the question posed of you:")

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
    st.write("\n")

    with st.expander("Ejemplos de preguntas para hacer"):
        st.write("1. ¿Cuántos empleados únicos hay en la base de datos?")
        st.write("2. Dime el historial laboral de Jorge Vales")
        st.write("3. ¿Cuántos empleos ha tenido Daniel Castro?")
        st.write("4. ¿Cuál es la edad promedio dentro de mi archivo?")
        st.write("5. ¿Cuál es la empresa que ha tenido mayor retención de empleados?")
    
    with st.expander("Funcionamiento"):
        st.write("La aplicación está cargada con una base de datos de 35 empleados ejemplo, la cual simula \
la unión entre bases de datos de comportamiento del empleado de empresas locales.")
        st.write("La intención del software NO es decidir, sino recomendar posibles candidatos basado en patrones \
de comportamiento que ha presentado el empleado a lo largo de su trayectoria laboral.")
        
        st.write("El software hace uso de nuestro proceso de análisis y recomendación simple, R.A.R.")

        st.markdown("<p style='font-size: 20px; font-weight: bold;'>R.A.R. = Recopilar - Analizar - Recomendar </p>", unsafe_allow_html=True)

        st.markdown("<p style='font-size: 16px; font-weight: bold;'>Recopilar</p>", unsafe_allow_html=True)
        st.write("Dentro de la primera etapa, Recopilar, se condensa la información proveniente de diversas bases de \
datos, se limpia y se estructura para poder analizarla correctamente.")
        
        st.markdown("<p style='font-size: 16px; font-weight: bold;'>Analizar</p>", unsafe_allow_html=True)
        st.write("La etapa Analizar abarca la combinación de programación analítica utilizando el lenguaje Python \
y el uso de inteligencia artificial para un entendimiento del resultado final con lenguaje natural.")
        
        st.markdown("<p style='font-size: 16px; font-weight: bold;'>Recomendar</p>", unsafe_allow_html=True)
        st.write("Recomendar, busca proporcionar resultados eficientes después de analizar grandes cantidades \
de información para que el tomador de decisiones pueda hacerlas de manera efectiva y precisa.")

    with st.expander("Nombres de algunos empleados ejemplo"):
        st.write("Andrea Moreno Herrera\n\
Ana Belén Medina López\n\
Jorge Eduardo Vales Cervantes\n\
Pedro Martínez García\n\
Victoria Ríos Sánchez\n\
Daniel Castro Vargas\n\
Ana María López Hernández\n\
Emilio Gutiérrez Navarro\n\
Valeria Domínguez Soto\n\
Luis Alberto Soto Ramírez")

elif selected == "Read.me":
    st.title("Read.me")

    st.write("John W. Gardner decía 'La excelencia es hacer las cosas ordinarias extraordinariamente bien', \
y creo que es totalmente cierto.")
    
    st.write("Este proyecto no solo busca reflejar el futuro de lo que será el análisis de contratación para la industria sino \
un destello de lo que será una inversión de bajo riesgo y altas ganancias en el futuro cercano. Y aunque esta \
descripción aplica para NIA Analytics, por este medio los invito a considerar una oportunidad que va más allá \
del proyecto en sí.")
    
    st.write("Dentro de unos meses estaré volando al otro lado del mundo a estudiar una maestría en Análisis de Negocios, \
en la Universidad de Essex, Inglaterra. Hoy en día hay financiamientos y becas otorgadas las cuales me ayudarán a avanzar \
")
    

    
    st.write("")

    with st.expander("Futuro"):
        st.image("Unconditional offer.png")