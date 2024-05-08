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
    update_presence.start()
    channel = bot.get_channel(1170158612556034068)  # Zmień na odpowiedni ID kanału
    if channel:
        await channel.send("Bot został uruchomiony i jest gotowy do działania.")

@tasks.loop(seconds=60)
async def update_presence():
    # Twoja logika aktualizacji statusu, upewnij się że jest zaimplementowana poprawnie
    await bot.change_presence(activity=discord.Game(name="maca ci mamuske"))

@bot.event
async def on_disconnect():
    channel = bot.get_channel(1170158612556034068)  # Zmień na odpowiedni ID kanału
    if channel:
        await channel.send("Bot został wyłączony.")

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

                bar_height = 60  # Zwiększona wysokość paska
                width, height = img.size
                new_img = Image.new("RGB", (width, height + bar_height), "black")
                new_img.paste(img, (0, 0))

                draw = ImageDraw.Draw(new_img)
                text = "RDM | Community"
                font = ImageFont.load_default()
                text_bbox = font.getbbox(text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (width - text_width) / 2
                text_y = height + (bar_height - text_height) / 2
                draw.text((text_x, text_y), text, font=font, fill="white")

                img_byte_arr = BytesIO()
                new_img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                await message.channel.send(f"{message.author.mention} wysłał:", file=discord.File(BytesIO(img_byte_arr), filename=attachment.filename))

    await bot.process_commands(message)

