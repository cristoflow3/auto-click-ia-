# auto-click-ia-

Aplicación sencilla para Windows que combina Python, OpenRouter, CrewAI y Supabase.

## Requisitos

- Python 3.10+
- Dependencias: `pip install -r requirements.txt`
- Variables de entorno (opcional):
  - `OPENROUTER_API_KEY` para usar el modelo de OpenRouter y como backend de CrewAI.
  - `SUPABASE_URL` y `SUPABASE_KEY` para registrar acciones.

## Uso

```bash
python main.py
```

La interfaz permite definir el intervalo de clics y un mensaje para la IA.
Al iniciar, el programa:
1. Consulta OpenRouter con el mensaje proporcionado.
2. Lanza una pequeña conversación multiagente con CrewAI (Planificador y Ejecutor).
3. Repite clics automáticos con `pyautogui`.
4. Registra acciones en Supabase si está configurado.

> Prueba este proyecto y adáptalo a tus necesidades.
