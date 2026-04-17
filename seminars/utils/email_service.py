from django.core.mail import EmailMessage


def send_id_card_email(user, seminar, file_path):
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