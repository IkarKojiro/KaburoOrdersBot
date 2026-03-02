import os
import json
from dotenv import load_dotenv

from telegram import (
    Update,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8443))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    media = [

        InputMediaPhoto(
            "https://raw.githubusercontent.com/IkarKojiro/KaburoOrdersBot/195e5cac3acb127792a757c85a9df44c9cfac040/IMG_7683.jpeg"
        ),

        InputMediaPhoto(
            "https://raw.githubusercontent.com/IkarKojiro/KaburoOrdersBot/195e5cac3acb127792a757c85a9df44c9cfac040/IMG_7684.jpeg"
        ),

        InputMediaPhoto(
            "https://raw.githubusercontent.com/IkarKojiro/KaburoOrdersBot/195e5cac3acb127792a757c85a9df44c9cfac040/IMG_7685.jpeg"
        )

    ]

    await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media
    )

    text = (
        "<b>Buenos días</b>\n\n"

        "На связи Максим.\n"
        "Я создаю свой бренд одежды kaburo и показываю весь путь "
        "с нуля здесь:\n"
        "https://t.me/kaburo_club\n\n"

        "Эта зип-худи - моя первая победа на пути к мечте.\n"
        "Я вложил в неё всю душу и выкрутил качество на максимум.\n\n"

        "Если хочешь такую же - кнопка ниже для тебя.\n"
        "Напишу лично.\n\n"

        "По вопросам: @uineska\n\n"

        "Быть Смелым.\n"
        "Молодым.\n"
        "Свободным 👇👇👇"
    )

    keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    "Оставить заявку",
                    web_app=WebAppInfo(
                        url="https://kaburo-orders-bot.vercel.app"
                    )
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True
    )

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )


async def webapp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    raw_data = update.message.web_app_data.data
    data = json.loads(raw_data)

    text = (

        "Новая заявка на кофту\n\n"

        f"Имя: {data['name']}\n"
        f"Размер: {data['size']}\n"
        f"Город: {data['city']}\n"
        f"Контакт: {data['contact']}\n\n"

        f"Telegram: @{update.message.from_user.username}"
    )

    # Админу
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    # Клиенту
    await update.message.reply_text(
        "Заявка отправлена ✅"
    )


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.WEB_APP_DATA,
            webapp_handler
        )
    )

    print("Webhook started")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )


if __name__ == "__main__":
    main()