from flask import Flask, request, jsonify
from telegram import Bot

# Initialize Flask app
app = Flask(__name__)

# Replace with your actual Telegram bot token and chat ID
BOT_TOKEN = "7680394855:AAFVjKErGVwWg9bZ49BnChVgCLnv1xA3MRw"
CHAT_ID = "8101143576"  # Your Telegram ID or group ID

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit_form():
    """Receives form data and sends it to Telegram."""
    data = request.json

    # Extract form data
    name = data.get("name", "N/A")
    email = data.get("email", "N/A")
    user_id = data.get("user_id", "N/A")
    username = data.get("username", "N/A")
    first_name = data.get("first_name", "N/A")

    # Create message
    message = f"📩 **New Form Submission**\n\n"
    message += f"👤 Name: {name}\n📧 Email: {email}\n"
    message += f"🆔 User ID: {user_id}\n👤 Username: @{username}\n"
    message += f"📝 First Name: {first_name}"

    # Send message to Telegram
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

    return jsonify({"status": "success", "message": "Data sent to Telegram"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
