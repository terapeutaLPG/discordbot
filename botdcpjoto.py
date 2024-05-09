import os
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Funkcja dodająca napis na obrazku
def add_text_to_image(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    # Obliczanie rozmiaru tekstu przy użyciu textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) // 2
    text_y = image.height - text_height - 10  # Ustawienie wysokości tekstu na dole obrazka
    draw.text((text_x, text_y), text, fill="white", font=font)
    return image

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_presence.start()
    # Zdefiniuj kanał logów
    log_channel_id = 1238168175825387622  # ID kanału logów
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send("bot się uruchomił.")

@tasks.loop(seconds=60)  # Aktualizuj obecność co 60 sekund
async def update_presence():
    activity = discord.Game("maca ci mamuske ")  # Przykład gry
    await bot.change_presence(activity=activity)

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
                # Dodaj tekst na obrazku
                text = "RDM | Community"  # Twój tekst do dodania
                new_img_with_text = add_text_to_image(new_img, text)
                img_byte_arr = BytesIO()
                new_img_with_text.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                await message.channel.send(f"{message.author.mention} wysłał:", file=discord.File(BytesIO(img_byte_arr), filename=attachment.filename))

    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))
