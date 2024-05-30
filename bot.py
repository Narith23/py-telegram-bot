from datetime import datetime
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "6873062278:AAHkxyT__I98JM0Npu8usS5InjaVDFYDFk4"
BOT_USERNMAE: Final = "@py_chatbot_bot"


# Commands
async def start_command(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thank for start bot.")


async def help_command(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so i can respond")


async def custom_command(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")


# Response
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "hello" in processed or "hi" in processed:
        return {"message": "Hey there! Can I hope you?"}

    elif "list ticket" in processed:
        if "installation" in processed or "install" in processed:
            return {
                "api": "list ticket",
                "message": "Wait abit, I checking..."
            }

    elif "bye" in processed:
        return {"message": "Bye!"}

    elif "time" in processed:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return {"message": current_time}

    elif "how are you" in processed:
        return {"message": "I am good!"}
    elif "what is your name" in processed:
        return {"message": "My name is Bot!"}
    elif "your name" in processed:
        return {"message": "My name is Bot!"}
    elif "date" in processed:
        return {"message": "Today is " + datetime.today().strftime("%d-%m-%Y %I:%M:%S %p")}
    elif "what is datetime" in processed:
        return {"message": "Today is " + datetime.today().strftime("%d-%m-%Y %I:%M:%S %p")}

    return {"message": "I don't understand"}


async def handle_message(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type} chat said: '{text}'")

    if message_type == "group":
        if BOT_USERNMAE in text:
            new_text = text.replace(BOT_USERNMAE, "").split()
            response: str = handle_response(" ".join(new_text))
        else:
            return
    else:
        response: str = handle_response(text)

    print(f"Response: {response}")
    if response['message'] is not None:
        await update.message.reply_text(response['message'])
    else:
        await update.message.reply_text(response)


async def error(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {contextType.error}")


if __name__ == "__main__":
    print("Starting bot...")
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    application.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    application.run_polling(poll_interval=3)
