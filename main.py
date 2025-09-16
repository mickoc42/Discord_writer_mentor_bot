import discord
import asyncio
import logging
import os
import json
from discord.ext import tasks, commands
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
channelID = int(os.getenv("CHANNEL_ID"))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Wczytanie danych z JSON
with open("schedule.json", "r") as f:
    schedule = json.load(f)

# Wczytanie puli wiadomości z pliku JSON
try:
    with open("messages.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # Teraz plik ma postać {"messages": [ ... ]}
        raw_messages = data.get("messages", [])
        message_pool = [m["message"] for m in raw_messages]
except Exception as e:
    print("Błąd wczytywania pliku:", e)
    message_pool = []

# Przygotowanie indeksów do losowania bez powtórek
unused_message_indices = list(range(len(message_pool)))
random.shuffle(unused_message_indices)

def get_next_message() -> str:
    global unused_message_indices
    if not message_pool:
        return "Brak wiadomości do wysłania."
    if not unused_message_indices:
        # Wyczerpano wszystkie – reset i ponowne losowanie
        unused_message_indices = list(range(len(message_pool)))
        random.shuffle(unused_message_indices)
    idx = unused_message_indices.pop()
    return message_pool[idx]


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
                if (index, today_str) not in sent_today:
                    # Oznaczenie wszystkich członków serwera
                    random_message = get_next_message()
                    await channel.send(f"@everyone {item[random_message]}")
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
        await vc.disconnect()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)