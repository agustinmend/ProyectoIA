from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import time

app = Flask(__name__)
CORS(app)

# ==========================================
# CONFIGURACIÓN DE DISCORD
# ==========================================
# Pega aquí la URL exacta que copiaste de Discord
DISCORD_WEBHOOK_URL = "Url Exacta del bot de discord"
COOLDOWN = 10
ultima_alerta = 0

@app.route('/alerta', methods=['POST'])
def manejar_alerta():
    global ultima_alerta
    ahora = time.time()
    
    if (ahora - ultima_alerta) < COOLDOWN:
        return jsonify({"status": "ignorado_por_cooldown"}), 200

    datos = request.json
    if not datos or 'imagen' not in datos:
        return jsonify({"error": "No hay imagen"}), 400

    # Decodificar y guardar la imagen localmente
    imagen_b64 = datos['imagen'].split(",")[1]
    ruta_imagen = "intruso.jpg"
    with open(ruta_imagen, "wb") as f:
        f.write(base64.b64decode(imagen_b64))

    # ==========================================
    # ENVÍO A DISCORD (Más simple que Telegram)
    # ==========================================
    with open(ruta_imagen, "rb") as foto:
        payload = {
            "content": "🚨 **ALERTA DE SEGURIDAD**: Se ha detectado un intruso trepando."
        }
        archivos = {
            "file": ("intruso.jpg", foto, "image/jpeg")
        }
        
        # Hacemos el POST directo a la URL de Discord
        respuesta = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=archivos)

    if respuesta.status_code in [200, 204]:
        print("[EXITO] Foto enviada a Discord.")
    else:
        print(f"[ERROR] Falló Discord. Código: {respuesta.status_code}")

    ultima_alerta = ahora
    return jsonify({"status": "alerta_enviada"}), 200

if __name__ == '__main__':
    print("Servidor listo. Esperando alertas del navegador...")
    app.run(port=5000)