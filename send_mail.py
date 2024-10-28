import smtplib
from email.message import EmailMessage

# Prompt user for the text file
textfile = input("Enter the name of the file to send: ")

# Open the plain text file whose name is in textfile for reading
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# Prompt for sender, recipient email addresses, and subject
me = input("Enter your email ID: ")
you = input("Enter the recipient's email ID: ")
subject = input("Enter the email subject: ")

# Email subject and headers
msg['Subject'] = subject
msg['From'] = me
msg['To'] = you

# SMTP server details (using Gmail's SMTP server as an example)
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Login details for SMTP server
smtp_user = me
smtp_password = input("Enter the app-specific password: ")

# Send the message via SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as s:
    s.starttls()  # Start TLS encryption
    s.login(smtp_user, smtp_password)  # Login to the SMTP server
    s.send_message(msg)  # Send the email

print("Email sent successfully.")
