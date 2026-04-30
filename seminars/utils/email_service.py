import threading
from django.core.mail import EmailMessage


def send_id_card_email_async(user, seminar, file_path):
    try:
        subject = "Your Seminar ID Card"

        message = f"""
Hello {user.get_full_name()},

You have successfully registered for:

Seminar: {seminar.title}
Date: {seminar.date_time}

Your ID card is attached with this email.

Thank you.
"""

        email = EmailMessage(
            subject=subject,
            body=message,
            to=[user.email]
        )

        email.attach_file(file_path)
        email.send()

    except Exception as e:
        print("Email failed:", e)


def send_id_card_email(user, seminar, file_path):
    thread = threading.Thread(
        target=send_id_card_email_async,
        args=(user, seminar, file_path)
    )
    thread.start()
