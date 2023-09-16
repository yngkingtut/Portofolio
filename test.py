import os
import re
import smtplib
import random


def password_requirements_met(password):
    requirements = [
        (len(password) >= 8, "Password length is at least 8 characters"),
        (re.search("[a-z]", password), "Contains at least one lowercase letter"),
        (re.search("[A-Z]", password), "Contains at least one uppercase letter"),
        (re.search("[0-9]", password), "Contains at least one digit"),
        (re.search("[!@#$%^&*()]", password), "Contains at least one special character")
    ]
    return all([req[0] for req in requirements]), requirements

def send_email(recipient_email, code):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print("Error: Email credentials not set in environment variables.")
        return False

    subject = "Your Authentication Code"
    body = f"Your authentication code is: {code}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True

def two_factor_auth(email):
    code = str(random.randint(100000, 999999))
    if not send_email(email, code):
        return False
    entered_code = input("Enter the code sent to your email: ")
    if entered_code == code:
        return True
    return False

def main():
    is_strong = False
    while not is_strong:
        password = input("Enter your password: ")
        is_strong, requirements = password_requirements_met(password)
        for met, req in requirements:
            print(f"{'[X]' if met else '[ ]'} {req}")

    email = input("Enter your email for two-factor authentication: ")
    if two_factor_auth(email):
        print("Login successful!")
    else:
        print("Incorrect code or email sending failed. Login failed.")

if __name__ == "__main__":
    main()
