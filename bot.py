import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import AsyncOpenAI


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
RENDER_EXTERNAL_URL = os.environ["RENDER_EXTERNAL_URL"]
WEBHOOK_PATH = os.environ["WEBHOOK_PATH"]
PORT = int(os.environ.get("PORT", "10000"))

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🤖 Я AI-бот. Напиши мне что-нибудь."
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    try:
        response = await client.responses.create(
            model="gpt-5.6-luna",
            input=update.message.text,
        )

        await update.message.reply_text(response.output_text)

    except Exception:
        await update.message.reply_text(
            "Произошла ошибка. Попробуй ещё раз."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=f"{RENDER_EXTERNAL_URL}/{WEBHOOK_PATH}",
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
