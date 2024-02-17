# API Tools 
import requests
import json

# Streamlit Tools
import streamlit as st
import numpy as np

# UI configs
st.set_page_config(page_title="Document Assistant", page_icon="📃", layout="wide")
st.title("Document Assistant")


def clear_chat_history():
    """Sirve para eliminar los mensajes mostrados y los mensajes de la memoria"""
    # Set default message sesion
    st.session_state.messages = [{"role": "assistant", "content": "Cómo te puedo ayudar?"}]

    # Clean Messages in Mem
    requests.get(url = 'http://127.0.0.1:8000/delete_memory')

# User Name
if "user" not in st.session_state:
        st.session_state["user"] = "DD360-User"

# Barra desplegable
my_sdbar = st.sidebar
with my_sdbar:
    st.title("Herramientas")
    st.session_state["user"] = st.text_input(label= "Nombre de usuario", value= st.session_state["user"], key= "user_name")
    my_sdbar.button('Clear Chat History', on_click=clear_chat_history)


# Guarda los elementos del chat
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Cómo te puedo ayudar?"}]

# Desplegar los mensajes en la pantalla
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Prompt es el input o mensaje del usuario
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generar un nuevo mensaje si el ultimo mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Formato para hacer el request
            inputs = {"msg_input": prompt}

            try:
                # Se hace la llamada a FastAPI (este debe estar prendido y asgurar que esta en esa ruta)
                # Si se ejectó en otra ruta, cambiar la url
                Answer = requests.post(url = 'http://127.0.0.1:8000/mensajes', data = json.dumps(inputs))
                # Formatear el string
                Answer = Answer.text.replace(r'\n', '\n').replace('"','')
            except:
                 Answer= "El servicio de FastAPI no esta ejecutado. Iniciar el servidor con: py back_end.py"

            placeholder = st.empty()
            placeholder.markdown(Answer)
    
    # Asignar el contenido de la respuesta
    message = {"role": "assistant", "content": Answer}

    # Sirve para indicar los mensajes que se van a desplegar
    # Se puede cambiar el integer para mostrar más o menos mensajes
    st.session_state.messages = st.session_state.messages[-6:]

    # Anexamos la última respuesta
    st.session_state.messages.append(message)


