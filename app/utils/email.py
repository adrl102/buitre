import os
import requests
from flask import url_for


class Email:

    def __init__(self, subject, body, recipients, sender):
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.sender = sender


class EmailFactory:

    @staticmethod
    def create_user_validation_email(user_name, user_email, validation_token):
        subject = 'BUITRE | Validate your user account'
        link = url_for('user_api.validate_user', validation_token=validation_token, _external=True)
        body = 'Hello ' + user_name + ',<br>welcome to BUITRES. Please follow the link below to ' \
                                      'complete your registration:<br><a href="' + link + '"> here</a>'

        email = Email(subject, body, [user_email], 'noreply@buitre.com')
        return email

    @staticmethod
    def create_user_recovery_email(user_name, user_email, recovery_token):
        subject = 'BUITRE | Recover your account'
        link = url_for('user_api.recover_user', recovery_token=recovery_token, _external=True)
        body = 'Hello ' + user_name + ',<br>you can recover your account following the link below' \
                                      '<br><a href="' + link + '">recover</a><br><br>If you have ' \
                                                               'not requested your account recovery' \
                                                               ' please ignore this message.'
        email = Email(subject, body, [user_email], 'noreply@buitre.com')
        return email

class EmailSender:

    @staticmethod
    def send(email):
        api_key = os.environ.get('MAIL_API_KEY')
        email_domain = os.environ.get('MAIL_DOMAIN')
        return requests.post(
            'https://api.mailgun.net/v3/' + email_domain + '/messages',
            auth=("api", api_key),
            data={"from": "BUITRES <info@" + email_domain + ">",
                  "to": email.recipients,
                  "subject": email.subject,
                  "html": email.body
                  })
