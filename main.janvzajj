import os
import telebot
import instaloader
from telebot import types
from collections import defaultdict
import logging

# Initialize the bot
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Initialize Instaloader
L = instaloader.Instaloader()

# To store user credentials and sessions temporarily
user_sessions = {}
report_log = {}  # To store reports submitted by users

# Logging setup
logging.basicConfig(filename='reports.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Keywords for report categories
report_keywords = {
    "HATE": ["hate", "racist", "discrimination", "offensive"],
    "SELF-HARM": ["suicide", "self-harm", "kill myself"],
    "NUDITY": ["nude", "sex", "porn"],
    "VIOLENCE": ["violence", "terrorist", "attack"],
    "SPAM": ["spam", "advertisement"]
}

# Function to check for keywords in Instagram profile
def analyze_profile(profile_info):
    reports = defaultdict(int)
    profile_texts = [
        profile_info.get("biography", ""),
        profile_info.get("full_name", ""),
    ]
    
    # Check keywords in profile text
    for text in profile_texts:
        for category, keywords in report_keywords.items():
            for keyword in keywords:
                if keyword in text.lower():
                    reports[category] += 1

    return reports

# Function to log in to Instagram using provided credentials
def login_instagram(username, password):
    try:
        user_loader = instaloader.Instaloader()
        print(f"Logging in user {username}...")
        user_loader.login(username, password)
        user_loader.save_session_to_file()
        print(f"{username} logged in successfully!")
        return user_loader
    except instaloader.exceptions.BadCredentialsException:
        return None
    except Exception as e:
        print(f"Error logging in for {username}: {e}")
        return None

# Function to get Instagram profile info
def get_instagram_profile(loader, username):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "follower_count": profile.followers,
            "following_count": profile.followees,
            "is_private": profile.is_private,
            "post_count": profile.mediacount,
        }
        return info
    except instaloader.exceptions.ProfileNotExistsException:
        return None

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Use /login to login to your Instagram account.")

# Login command
@bot.message_handler(commands=['login'])
def login(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Please enter your Instagram username:")
    bot.register_next_step_handler(message, get_instagram_username)

# Get Instagram username
def get_instagram_username(message):
    user_id = message.chat.id
    username = message.text.strip()

    # Save the username temporarily and ask for the password
    user_sessions[user_id] = {'username': username}
    bot.send_message(user_id, "Please enter your Instagram password:")
    bot.register_next_step_handler(message, get_instagram_password)

# Get Instagram password
def get_instagram_password(message):
    user_id = message.chat.id
    password = message.text.strip()

    # Get the username from the session
    username = user_sessions[user_id]['username']

    # Try to log in with the provided credentials
    loader = login_instagram(username, password)
    
    if loader:
        user_sessions[user_id]['loader'] = loader
        bot.send_message(user_id, f"Successfully logged in as {username}. Use /report <target_username> to report a profile.")
    else:
        bot.send_message(user_id, "Login failed. Please try again using /login.")

# Report command to analyze and log a profile
@bot.message_handler(commands=['report'])
def analyze(message):
    user_id = message.chat.id

    if user_id not in user_sessions or 'loader' not in user_sessions[user_id]:
        bot.reply_to(message, "You need to log in first using /login.")
        return

    # Get the Instagram username to report
    target_username = message.text.split()[1:]
    if not target_username:
        bot.reply_to(message, "Please provide the username to report. Example: /report <username>")
        return

    target_username = ' '.join(target_username)

    # Fetch Instagram profile info using the user's session
    loader = user_sessions[user_id]['loader']
    profile_info = get_instagram_profile(loader, target_username)
    
    if profile_info:
        # Analyze the profile for reports
        reports = analyze_profile(profile_info)
        
        if reports:
            response = f"Report for Instagram profile {target_username}:\n"
            for category, count in reports.items():
                response += f"{category}: {count} incidents\n"
        else:
            response = f"No suspicious activity detected for {target_username}."
        
        # Log the report
        if user_id not in report_log:
            report_log[user_id] = []
        report_log[user_id].append(target_username)
        logging.info(f"User {user_sessions[user_id]['username']} reported {target_username}")
        response += "\nThis profile has been reported and logged."
        
    else:
        response = f"Profile {target_username} not found."

    bot.reply_to(message, response)

# Start the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
    
