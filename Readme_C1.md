# Instalación

Para ejecutar el proyecto es recomendable seguir las siguientes indicaciones:

**Importante**: Asegurarse que en el archivo **.env** la API Key de OAI registrada tenga acceso al modelo de GPT-3.5.

Para **VSCode**:

En una terminal del sistema (CMD):
1. `cd Proyect_folder(Challenge1)` Entramos a la ruta del folder del Proyecto.
2. `python -m venv env` Esto para crear un ambiente virtual. (**Asumo que tienen Python > 3.8**)
3. `env\Scripts\activate.bat` Para activar el ambiente virtual.
4. `pip install -r requirements.txt -q` Para instalar las dependencias.
5. `code .` Para abrir el editor de código.
6. En el archivo `.env` de variable de entorno, anotar la API_Key de OAI.

7. Con una terminal ejecutar el API (dentro de la terminal de vscode debe estar activo el ambiente, se puede activar como `env\Scripts\Activate.Ps1`) del servicio FastAPI de la siguiente forma:
`py .\back_end.py`

Aquí podemos ver los **logs cuando se hagan peticiones** a la API.

Podemos acceder a la ruta ` http://127.0.0.1:8000\docs` para ver el Swagger con los métodos.

8. En otra terminal (dentro de la terminal de vscode debe estar activo el ambiente, se puede activar como `env\Scripts\Activate.Ps1`) ejecutamos la Interfaz de usuario:
`streamlit run .\front_end.py`

Aquí podemos interactuar de manera más amigable con la API del backend.

Si no se abre de manera automática la app, hay que abrir la ruta `http://localhost:8501` en el navegador.

---
Para **CMD**:

En una terminal del sistema (CMD):
1. `cd Proyect_folder(Challenge1)` Entramos a la ruta del folder del Proyecto.
2. `python -m venv env` Esto para crear un ambiente virtual. (**Asumo que tienen Python > 3.8**)
3. `env\Scripts\activate.bat` Para activar el ambiente virtual.
4. `pip install -r requirements.txt -q` Para instalar las dependencias.
5. `code .` Para abrir el editor de código.
6. En el archivo `.env` de variable de entorno, anotar la API_Key de OAI.

7. En otra terminal del sistema (CMD):
    1. `cd Proyect_folder(Challenge1)` Entramos a la ruta del folder del Proyecto.
    2. `env\Scripts\activate.bat` Para activar el ambiente virtual.
    3. Con el ambiente activo, se va a ejecutar el API del servicio FastAPI de la siguiente forma:
    `py .\back_end.py`

    Aquí podemos ver los **logs cuando se hagan peticiones** a la API.

    Podemos acceder a la ruta ` http://127.0.0.1:8000\docs` para ver el Swagger con los métodos.

8. En otra terminal del sistema (CMD):
    1. `cd Proyect_folder(Challenge1)` Entramos a la ruta del folder del Proyecto.
    2. `env\Scripts\activate.bat` Para activar el ambiente virtual.
    3. Aquí ejecutamos la Interfaz de usuario:
    `streamlit run .\front_end.py`

    Aquí podemos interactuar de manera más amigable con la API del backend.

    Si no se abre de manera automática la app, hay que abrir la ruta `http://localhost:8501` en el navegador.

---
# Funcionamiento
Se divide en 3 capas de **agentes**:

1. El **clasificador** muestra de que tipo es el mensaje y a que **"actividad"** mandarlo. (Similar a MoE)
2. El **conversation_** es un intermediario que use para traducir la respuesta del agente y contestar consultas genéricas del usuairo o que se pueden contestar desde el uso del chat-history.
3. El **agent** es un desarrollo para poder interactuar con archivos .csv con lenguaje natural (por defecto responde en inglés), usando como backbone OpenAI. En un desarrollo con más tiempo se pueden personalizar más actividades sobre el .csv. En el trasfondo se ejecuta código para realizar las operaciones.
    3.1 El agent en operaciones muy complejas frena el procesamiento para no saturar la memoria.

