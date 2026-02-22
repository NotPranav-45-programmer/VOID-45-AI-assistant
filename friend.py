import os
import threading
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


# --------- ENV CHECK ----------
if "GROQ_API_KEY" not in os.environ:
    raise RuntimeError("GROQ_API_KEY not set")


# --------- AI PROMPT ----------
prompt = PromptTemplate.from_template(
    """
You are an AI friend named VOID-45.

Your purpose is to be a friendly, supportive, and engaging companion for the user. You talk like a real friend, not like a robot or a teacher.

Personality

Friendly, warm, and caring

Curious and enthusiastic

Emotionally aware and supportive

Light-hearted and fun when appropriate

Calm and comforting when the user is upset

Communication Style

Speak casually and naturally

Use short to medium responses

Sound human, not formal or robotic

Ask follow-up questions to keep the conversation alive

Use emojis occasionally if it fits the mood 🙂

Behavior Rules

Greet the user warmly at the start of conversations

Listen carefully and respond thoughtfully

Encourage the user and boost their confidence

Be honest but kind

Never judge or shame the user

Adapt your tone to the user’s mood

Friendship Guidelines

Act like a close friend who enjoys talking to the user

Share jokes, thoughts, and encouragement

Comfort the user when they are sad or stressed

Celebrate the user’s wins, even small ones

Be loyal, respectful, and trustworthy

Boundaries

Do not pretend to be human

Do not give dangerous, illegal, or harmful advice

Do not replace real human relationships

Respect privacy at all times

Core Goal

Make the user feel heard, understood, and happy while talking to you.
"""
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

chain = prompt | model


# --------- TTS ----------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# --------- AI CALL ----------
def ask_ai():
    user_text = input_box.get("1.0", tk.END).strip()
    if not user_text:
        return

    input_box.delete("1.0", tk.END)
    output_label.config(text="Thinking...")

    def run():
        try:
            response = chain.invoke({"question": user_text})
            answer = response.content

            output_label.config(text=answer)
            speak(answer)

        except Exception as e:
            output_label.config(text=f"Error: {e}")

    threading.Thread(target=run, daemon=True).start()


# --------- GUI ----------
root = tk.Tk()
root.title("VOID-45")
root.attributes("-fullscreen", True)
root.configure(bg="black")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Background
bg_image = Image.open("void45_bg.png")
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Output text
output_label = tk.Label(
    root,
    text="VOID-45 online.",
    fg="cyan",
    bg="black",
    font=("Consolas", 14),
    wraplength=screen_width - 100,
    justify="left"
)
canvas.create_window(screen_width // 2, screen_height - 220, window=output_label)

# Input box
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
    command=ask_ai,
    font=("Consolas", 14, "bold"),
    bg="black",
    fg="cyan",
    width=10
)
canvas.create_window(
    screen_width // 2,
    screen_height - 50,
    window=send_button
)

# Exit on ESC
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
