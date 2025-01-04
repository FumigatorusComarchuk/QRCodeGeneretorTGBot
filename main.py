
import os
import time
import qrcode
from hydrogram import Client
from hydrogram.filters import command, text
from config import settings


bot = Client(
    "QRCodeBot",
    bot_token=settings.TOKEN,
    api_id=settings.API_ID,
    api_hash=settings.API_HASH
)


@bot.on_message(command("start"))
async def send_welcome(bot, message):
    await bot.send_message(message.from_user.id, "Вітаємо!\nВідправте текст який хочете закодувати в QR-код\n")
    message.stop_propagation()


@bot.on_message(text)
async def handle_text_messages(bot, message):
    msg = await bot.send_message(message.from_user.id, "Створюю QR-код...")
    file_name = f"{message.from_user.id}:{time.time()}.png"
    img = qrcode.make(message.text)
    img.save(file_name)
    await bot.send_photo(message.from_user.id, file_name)
    await msg.delete()
    os.remove(file_name)
    message.stop_propagation()


@bot.on_message()
async def other_messages_handler(bot, message):
    await bot.send_message(message.from_user.id, "Для створення QR-коду потрібно відправити текст")


bot.run()
