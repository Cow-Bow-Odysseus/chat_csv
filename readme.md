# Instalación

Para ejecutar el proyecto es recomendable seguir las siguientes indicaciones:

**Importante**: Asegurarse que en el archivo **.env** la API Key de OAI registrada tenga acceso al modelo de GPT-3.5.

Para **VSCode**:

En una terminal del sistema (CMD):
1. `cd Proyect_folder` Entramos a la ruta del folder del Proyecto.
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
1. `cd Proyect_folder` Entramos a la ruta del folder del Proyecto.
2. `python -m venv env` Esto para crear un ambiente virtual. (**Asumo que tienen Python > 3.8**)
3. `env\Scripts\activate.bat` Para activar el ambiente virtual.
4. `pip install -r requirements.txt -q` Para instalar las dependencias.
5. `code .` Para abrir el editor de código.
6. En el archivo `.env` de variable de entorno, anotar la API_Key de OAI.

7. En otra terminal del sistema (CMD):
    1. `cd Proyect_folder` Entramos a la ruta del folder del Proyecto.
    2. `env\Scripts\activate.bat` Para activar el ambiente virtual.
    3. Con el ambiente activo, se va a ejecutar el API del servicio FastAPI de la siguiente forma:
    `py .\back_end.py`

    Aquí podemos ver los **logs cuando se hagan peticiones** a la API.

    Podemos acceder a la ruta ` http://127.0.0.1:8000\docs` para ver el Swagger con los métodos.

8. En otra terminal del sistema (CMD):
    1. `cd Proyect_folder` Entramos a la ruta del folder del Proyecto.
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

# Flow of Interaction
Al ingresar un mensaje, ese pasa por el **clasificador**, este determina si va a responder de manera genérica o si va a usar la herramientas del **agent** para ejecutar comando sobre el dataframe. Supongamos que la pregunta es acerca del df, entonces esta la pasa a el **agent** el cual ejecuta los comandos necesarios para responder y devuelve la respuesta en ingles, esta respuesta se manda como `input` a el **conversation_**, este tiene 2 objetivos principales, responder a los mensajes genéricos, traducir los mensajes y darles formatos necesarios salidos del **agent**, y mantener una memoria de la sesión.

El sistema responde cosas sencillas como **Cuál es el valor total de las propiedades de tipo "for sale"?**, **Cuál es el valor de las propiedades en renta?**, **Dame el precio promedio de las propiedades?**. Se puede ampliar el catálogo de operaciones así como la complejidad realizando un custom_agent pero requiere de más tiempo/scripting.