## Flow of Interaction
Al ingresar un mensaje, ese pasa por el **clasificador**, este determina si va a responder de manera genérica o si va a usar la herramientas del **agent** para ejecutar comando sobre el dataframe. Supongamos que la pregunta es acerca del df, entonces esta la pasa a el **agent** el cual ejecuta los comandos necesarios para responder y devuelve la respuesta en ingles, esta respuesta se manda como `input` a el **conversation_**, este tiene 2 objetivos principales, responder a los mensajes genéricos, traducir los mensajes y darles formatos necesarios salidos del **agent**, y mantener una memoria de la sesión.

El sistema responde cosas sencillas como **Cuál es el valor total de las propiedades de tipo "for sale"?**, **Cuál es el valor de las propiedades en renta?**, **Dame el precio promedio de las propiedades?**. Se puede ampliar el catálogo de operaciones así como la complejidad realizando un custom_agent pero requiere de más tiempo/scripting.

## Streamlit
Sirve como Interfaz de Usuario personalizable, pero **se pueden usar otros framework basados en Python (Taipy) o Java (Vue)**. Pero almenos para el caso de Java toma más tiempo de desarrollo. Y en términos de tiempo, Streamlit es más rápido de montar.

---
# Notas

## Por qué OpenAI y no un modelo Local?

El **modelo base usado fue GPT-3.5-Turbo, el cuál tiene 175 billones de parámetros.** Actualmente hay modelos locales que funcionan de manera similar como lo es Falcon180B, Mixtral-8x7B, MPT30B. Desafortunadamente estos ocuapan recursos GPU altos para poder ejecutarse en local, por ejemplo: Falcon180B (400GB RAM), Mixtral-8x7B (64GB of RAM), MPT30B (1xA100-80GB). Y la capa gratuita de **Google Colab** solo corre con ciertas dificultades **Mixtral-8x7B**, los demás requieren instancias especializadas.

Si se cuentan con los recursos se pueden usar esos modelos mencionados para repetir esta Demo.

## Por qué no un modelo más pequeño?

Existen versiones cuantizadas a 2,3,4,8,16 bits de dichos modelos (no todos) así como de muchos otros más, el problema surge en la precisión, pues las salidas de inferencia corren el riesgo de alucinaciones, duplicate tokens y falta de generalización del modelo generando **malas** respuestas. Además de que a pesar de la cuantización, aún necesitan recursos GPU.

## Por qué no un modelo aún más pequeño?

Esta actividad de puede realizar usando **Deberta-v3-large-squad2**, con las indicaciones adecuadas podemos hacer que indetifique entidades y intecinón y así poder hacer preguntas de manera natural, pero este modelo **no genera texto**, por lo que las repuestas serán más planas, y a medida que se quieran más operaciones hay que hacer más scripting. 

## Aproximaciones opcionales

Dependiendo del caso y la situación se puede optar de manera general por los siguientes modelos:

1. **Microsoft Open AI Service**: Permite mantener la seguridad de los datos, pues no se comparten en ningun momento. Además el servicio vive del lado de MSFT y no de OpenAI.
2. **OpeanAI / Anthropic / MPT Databricks**: Permite usar su API sin tener que gestionar recursos de GPU. Los costos a medida de la oferta tenderan a bajar. Los modelos son a gran escala permitiendo gran variedad de actividades, sumado a que algunos ya son multimodales.
3. **Falcon180B, Mixtral-8x7B, LLama-13b**: Son modelos que usan recursos GPU, pero al tener los pesos en instancias locales aseguramos la protección de la información pues no sale de nuestro ambiente.

## Métodos usados en la API
Los métodos get son complementarios para actividades de eliminar u obtener la infromación.
El método post es el que ejecuta la actvidad principal de conectarse a el LLM y generar la respuesta. 

## Langchain
Es de los mejores frameworks para trabajar con LLM´s así como **LLama Index**. Sumado a eso, ya se tienen herramientas para facilitar actividades de RAG. En caso de querer hacer finetunnig de modelos se tiene que pasar por otros frameworks y pasos.

## Mejoras ⏫
Es posible mejorar las salidas al chatear con 1 o más files, mediante el uso de vector stores para almacenar conocimiento recurrente. Usar agentes especializados para las actividades de interacción con el archivo. Usar un balanceo de modelos y tareas async para asegurar el uso intensivo (caso para una app web o "atención" al cliente.)