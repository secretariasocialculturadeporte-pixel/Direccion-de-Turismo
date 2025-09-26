# Proyecto de Turismo de Puerto Gaitán

Este es un proyecto full-stack que consiste en un backend de Django y un frontend de Next.js, diseñado para gestionar y mostrar información turística de Puerto Gaitán. El sistema incluye un directorio de prestadores de servicios, publicaciones, atractivos turísticos y un sistema de agentes de IA basado en LangChain para la gestión automatizada de tareas.

## Requisitos Previos

- Python 3.10+
- Node.js 18+
- `pip` para la gestión de paquetes de Python
- `npm` para la gestión de paquetes de Node.js

## Configuración del Backend

1.  **Navegar al directorio del backend:**
    ```bash
    cd backend
    ```

2.  **Instalar las dependencias de Python:**
    Se recomienda crear y activar un entorno virtual primero.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Instalar dependencias adicionales de MFA:**
    El sistema utiliza autenticación de múltiples factores que requiere una dependencia adicional.
    ```bash
    pip install fido2
    ```

4.  **Ejecutar las migraciones de la base de datos:**
    Esto creará el esquema de la base de datos SQLite.
    ```bash
    python manage.py migrate
    ```

5.  **Poblar la base de datos con datos iniciales:**
    Este script crea las categorías, usuarios de prueba y algunos registros de ejemplo.
    ```bash
    python manage.py shell < ../create_data.py
    ```

6.  **Ejecutar el servidor del backend:**
    El servidor de desarrollo de Django (`runserver`) tiene un problema que causa que se cuelgue. Se debe utilizar `uvicorn`.

    Primero, instala `uvicorn`:
    ```bash
    pip install uvicorn
    ```

    Luego, ejecuta el servidor:
    ```bash
    uvicorn puerto_gaitan_turismo.asgi:application --host 127.0.0.1 --port 8000
    ```
    El backend estará disponible en `http://127.0.0.1:8000`.

## Configuración del Frontend

1.  **Instalar las dependencias de Node.js:**
    Desde el directorio raíz del proyecto:
    ```bash
    npm install --prefix frontend
    ```

2.  **Ejecutar el servidor de desarrollo del frontend:**
    ```bash
    npm run dev --prefix frontend
    ```
    El frontend estará disponible en `http://localhost:3000`.

## Pruebas

### Pruebas Funcionales

Una vez que ambos servidores (backend y frontend) estén en funcionamiento, puedes navegar a `http://localhost:3000` para probar la aplicación.

**Flujos de usuario a probar:**
- Visualizar la lista de prestadores de servicios.
- Filtrar prestadores por categoría.
- Registrar un nuevo usuario (prestador o turista).
- **Nota:** El inicio de sesión está actualmente roto.

### Pruebas del Agente de IA

El sistema de agentes de IA puede ser probado a través de un comando de gestión personalizado. Este comando simula una orden para el agente y ejecuta la cadena de mando completa.

Para ejecutar la prueba, utiliza el siguiente comando desde el directorio `backend`:
```bash
python manage.py test_agent
```
El comando mostrará en la consola el progreso del agente y el informe final de la misión.

## Problemas Conocidos

- **Inicio de sesión de usuarios:** El flujo de inicio de sesión no funciona actualmente. Devuelve un error de "credenciales no válidas" incluso con los datos correctos. Esto parece ser un problema de configuración profundo entre `django-allauth` y `dj-rest-auth` que requiere más investigación.
- **Servidor de desarrollo de Django:** El comando `runserver` se cuelga al iniciar. Se debe usar `uvicorn` como solución alternativa para el desarrollo.
- **Dependencia `fido2`:** La dependencia `fido2` es necesaria para la autenticación MFA pero no estaba en `requirements.txt`. Ha sido instalada manualmente como parte de estas instrucciones.
- **Dependencia de LLM en Agentes:** Los agentes de IA están diseñados para usar un LLM (como GPT-4o) para la planificación. En ausencia de una clave de API de OpenAI, los agentes utilizan planes de contingencia simulados para permitir la prueba de la ejecución de herramientas. Para una funcionalidad completa, se debe configurar la variable de entorno `OPENAI_API_KEY`.