from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import smtplib


def send_to_pomper(name, receiver):
    # Creating message subject and sender
    subject = 'Customer Inquiry'
    sender = 'info@pomperadventures.com'

    # passing in the context vairables
    text_content = render_to_string(
        'email/status_email.txt', {"name": name})
    html_content = render_to_string(
        'email/status_email.html', {"name": name})

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# def employee_to_hod(name, receiver):
#     # Creating message subject and sender
#     subject = 'Leave application request'
#     sender = 'capemedia2v@gmail.com'

#     # passing in the context vairables
#     text_content = render_to_string(
#         'email/to_hod.txt', {"name": name})
#     html_content = render_to_string(
#         'email/to_hod.html', {"name": name})

#     msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
