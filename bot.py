from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual Telegram bot token
BOT_TOKEN = "7680394855:AAFVjKErGVwWg9bZ49BnChVgCLnv1xA3MRw"

# Web App URL
WEB_APP_URL = "https://botdepoy.github.io/RenderBot/form.html"

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    """Handles /start command and displays a menu with multiple buttons."""
    # Create an inline keyboard with multiple buttons
    keyboard = [
        [InlineKeyboardButton("填写信息 (Fill Form)", web_app={"url": WEB_APP_URL})],
        [InlineKeyboardButton("帮助 (Help)", callback_data="help")],
        [InlineKeyboardButton("关于我们 (About Us)", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the buttons
    await update.message.reply_text(
        "请选择一个选项 (Please choose an option):",
        reply_markup=reply_markup,
    )

# Callback query handler
async def button_callback(update: Update, context: CallbackContext) -> None:
    """Handles button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text("帮助信息 (Help information):\n\n如有问题，请联系管理员。")
    elif query.data == "about":
        await query.edit_message_text("关于我们 (About Us):\n\n这是一个示例Telegram机器人。")

# Main function to start the bot
def main() -> None:
    # Initialize the bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Add callback query handler for button clicks
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
