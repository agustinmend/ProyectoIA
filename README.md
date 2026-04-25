# Sistema de Seguridad Activa con IA: Detección de Intrusos mediante Estimación de Posturas

Este proyecto transforma una cámara de vigilancia convencional en un sensor inteligente capaz de detectar intrusiones perimetrales (escalamiento de muros) en tiempo real. Utiliza modelos de aprendizaje automático basados en geometría articular.

##  El Problema
Las cámaras de seguridad tradicionales son dispositivos pasivos que solo graban video. Los detectores de movimiento convencionales (VMD) basados en cambios de píxeles generan una tasa inaceptable de falsos positivos debido a sombras, lluvia o movimiento de vegetación. Este sistema resuelve esto mediante el análisis semántico de la postura humana.

## Arquitectura del Sistema
El proyecto emplea un diseño desacoplado para optimizar el rendimiento y la fiabilidad:

1.  **Sensor de Visión (Frontend - JavaScript/TensorFlow.js):**
    * Ejecuta el modelo **PoseNet** mediante WebGL para procesamiento en tiempo real.
    * **Filtro de Persistencia Temporal:** Implementa una lógica de validación de 10 fotogramas continuos para eliminar detecciones prematuras o ruidos visuales momentáneos.
    * Captura de "Imagen Limpia": Utiliza un canvas oculto para capturar al intruso sin el dibujo del esqueleto, facilitando su identificación.

2.  **Controlador de Alertas (Backend - Python/Flask):**
    * Servidor asíncrono que recibe alertas mediante peticiones POST (Base64).
    * Integración con **Discord Webhooks** para notificaciones instantáneas con evidencia fotográfica.
    * Gestión de *Cooldown* para prevenir la saturación de alertas en el canal de comunicación.

## 📊 Dataset y Entrenamiento
Se utilizó un enfoque de **Transfer Learning** sobre una arquitectura binaria asimétrica para optimizar la detección de anomalías:

* **Dataset Total:** 1600 imágenes de entrenamiento.
* **Clase Trepando (400 muestras):** Enfoque estricto en vectores de suspensión e impulso final, eliminando fotogramas de transición.
* **Clase Normal (1200 muestras):** Inclusión de **Casos Adversarios** (sujetos saludando, sentados o estirándose) para mapear exhaustivamente el espacio inofensivo y reducir la tasa de falsas alarmas.

## Instalación y Uso

### Requisitos Previos
* Python 3.10+
* Navegador Chrome o Edge (para soporte WebGL)

### Configuración
1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/agustinmend/ProyectoIA
    cd Codigo
    ```
2.  **Instalar dependencias:**
    ```bash
    pip install flask requests flask-cors
    ```
3.  **Configurar Webhook:** Edita la variable `DISCORD_WEBHOOK_URL` en `servidor.py` con tu enlace de Discord.

### Ejecución
Para poner en marcha el sistema, abre dos terminales en la raíz del proyecto:

* **Terminal 1 (Backend):**
    ```bash
    python servidor.py
    ```
* **Terminal 2 (Frontend):**
    ```bash
    python -m http.server 8000
    ```
Accede a `http://localhost:8000` en tu navegador y activa la cámara.

---
**Autor:** Agustín - Santa Cruz de la Sierra, Bolivia.
