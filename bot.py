import logging

# Configure logging to write to reports.log file
logging.basicConfig(
    filename='reports.log',         # Log file path
    level=logging.INFO,             # Log level set to INFO to capture report details
    format='%(asctime)s - %(message)s'  # Log format: Timestamp and message
)

# Example function to log a report
def log_report(user_id, user_ig_username, target_ig_username):
    """
    Logs a report of a user reporting an Instagram profile.

    :param user_id: The Telegram user ID who made the report
    :param user_ig_username: The Instagram username of the reporting user
    :param target_ig_username: The Instagram username of the target profile
    """
    logging.info(f"User {user_ig_username} (ID: {user_id}) reported Instagram profile {target_ig_username}")

# Example usage of the log_report function when a report is made
def handle_report(user_id, user_ig_username, target_ig_username):
    # Perform the reporting logic here...
    
    # Log the report action
    log_report(user_id, user_ig_username, target_ig_username)

# Simulating a report for demonstration
if __name__ == "__main__":
    user_id = 123456
    user_ig_username = "john_doe"
    target_ig_username = "target_profile"
    
    handle_report(user_id, user_ig_username, target_ig_username)
