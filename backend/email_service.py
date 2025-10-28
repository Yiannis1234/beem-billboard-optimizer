"""
Email service for sending contact form messages
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_contact_email(name, email, message):
    """Send contact form message to vamvak@outlook.com"""
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"  # Using Gmail SMTP
        smtp_port = 587
        
        # You'll need to set these environment variables
        sender_email = os.getenv("SENDER_EMAIL", "your-gmail@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "your-app-password")
        recipient_email = "vamvak@outlook.com"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"BritMetrics Contact Form - {name}"
        
        # Email body
        body = f"""
New message from BritMetrics contact form:

Name: {name}
Email: {email}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message}

---
Sent from BritMetrics Billboard Intelligence Platform
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        return True, "Message sent successfully!"
        
    except Exception as e:
        return False, f"Failed to send message: {str(e)}"

def send_auto_reply(name, email):
    """Send auto-reply to the person who submitted the form"""
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        sender_email = os.getenv("SENDER_EMAIL", "your-gmail@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "your-app-password")
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Thank you for contacting BritMetrics!"
        
        body = f"""
Hi {name},

Thank you for reaching out to BritMetrics! We've received your message and will get back to you within 24 hours.

In the meantime, feel free to explore our Billboard Intelligence Platform at britmetrics.com

Best regards,
The BritMetrics Team

---
BritMetrics - Billboard Intelligence Platform
📧 vamvak@outlook.com
🔗 https://www.linkedin.com/in/ioannisvamvakas/
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Auto-reply failed: {e}")
        return False
