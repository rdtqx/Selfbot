import os
import time
import discord
import asyncio
from datetime import datetime
from flask import Flask, render_template_string, redirect, url_for
from threading import Thread

TOKEN = os.getenv("TOKEN")  # Set this using Replit secrets or a .env file

intents = discord.Intents.all()
client = discord.Client(intents=intents)
start_time = None

# === Game Info ===
GAME_NAME = "bust a nut simulator 2021"
GAME_IMAGE_URL = "https://cdn.discordapp.com/attachments/1342843098274861087/1377112134470598707/IMG_4919.jpg?ex=6837c71e&is=6836759e&hm=a4326291fea3ad8397e95a465796f73903515bc6a3a7efd601aaf6a3b7c97b2c&"  # Replace with your image

# === Format Uptime ===
def format_uptime():
    if not start_time:
        return "Starting..."
    uptime = datetime.now() - start_time
    return str(uptime).split('.')[0]

# === Discord Events ===
@client.event
async def on_ready():
    global start_time
    start_time = datetime.now()
    print(f"✅ Logged in as {client.user}")
    asyncio.create_task(set_apex_status())

# === Richer Game Presence Setter ===
async def set_apex_status():
    try:
        activity = discord.Game(name=GAME_NAME)
        await client.change_presence(activity=activity)
        print("🎮 Status set")
    except Exception as e:
        print(f"⚠️ Error setting status: {e}")
    while True:
        await asyncio.sleep(3600)

# === Flask App ===
app = Flask("")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Discord Self-Bot</title>
    <style>
        body { font-family: Arial; text-align: center; background: #202225; color: white; }
        img { max-width: 300px; margin-top: 20px; }
        button {
            background-color: #7289DA;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>✅ Self-bot Online</h1>
    <p><strong>Uptime:</strong> {{ uptime }}</p>
    <img src="{{ image_url }}" alt="Game Cover">
    <form action="/status">
        <button type="submit">Set Status Again</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, uptime=format_uptime(), image_url=GAME_IMAGE_URL)

@app.route('/status')
def manual_status_reset():
    asyncio.run_coroutine_threadsafe(set_apex_status(), client.loop)
    return redirect(url_for('home'))

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run_flask, daemon=True)
    thread.start()

# === Launch Web Server ===
keep_alive()

# === Self-bot Loop (at your own risk) ===
while True:
    try:
        client.run(TOKEN, bot=False)  # ⚠️ Against Discord TOS
    except Exception as e:
        print(f"🔥 Crash detected: {e}")
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)
