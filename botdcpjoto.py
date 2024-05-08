import discord
from discord.ext import commands, tasks

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Rozpocznij cykliczne wywoływanie funkcji update_presence() co 60 sekund
    update_presence.start()

@tasks.loop(seconds=60)  # Aktualizuj obecność co 60 sekund
async def update_presence():
    discordPresence = discord.RichPresence()
    discordPresence.state = "maca ci mamuske"
    discordPresence.details = "jaruso"
    discordPresence.start = 1507665886
    discordPresence.end = 1507665886
    discordPresence.large_image = "jaruso"
    discordPresence.large_text = "jaruso99"
    discordPresence.small_image_text = "Rogue - Level 100"
    discordPresence.party_id = "ae488379-351d-4a4f-ad32-2b9b01c91657"
    discordPresence.party_size = (3, 69)
    discordPresence.join_secret = "MTI4NzM0OjFpMmhuZToxMjMxMjM="
    await bot.change_presence(activity=discordPresence)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                await message.delete()
                img_data = await attachment.read()
                img = Image.open(BytesIO(img_data))

                # Określ wysokość paska
                bar_height = 60  # Zwiększona wysokość paska

                # Stwórz nowy obraz z dodatkowym miejscem na pasek
                width, height = img.size
                new_img = Image.new("RGB", (width, height + bar_height), "black")
                new_img.paste(img, (0, 0))

                draw = ImageDraw.Draw(new_img)
                text = "RDM | Community"
                font = ImageFont.load_default()
                # Używamy getbbox() zamiast getsize()
                text_bbox = font.getbbox(text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (width - text_width) / 2
                text_y = height + (bar_height - text_height) / 2  # Umieść tekst w nowym pasku na dole
                draw.text((text_x, text_y), text, font=font, fill="white")

                img_byte_arr = BytesIO()
                new_img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                await message.channel.send(f"{message.author.mention} wysłał:", file=discord.File(BytesIO(img_byte_arr), filename=attachment.filename))

    await bot.process_commands(message)

bot.run('DISCORD_TOKEN')  # Podmień na swój token
