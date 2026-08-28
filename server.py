
from flask import Flask, request, jsonify, send_from_directory
from google import genai
import os

app = Flask(__name__)

PORT = 5000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_KEY = os.getenv("GEMINI_API_KEY")

MUSIC_FOLDER = os.path.join(
    BASE_DIR,
    "assets",
    "sounds",
    "2026 - Hazbin - Hotel (exit song)"
)

IMAGE_FOLDER = os.path.join(
    BASE_DIR,
    "assets",
    "images"
)


# ==========================================
# GEMINI
# ==========================================

if not API_KEY:
    print("⚠️ No se encontró GEMINI_API_KEY.")
    client = None
else:
    client = genai.Client(api_key=API_KEY)
    print("✅ API de Gemini detectada.")


# ==========================================
# PÁGINA
# ==========================================

@app.route("/")
def inicio():
    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# ==========================================
# IMÁGENES
# ==========================================

@app.route("/assets/images/<path:filename>")
def images(filename):
    return send_from_directory(
        IMAGE_FOLDER,
        filename
    )


# ==========================================
# MÚSICA
# ==========================================

@app.route("/assets/music/<path:filename>")
def music(filename):
    return send_from_directory(
        MUSIC_FOLDER,
        filename
    )


# ==========================================
# CHAT GEMINI
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():

    if client is None:
        return jsonify({
            "response": "No tengo conectada la API de Gemini."
        }), 500

    datos = request.get_json()

    mensaje = datos.get(
        "message",
        ""
    ).strip()

    if not mensaje:
        return jsonify({
            "response": "No recibí ningún mensaje"
        })

    try:

        prompt = f"""
Eres VOX, un asistente personal.

Hablas español.

Tu personalidad:
- Amigable
- Natural
- Inteligente
- Divertida
- Directa
- Puedes hablar de música,
  videojuegos, tecnología y temas cotidianos.

El usuario dijo:

{mensaje}

Responde como VOX.
"""

        respuesta = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return jsonify({
            "response": respuesta.output_text
        })

    except Exception as error:

        print(
            f"❌ Error Gemini: {error}"
        )

        return jsonify({
            "response":
            "Tuve un problema conectándome con Gemini."
        }), 500


# ==========================================
# INICIO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("              VOX WEB v0.1")
    print("=" * 50)

    print(
        f"🌐 Servidor: http://localhost:{PORT}"
    )

    print(
        "🎵 Música:",
        MUSIC_FOLDER
    )

    print(
        "🖼️ Fondo:",
        IMAGE_FOLDER
    )

    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )

