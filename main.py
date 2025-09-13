import discord
import asyncio
import logging
import os
import json
from flask import Flask
from discord.ext import tasks, commands
from dotenv import load_dotenv
from datetime import datetime, time as dtime
from hypercorn.asyncio import serve
from hypercorn.config import Config
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
channelID = int(os.getenv("CHANNEL_ID"))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Render!"

async def start_flask():
    config = Config()
    config.bind = [f"0.0.0.0:{os.environ.get('PORT', 5000)}"]
    await serve(app, config)


async def start_bot():
    await bot.start(token)

async def main():
    # run both concurrently
    await asyncio.gather(
        start_flask(),
        start_bot()
    )


# Wczytanie danych z JSON
with open("data.json", "r") as f:
    schedule = json.load(f)

sent_today = set()
last_day_checked = None  # do resetu codziennie

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    check_messages.start()


@tasks.loop(hours=1)
async def check_messages():
    global last_day_checked, sent_today
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%A")
    channel = bot.get_channel(channelID)



    # Resetujemy sent_today po północy
    if last_day_checked != today_str:
        sent_today.clear()
        last_day_checked = today_str

    for index, item in enumerate(schedule):
        if weekday in item["days"]:
            msg_time = dtime.fromisoformat(item["time"])
            if now.hour == msg_time.hour:
                if (index, today_str) not in sent_today:
                    # Oznaczenie wszystkich członków serwera
                    await channel.send(f"@everyone {item['message']}")
                    sent_today.add((index, today_str))

@bot.command()
async def timer(ctx, minutes: int):
    if minutes <= 0:
        await ctx.send("❌ Podaj liczbę minut większą od 0.")
        return

    msg = await ctx.send(f"⏳ Odliczam {minutes} minut...")

    for remaining in range(minutes, 0, -1):
        await msg.edit(content=f"⏳ Pozostało {remaining} minut...")
        await asyncio.sleep(60)  # czekaj minutę

    # po zakończeniu
    await ctx.send(f"✅ myk,myk , dokończcie zdanie i czytamy :D ")

    # jeśli użytkownik jest na kanale głosowym, bot dołącza i odtwarza dźwięk
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio("beep.mp3"))

        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

