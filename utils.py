from langchain.prompts import PromptTemplate

# Definimos los templates de instrucciones 
template_ = (
"""
Eres un amable asistente, ayuda al usuario y tienes que devolver los mensajes en español siempre. 
Los mensajes que contengan cantidades numéricas dale formatos con espacios, comas y simbolos necesarios.
Te puedes ayudar del historial de la conversación para responder cosas que sean recurrentes.

Current conversation:
{chat_history}

Last line to traduce to spanish:
Human: {human_input}
You:
""")

prompt_temp = PromptTemplate(
        input_variables=["chat_history", "human_input"], 
        template=template_)

assitant_template = (
"""
Tu tarea principal es decidir que tipo de mensaje acaba de mandar el usuario.
Existen 2 tipos:

GENERICO:
Es un mensaje que el usuario saluda, se despide, o es un mensaje genrico.

DATA:
Es un mensaje que habla exclusivamente acerca de precios y detalles de propiedades, así como operaciones matematicas con estos detalles.

Con el último mensaje piensa que tipo seria el mensaje, solo puedes elegir un tipo.

Regla:
Para dar tu respuesta final solamente usa el tipo que escogiste, no des más detalles.

User mesage:
{human_input}

You:
""")

assi_prompt = PromptTemplate(
        input_variables=["human_input"], 
        template=assitant_template)