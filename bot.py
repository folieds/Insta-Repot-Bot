import os
import logging
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='reports.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Initialize Telegram bot
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# In-memory user sessions for logged-in users
user_sessions = {}

# Function to log reports
def log_report(user_id, user_ig_username, target_ig_username):
    logging.info(f"User {user_ig_username} (ID: {user_id}) reported Instagram profile {target_ig_username}")

# Command to log in
@bot.message_handler(commands=['login'])
def login(message):
    user_id = message.chat.id
    bot.reply_to(message, "Please send your Instagram username.")

    # Set the next step to process the username
    bot.register_next_step_handler(message, process_username)

def process_username(message):
    user_id = message.chat.id
    username = message.text.strip()
    
    # Store the username and ask for the password
    user_sessions[user_id] = {"username": username}
    bot.reply_to(message, "Please send your Instagram password.")

    # Set the next step to process the password
    bot.register_next_step_handler(message, process_password)

def process_password(message):
    user_id = message.chat.id
    password = message.text.strip()
    username = user_sessions[user_id]["username"]

    # Simulate Instagram login validation (replace with actual logic)
    if authenticate(username, password):
        bot.reply_to(message, f"Login successful as {username}. You can now report profiles.")
    else:
        bot.reply_to(message, "Login failed. Please check your credentials.")

# Simulated authentication function (replace with actual logic)
def authenticate(username, password):
    return username == "valid_user" and password == "valid_password"

# Command to report an Instagram profile
@bot.message_handler(commands=['report'])
def report(message):
    user_id = message.chat.id

    if user_id not in user_sessions:
        bot.reply_to(message, "You need to log in first. Use /login to authenticate.")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Invalid format. Use: /report <target_instagram_username>")
        return

    target_ig_username = args[1]
    user_ig_username = user_sessions[user_id]["username"]

    # Log the report action
    log_report(user_id, user_ig_username, target_ig_username)

    # Notify the user
    bot.reply_to(message, f"Your report has been submitted against {target_ig_username}.")

# Start polling the bot
bot.polling(none_stop=True)
