import os
from classes.PrimeCalculator import PrimeCalculator
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
from classes.PrimeBot import PrimeBot


# load environment variables
load_dotenv()

# get environment variables
TOKEN = os.getenv("TOKEN", "")
USERNAME = os.getenv("USERNAME", "")

bot = PrimeBot()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot.input_investment = True
    await update.message.reply_text("Please enter your investment: ")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help feature comming soon...")


async def else_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unrecognized command")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    if bot.input_investment:
        if not bot.validate_investment(text):
            await update.message.reply_text("Please provide a valid number")
        else:
            if float(text) < 100:
                await update.message.reply_text("Investment must be at least 100 $")
            else:
                bot.input_investment = False

                prime = PrimeCalculator()
                prime.investment = float(text)
                weekly_net_profit = prime.weekly_net_profit()

                reply_keyboard = [[KeyboardButton("/start")]]

                await update.message.reply_text(
                    f"Weekly net profit: {weekly_net_profit:.2f} $"
                )

                await update.message.reply_text(
                    f"Monthly net profit: {(weekly_net_profit * 4):.2f} $",
                    reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard,
                        resize_keyboard=True,
                        one_time_keyboard=True,
                        input_field_placeholder="Calculate",
                    ),
                )
    else:
        await else_command(update, context)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(str(context.error))


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("else", else_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
