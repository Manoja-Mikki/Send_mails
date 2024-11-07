import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from urllib.parse import quote  # Import quote for URL encoding

# API and Email details
WEATHER_API_KEY = input("Enter API key: ")
EMAIL_ADDRESS = 'manojam1701@gmail.com'  # Your Gmail address
APP_PASSWORD = input("Enter app specific passpord:")  # Use the app-specific password generated in Google account
RECIPIENT_EMAIL = input("Enter recipient email: ")


def get_weather_update(country_code="us"):
    # Construct URL with ZIP code and country code
    zip_code=input("Enter zip code inside US:")
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&APPID={WEATHER_API_KEY}&units=metric'
    print(f"Request URL: {url}")  # Debugging statement to check URL
    response = requests.get(url)
    print(f"Response Status Code: {response.status_code}")  # Debugging statement to check response status

    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        weather_update = f"Today's weather in {zip_code}:\n" \
                         f"Description: {weather_desc.capitalize()}\n" \
                         f"Temperature: {temperature}°F"
        return weather_update
    else:
        # Print error details for debugging
        print(f"Error: {response.status_code}, {response.text}")
        return "Failed to get weather data."

# Test the weather update function
weather_update = get_weather_update()
print(weather_update)  # This should print the weather update if successful

def send_email(weather_update):
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Daily Weather Update"
    
    msg.attach(MIMEText(weather_update, 'plain'))


    
    
    # Set up the SMTP server and send the email using the app-specific password
    try:
        # SMTP server details (using Gmail's SMTP server as an example)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Login details for SMTP server
        smtp_user = EMAIL_ADDRESS
        smtp_password = input("Enter the app-specific password: ")

# Send the message via SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.starttls()  # Start TLS encryption
            s.login(smtp_user, smtp_password)  # Login to the SMTP server
            s.send_message(msg)  # Send the email

            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def daily_weather_email():
    # Get the weather update and send the email
    weather_update = get_weather_update()
    send_email(weather_update)

# Schedule the email to be sent daily at a specific time (e.g., 7:00 AM)
schedule.every().day.at("06:00").do(daily_weather_email)

print("Daily weather email scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
