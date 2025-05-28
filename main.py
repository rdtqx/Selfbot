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

# --- Game/Stream Info ---
STREAM_GAME_NAME = "Roblox"  # What you're "playing" on Twitch
STREAM_URL = "https://www.twitch.tv/rcpfc17"  # YOUR TWITCH CHANNEL URL
GAME_IMAGE_URL = "https://cdn.discordapp.com/attachments/1342843098274861087/1377112134470598707/IMG_4919.jpg?ex=6837c71e&is=6836759e&hm=a4326291fea3ad8397e95a465796f73903515bc6a3a7efd601aaf6a3b7c97b2c&"  # Replace with your image

# --- Your Custom Links ---
YOUTUBE_URL = "https://www.youtube.com/your_youtube_channel" # Your YouTube channel URL
ABOUT_ME_URL = "https://yourwebsite.com/about" # An "About Me" page or another link

# --- Format Uptime ---
def format_uptime():
    if not start_time:
        return "Starting..."
    uptime = datetime.now() - start_time
    return str(uptime).split('.')[0]

# --- Discord Events ---
@client.event
async def on_ready():
    global start_time
    start_time = datetime.now()
    print(f"✅ Logged in as {client.user}")
    asyncio.create_task(set_streaming_status())

# --- Richer Streaming Presence Setter ---
async def set_streaming_status():
    try:
        activity = discord.Streaming(
            name=STREAM_GAME_NAME,
            url=STREAM_URL,
            details="online 24/7", # This appears under the stream name
            state="click the link pookie", # This appears as a smaller line below details
            assets={"large_image": "img_4920", "large_text": "Streaming now!"} # Optional: requires Discord developer assets
        )
        await client.change_presence(activity=activity)
        print("🔴 Streaming status set!")
    except Exception as e:
        print(f"⚠️ Error setting streaming status: {e}")
    while True:
        await asyncio.sleep(3600) # Update status every hour

# --- Flask App ---
app = Flask("")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Discord Self-Bot</title>
    <style>
        body { font-family: Arial; text-align: center; background: #202225; color: white; }
        img { max-width: 300px; margin-top: 20px; border-radius: 8px; }
        .button-container { margin-top: 30px; }
        .btn {
            background-color: #7289DA;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin: 10px;
            text-decoration: none; /* For anchor tags */
            display: inline-block;
        }
        .btn.twitch { background-color: #9146FF; }
        .btn.youtube { background-color: #FF0000; }
        .btn.about { background-color: #5865F2; }
    </style>
</head>
<body>
    <h1>✅ Self-bot Online</h1>
    <p><strong>Uptime:</strong> {{ uptime }}</p>
    <img src="{{ image_url }}" alt="Game Cover">
    <div class="button-container">
        <a href="{{ twitch_url }}" target="_blank" class="btn twitch">Watch on Twitch</a>
        <a href="{{ youtube_url }}" target="_blank" class="btn youtube">My YouTube</a>
        <a href="{{ about_me_url }}" target="_blank" class="btn about">About Me</a>
        <form action="/status" style="display: inline;">
            <button type="submit" class="btn">Refresh Status</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE,
        uptime=format_uptime(),
        image_url=GAME_IMAGE_URL,
        twitch_url=STREAM_URL,
        youtube_url=YOUTUBE_URL,
        about_me_url=ABOUT_ME_URL
    )

@app.route('/status')
def manual_status_reset():
    asyncio.run_coroutine_threadsafe(set_streaming_status(), client.loop)
    return redirect(url_for('home'))

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run_flask, daemon=True)
    thread.start()

# --- Launch Web Server ---
keep_alive()

# --- Self-bot Loop (at your own risk) ---
while True:
    try:
        client.run(TOKEN, bot=False)  # ⚠️ Against Discord TOS
    except Exception as e:
        print(f"🔥 Crash detected: {e}")
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)
