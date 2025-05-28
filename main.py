import os
import time
import discord
import asyncio
from datetime import datetime
from flask import Flask
from threading import Thread

# === Your TOKEN here ===
TOKEN = os.getenv("TOKEN")  # Use Replit Secrets or .env file
# Example for local testing:
# TOKEN = "YOUR_USER_TOKEN_HERE"

# === Discord Client Setup ===
intents = discord.Intents.all()
client = discord.Client(intents=intents)
start_time = None

# === Uptime Formatter ===
def format_uptime():
    if not start_time:
        return "Starting..."
    uptime = datetime.now() - start_time
    return str(uptime).split('.')[0]  # HH:MM:SS

# === On Ready Event ===
@client.event
async def on_ready():
    global start_time
    start_time = datetime.now()
    print(f"✅ Logged in as {client.user}")
    asyncio.create_task(set_apex_status())

# === Static Legit Status Setter ===
async def set_apex_status():
    try:
        game = discord.Game(name="Roblox")
        await client.change_presence(activity=game)
        print("🎮 Status set to: Playing Apex Legends")
    except Exception as e:
        print(f"⚠️ Error setting status: {e}")
    while True:
        await asyncio.sleep(3600)  # Keep alive forever

# === Flask Keep-Alive Server ===
app = Flask("")

@app.route('/')
def home():
    return f"✅ Self-bot online — Uptime: {format_uptime()}"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run_flask, daemon=True)
    thread.start()

# === Enable Flask (optional for Replit) ===
keep_alive()

# === Auto-Restart Loop ===
while True:
    try:
        client.run(TOKEN, bot=False)
    except Exception as e:
        print(f"🔥 Crash detected: {e}")
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)
