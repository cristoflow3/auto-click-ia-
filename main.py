import os
import threading
import time
import tkinter as tk

import pyautogui
import requests
from supabase import create_client

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase_client = (
    create_client(SUPABASE_URL, SUPABASE_KEY)
    if SUPABASE_URL and SUPABASE_KEY
    else None
)


def query_openrouter(prompt: str) -> str:
    """Send a simple prompt to OpenRouter and return the response text."""
    if not OPENROUTER_API_KEY:
        return "OpenRouter key not configured."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return f"OpenRouter error: {exc}"


def log_action(action: str) -> None:
    """Store a simple log entry in Supabase if configured."""
    if supabase_client:
        try:
            supabase_client.table("logs").insert({"action": action}).execute()
        except Exception:
            pass


def crew_example() -> str:
    """Demonstrate running a basic CrewAI agent."""
    try:
        from crewai import Agent, Crew

        agent = Agent(name="Helper", instructions="Saluda al mundo")
        crew = Crew(agents=[agent], tasks=["Di hola"], verbose=False)
        return crew.kickoff()
    except Exception as exc:
        return f"CrewAI error: {exc}"


class AutoClickApp:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Auto Click AI")
        self.running = False

        tk.Label(master, text="Intervalo (s):").grid(row=0, column=0)
        self.interval_entry = tk.Entry(master)
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.grid(row=0, column=1)

        tk.Label(master, text="Mensaje IA:").grid(row=1, column=0)
        self.prompt_entry = tk.Entry(master)
        self.prompt_entry.grid(row=1, column=1)

        self.start_button = tk.Button(master, text="Iniciar", command=self.start)
        self.start_button.grid(row=2, column=0)
        self.stop_button = tk.Button(master, text="Detener", command=self.stop)
        self.stop_button.grid(row=2, column=1)

        self.output = tk.Text(master, height=8, width=50)
        self.output.grid(row=3, column=0, columnspan=2)

    def start(self) -> None:
        if not self.running:
            self.running = True
            threading.Thread(target=self.run, daemon=True).start()

    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        interval = float(self.interval_entry.get())
        prompt = self.prompt_entry.get().strip()
        if prompt:
            reply = query_openrouter(prompt)
            self.output.insert(tk.END, f"IA: {reply}\n")
            log_action(f"prompt: {prompt}")
        crew_msg = crew_example()
        if crew_msg:
            self.output.insert(tk.END, f"CrewAI: {crew_msg}\n")
        while self.running:
            pyautogui.click()
            log_action("click")
            time.sleep(interval)


def main() -> None:
    root = tk.Tk()
    app = AutoClickApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

