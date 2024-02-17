##################################################################################
# Definimos las dependencias necesarias
# Load extra utils
import utils as utls

# Fast API 
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# LLM Tools
import openai
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
# LLM Experimental for csv
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents.agent_types import AgentType

# File Tools
import pandas as pd

# Load Env variables
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

##################################################################################
# Define la clase para el input en mensajes
class media_inputs(BaseModel):
    # Con esto nos aseguramos que el input sea una lista
    msg_input: str

##################################################################################
# Definimos el handler para la API
app = FastAPI()

@app.get("/")
def welcome():
    """Solo es un saludo de bienvenida."""
    welcome_msg = """Bienvenido a la sección root de su aplicación de asistente en archivos csv. Para probar el swagger de la documentación, ingrese a la siguiente ruta -> http://127.0.0.1:8000/docs"""
    return welcome_msg

@app.post("/mensajes")
def root(inputs:media_inputs):
    """
    Con esta función devolvemos respuesta al usuario usando Chatgpt . \n
    Importante que exista la API Key como variable de entorno en el archivo `.env` \n

    Argumentss: \n
        - msg_input: Mensaje del usuario. \n

    Return:  \n
        - Regresa una respuesta en formato `str` al usuario. \n
    """
    # Capturamos la entrada de mensajes
    user_msg = inputs.msg_input

    # Pasamos el mensaje por el clasificador:
    msg_class = classifier_.predict(human_input = user_msg)

    # Dependiendo de la clase asignamos la actividad
    if msg_class == "GENÉRICO":
        print(f"Route in {msg_class}")
        # Se contesta el mensaje
        answer = conversation_.predict(human_input= user_msg)
    elif msg_class == "DATA":
        print(f"Route in {msg_class}")
        # Por default el agent responde en inglés
        # Se espera que el mensaje sea lo más claro y no ambiguo (ej. Cuál es el precio?)
        raw_answer = agent.run(user_msg)
        print(raw_answer)
        # Tomamos la salida para traducirla y darle formatos
        answer = conversation_.predict(human_input= raw_answer)
    else:
        print(f"Without Route")
        # Se contesta el mensaje que no se asigno a ninguna clase
        answer = conversation_.predict(human_input= user_msg)
    
    return answer

@app.get("/delete_memory")
def delete_mem():
    """
    Este método solo sirve para eliminar la memoria existente.

    Return:
    - log_info = Mensaje de status
    """
    try:
        conversation_.memory.clear()
        log_info = "Se logró eliminar los mensajes en la memoria."
    except:
        log_info = "No se logró eliminar los mensajes en la memoria."

    return log_info

@app.get("/memory_info")
def memory_info():
    """
    Este método solo sirve para consultar los mensajes en la memoria existente.

    Return:
    - log_info = Mensaje con el número de las N conversaciones guardadas.
    """
    try:
        # conversation_.memory.buffer_as_messages regresa la lista de mensajes
        msgs_in_mem = len(conversation_.memory.buffer_as_messages)
        log_info = f"Existen {msgs_in_mem} mensajes en la memoria."
    except:
        log_info = "No existen mensajes en la memoria."

    return log_info

##################################################################################
# Al ejecutar FastAPI (Servidor) le pedimos cargar los "agentes"
if __name__ == "__main__":
    classifier_ = LLMChain(
        # Configuraciones, OAI Key, Model, Temperature (Creatividad)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
        # Template de funcionamiento
        prompt = utls.assi_prompt)
    
    conversation_ = LLMChain(
        # Configuraciones, OAI Key, Model, Temperature (Creatividad)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
        # Template de funcionamiento
        prompt = utls.prompt_temp,
        # Eliminamos los callback de OpenAI
        verbose = False,
        # K = El número entero indica el máximo número de pares de mensajes a guardar (3 = 6 mensajes de memoria)
        memory = ConversationBufferWindowMemory(k= 3 ,memory_key="chat_history", input_key="human_input"))

    agent = create_csv_agent(
        # Configuraciones, Model, Temperature (Creatividad)
        OpenAI(temperature=0.1),
        # Carga del CSV (Solo se ejecuta 1 vez al iniciar FastApi)
        "./listings.csv",
        # Eliminamos los callback de OpenAI
        verbose=False,
        # ZeroShot hace referencia a preguntas "sin" contexto previo
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    
    # Por default la app se ejecuta en el local host = http://127.0.0.1:8000/ 
    uvicorn.run(app, port=8000)