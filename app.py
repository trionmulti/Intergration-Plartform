import streamlit as st
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. DEFINE THE LOGIC NODES (The Backend) ---

class GeminiNode:
    def __init__(self, api_key):
        self.api_key = api_key

    def run(self, input_text):
        if not self.api_key:
            return "Error: Missing Gemini API Key"
        
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Write a professional email body about: {input_text}. Keep it concise."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"

class GmailNode:
    def __init__(self, user_email, app_password, target_email):
        self.user = user_email
        self.password = app_password
        self.to = target_email

    def run(self, email_body):
        if not self.user or not self.password:
            return "Error: Missing Gmail Credentials"
            
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = self.to
        msg['Subject'] = "Automated Streamlit Email"
        msg.attach(MIMEText(email_body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            return "Success: Email sent via Gmail!"
        except Exception as e:
            return f"Gmail Error: {e}"

# --- 2. BUILD THE VISUAL INTERFACE (The Frontend) ---

def main():
    st.set_page_config(page_title="My AI Platform", page_icon="🤖")
    
    st.title("⚡ My Custom AI Integration Platform")
    st.markdown("Generate emails with Gemini and send them via Gmail.")

    # --- Sidebar for Configuration (Security) ---
    st.sidebar.header("🔌 Connections")
    
    gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
    gmail_user = st.sidebar.text_input("Your Gmail Address")
    gmail_pass = st.sidebar.text_input("Gmail App Password", type="password")
    target_email = st.sidebar.text_input("Target Recipient Email")

    st.divider() # visual separator

    # --- Main Workflow Area ---
    st.subheader("1. Trigger")
    user_topic = st.text_input("What should this email be about?", placeholder="e.g. Requesting a meeting on Friday")

    # --- The "Run" Button ---
    if st.button("🚀 Run Workflow"):
        
        # Step 1: AI Processing
        st.subheader("2. Processing (AI)")
        with st.spinner("Gemini is writing..."):
            ai_node = GeminiNode(gemini_key)
            generated_content = ai_node.run(user_topic)
            
            # Display the result in a nice box
            st.text_area("Generated Content:", value=generated_content, height=200)

        # Step 2: Action
        st.subheader("3. Action (Email)")
        if "Error" in generated_content:
            st.error("Workflow stopped due to AI error.")
        else:
            with st.spinner("Sending email..."):
                email_node = GmailNode(gmail_user, gmail_pass, target_email)
                status = email_node.run(generated_content)
                
                if "Success" in status:
                    st.success(status)
                else:
                    st.error(status)

if __name__ == "__main__":
    main()