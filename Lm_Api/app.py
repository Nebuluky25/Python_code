from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# URL del API del modelo
LLM_API_URL = "http://192.168.0.104:1234/v1/chat/completions"

def env_prompt(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "local-mode",  # Ajusta esto según tu modelo de lenguaje
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 75,  # Reducción en el número de tokens
        "temperature": 0.5,  # Menos creatividad, más velocidad
        "n": 1,
        "stop": None,
    }

    try:
        print("Enviando la siguiente solicitud: ", data)
        print("URL del modelo: ", LLM_API_URL)

        respuesta = requests.post(LLM_API_URL, json=data, headers=headers)
        respuesta.raise_for_status()  # Eleva un error si ocurre un HTTP error

        print("Respuesta del modelo: ", respuesta.json())
        return respuesta.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
    except requests.exceptions.HTTPError as http_err:
        print("Error HTTP: ", http_err)
        return f"Error HTTP: {http_err}"
    except requests.exceptions.RequestException as e:
        print("Error al conectar con el modelo: ", str(e))
        return f"Error al conectar con el modelo: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.form.get("mensaje")

    if not mensaje:
        return jsonify({"error": "No se proporcionó el campo 'mensaje'"}), 400

    prompt = (f"Eres un asistente conversacional al estilo de ChatGPT. "
              f"Responde de manera amigable y clara a la siguiente pregunta: '{mensaje}'")

    respuesta_ia = env_prompt(prompt)

    return render_template_string("""
        <h1>Chatbot LLM</h1>
        <form action="/chat" method="post">
            <input type="text" name="mensaje" placeholder="Escribe tu mensaje aquí" required>
            <button type="submit">Enviar</button>
        </form>
        <h2>Respuesta:</h2>
        <pre>{{ respuesta }}</pre>
    """, respuesta=respuesta_ia)

@app.route("/", methods=["GET"])
def home():
    return render_template_string("""
        <h1>Chatbot LLM</h1>
        <form action="/chat" method="post">
            <input type="text" name="mensaje" placeholder="Escribe tu mensaje aquí" required>
            <button type="submit">Enviar</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
    print("Aplicación en ejecución.")