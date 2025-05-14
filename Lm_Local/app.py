from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# URL del API del modelo
LLM_API_URL = "Introduce la url correspondiente"

def env_prompt(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "local-mode",  
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,  
        "temperature": 0.9, 
        "n": 1,
        "stop": None,
    }

    try:
        respuesta = requests.post(LLM_API_URL, json=data, headers=headers)
        respuesta.raise_for_status()

        return respuesta.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err}"
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con el modelo: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.form.get("mensaje")

    if not mensaje:
        return jsonify({"error": "No se proporcionó el campo 'mensaje'"}), 400

    prompt = (f"Eres un especialista en inteligencia artificial. "
              f"Explica las mejores prácticas para el despliegue de un modelo de lenguaje local, "
              f"incluyendo advertencias sobre su uso y requerimientos de infraestructura.")

    respuesta_ia = env_prompt(prompt)

    return render_template_string("""
        <h1>Chatbot Despliegue LLM Local</h1>
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
        <h1>Chatbot Despliegue LLM Local</h1>
        <form action="/chat" method="post">
            <input type="text" name="mensaje" placeholder="Escribe tu mensaje aquí" required>
            <button type="submit">Enviar</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)  
