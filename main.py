import os
import threading
import tkinter as tk

from PIL import Image, ImageTk
import pyttsx3

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


# Check API key
if "GROQ_API_KEY" not in os.environ:
    raise RuntimeError("Missing GROQ_API_KEY")


# AI personality
prompt = PromptTemplate.from_template(
    """
You are VOID-45, a friendly AI companion.

Rules:
- Speak naturally and casually
- Be supportive and calm
- Keep responses short to medium length
- Ask follow-up questions sometimes
- Never give harmful advice
- Do not pretend to be human

Conversation:
{chat_history}

User:
{question}

VOID-45:
"""
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4
)

chain = prompt | model


# Voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Store conversation history
chat_history = []


def generate_response(user_text):
    history_text = "\n".join(chat_history[-10:])

    response = chain.invoke({
        "question": user_text,
        "chat_history": history_text
    })

    return response.content


def send_message():
    user_text = input_box.get("1.0", tk.END).strip()

    if not user_text:
        return

    input_box.delete("1.0", tk.END)

    output_label.config(text="VOID-45 is thinking...")

    chat_history.append(f"User: {user_text}")

    def run():
        try:
            answer = generate_response(user_text)

            chat_history.append(f"VOID-45: {answer}")

            output_label.config(text=answer)

            speak(answer)

        except Exception:
            output_label.config(
                text="VOID-45 ran into a problem."
            )

    threading.Thread(target=run, daemon=True).start()


# Main window
root = tk.Tk()

root.title("VOID-45")
root.attributes("-fullscreen", True)
root.configure(bg="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Background image
bg_image = Image.open("void45_bg.png")
bg_image = bg_image.resize((screen_width, screen_height))

bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(
    root,
    width=screen_width,
    height=screen_height,
    highlightthickness=0
)

canvas.pack(fill="both", expand=True)

canvas.create_image(
    0,
    0,
    image=bg_photo,
    anchor="nw"
)


# Chat output
output_label = tk.Label(
    root,
    text="VOID-45 online.",
    fg="cyan",
    bg="black",
    font=("Consolas", 14),
    wraplength=screen_width - 100,
    justify="left"
)

canvas.create_window(
    screen_width // 2,
    screen_height - 220,
    window=output_label
)


# User input
input_box = tk.Text(
    root,
    height=4,
    font=("Consolas", 14),
    bg="black",
    fg="cyan",
    insertbackground="cyan",
    wrap="word"
)

canvas.create_window(
    screen_width // 2,
    screen_height - 120,
    window=input_box,
    width=screen_width - 200
)


# Send button
send_button = tk.Button(
    root,
    text="SEND",
    command=send_message,
    font=("Consolas", 13, "bold"),
    bg="black",
    fg="cyan",
    activebackground="black",
    activeforeground="cyan",
    bd=1
)

canvas.create_window(
    screen_width // 2,
    screen_height - 50,
    window=send_button
)


# Exit app with ESC
root.bind("<Escape>", lambda event: root.destroy())


root.mainloop()
