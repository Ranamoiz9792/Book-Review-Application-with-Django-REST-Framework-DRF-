import datetime
import jwt
import random
import smtplib
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_jwt_token(useremail):
    """Generate a JWT token with a 6-hour expiry"""
    payload = {
        'email': useremail,
        
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)

def generate_email_body(otp):
    """Generate an HTML email template for OTP"""
    print("OTP in email:", otp)
    body = """
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        </head>

        <body style="font-family: 'Roboto', sans-serif; margin: 0; padding: 0;">
            <div style="width: 100%; max-width: 800px; margin: 0 auto; box-shadow: 0 0 15px rgba(0, 0, 0, 0.5); border-radius: 10px; overflow: hidden;">
                <div>
                    <p style="color: #000000;">Hello, Use the following One-Time Password (OTP) to complete the registeration process:</p>
                    <div style="color: #7EDDD3; font-size: 36px; text-align: center; background-color: #253746; padding: 15px; border-radius: 5px; margin: 30px 0; box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);">
                        """ + otp + """
                    </div>
                    <p style="color: #000000;">This OTP is valid for the next 10 minutes. Please do not share this code with anyone for security reasons.</p>
                    <p style="color: #000000;">If you did not request this code, please ignore this email or contact our support team immediately.</p>
                    <a href="mailto:contact@gmail.com" style="background-color: #7EDDD3; color: #ffffff; padding: 10px 20px; border: none; border-radius: 5px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 10px 0; transition: background-color 0.3s ease, box-shadow 0.3s ease; cursor: pointer; box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);">
                        Contact Support
                    </a>
                    <div style="margin-top: 20px;">
                        <a href="https://facebook.com" style="margin: 0 10px; color: #ffffff; text-decoration: none; transition: color 0.3s ease, transform 0.3s ease;">
                            <svg fill="#ffffff" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width: 24px; height: 24px; vertical-align: middle;">
                                <path d="M22.675 0h-21.35c-.733 0-1.325.592-1.325 1.325v21.351c0 .733.592 1.324 1.325 1.324h11.488v-9.294h-3.125v-3.622h3.125v-2.67c0-3.1 1.894-4.788 4.659-4.788 1.325 0 2.464.099 2.794.143v3.24l-1.918.001c-1.503 0-1.794.714-1.794 1.761v2.313h3.588l-.467 3.622h-3.121v9.294h6.125c.733 0 1.325-.591 1.325-1.324v-21.351c0-.733-.592-1.325-1.325-1.325z"/>
                            </svg>
                        </a>
                        <a href="https://twitter.com" style="margin: 0 10px; color: #ffffff; text-decoration: none; transition: color 0.3s ease, transform 0.3s ease;">
                            <svg fill="#ffffff" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width: 24px; height: 24px; vertical-align: middle;">
                                <path d="M23.954 4.569c-.885.392-1.833.656-2.825.775 1.014-.608 1.794-1.574 2.163-2.723-.95.564-2.005.974-3.127 1.195-.897-.958-2.178-1.557-3.594-1.557-2.717 0-4.92 2.203-4.92 4.917 0 .386.045.763.128 1.124-4.087-.205-7.719-2.164-10.148-5.144-.423.725-.666 1.562-.666 2.457 0 1.694.862 3.188 2.173 4.066-.8-.026-1.554-.245-2.211-.612v.062c0 2.364 1.681 4.337 3.914 4.785-.409.111-.839.171-1.284.171-.314 0-.622-.03-.923-.086.623 1.947 2.433 3.365 4.576 3.405-1.68 1.319-3.804 2.105-6.104 2.105-.396 0-.787-.023-1.175-.067 2.179 1.397 4.765 2.213 7.548 2.213 9.054 0 14.004-7.503 14.004-14.003 0-.213-.004-.425-.014-.637.961-.694 1.796-1.56 2.457-2.549z"/>
                            </svg>
                        </a>
                    </div>
                </div>
                <div style="color: #7EDDD3; text-align: center; padding: 15px; font-size: 14px;">
                    &copy; 2024 Your Company Name. All rights reserved.<br>
                    <a href="#" style="color:  #253746; text-decoration: none; transition: color 0.3s ease;">Privacy Policy</a> | <a href="#" style="color: #253746; text-decoration: none; transition: color 0.3s ease;">Terms of Service</a>
                </div>
            </div>
        </body>
        </html>

        """

    return body

def send_email(recipient, subject, body):
    """Send an email using SMTP"""
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = recipient

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Email sent to {receiver_email}")
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
