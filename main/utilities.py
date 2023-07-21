from django.template.loader import render_to_string
from django.core.signing import Signer

from TutorSite.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    """Функция отправляет подтверждение регистрации на емейл юзера"""

    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user,
               'host': host,
               'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.html', context)
    body_text = render_to_string('email/activation_letter_body.html', context)
    user.email_user(subject, body_text)
