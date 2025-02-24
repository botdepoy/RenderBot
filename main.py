from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
FORM, NAME, SERVICE, PHONE = range(4)

# Start command
async def start(update: Update, context: CallbackContext) -> int:
    # Display a start menu with buttons
    keyboard = [["Form"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)
    return FORM

# Handle form button click
async def form(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("请填写以下信息：\n1. 想办什么业务？", reply_markup=ReplyKeyboardRemove())
    return NAME

# Collect name
async def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.user_data["name"] = user.first_name
    context.user_data["username"] = user.username
    context.user_data["service"] = update.message.text
    await update.message.reply_text("2. 请输入您的电话号码：")
    return PHONE

# Collect phone number and send data
async def phone(update: Update, context: CallbackContext) -> int:
    context.user_data["phone"] = update.message.text

    # Send data to your Telegram ID
    user_data = context.user_data
    message = (
        f"New Form Submission:\n"
        f"Name: {user_data['name']}\n"
        f"Username: @{user_data['username']}\n"
        f"Service: {user_data['service']}\n"
        f"Phone: {user_data['phone']}"
    )
    await context.bot.send_message(chat_id=8101143576, text=message)

    await update.message.reply_text("感谢您的提交！我们会尽快联系您。")
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("操作已取消。", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    # Replace with your bot token
    application = Application.builder().token("7680394855:AAFVjKErGVwWg9bZ49BnChVgCLnv1xA3MRw").build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FORM: [MessageHandler(filters.Text("Form"), form)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
