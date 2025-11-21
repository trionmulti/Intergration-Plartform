import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION SECTION ---
# In a real platform, these would be saved in a secure database or environment file.
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GMAIL_USER = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_gmail_app_password"
TO_EMAIL = "recipient_email@example.com" 

# Configure the AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def step_1_generate_content(user_topic):
    """
    The 'Intelligence' Node: Asks Gemini to write the content.
    """
    print(f"Please wait... asking Gemini to write about: {user_topic}")
    
    prompt = f"Write a professional, short email body about: {user_topic}. Do not include subject lines or placeholders like [Your Name], just the body text."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

def step_2_send_email(body_content):
    """
    The 'Action' Node: Connects to Gmail and sends the message.
    """
    print("Connecting to Gmail...")
    
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Automated Message from My Platform"

    # Attach the AI-generated body
    msg.attach(MIMEText(body_content, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Upgrade connection to secure
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        print("Success! Email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- THE PLATFORM ENGINE ---
def main():
    print("--- MY INTEGRATION PLATFORM V0.1 ---")
    
    # 1. The Trigger (User Input)
    command = input("What kind of email should I write and send? > ")
    
    # 2. The Process (AI)
    ai_content = step_1_generate_content(command)
    print(f"\nGenerated Content:\n{ai_content}\n")
    
    # 3. The Action (Integration)
    confirm = input("Send this email? (yes/no): ")
    if confirm.lower() == "yes":
        step_2_send_email(ai_content)
    else:
        print("Action cancelled.")

if __name__ == "__main__":
    main()