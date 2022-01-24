# pylint: disable=global-statement,broad-except
from typing import Optional

from sendgrid import SendGridAPIClient

from server.config.logger import log
from server.config.environment import config

__mailer: Optional[SendGridAPIClient] = None


def setup():
    global __mailer
    __mailer = SendGridAPIClient(api_key=config.sendgrid_secret_key)

    log.info(f'mailer: Setting up mailer with \'{config.sendgrid_sender}\' as the sender')


class EmailResponse:
    def __init__(self, is_sent: bool, msg: str, res=None, error=None) -> None:
        self.is_sent = is_sent
        self.message = msg
        self.response = res
        self.error = error


def send_email(recipient, subject, html) -> EmailResponse:
    global __mailer
    fn = 'send_email'
    dev_whitelist = ('qwikwire.com', 'aqwire.io')

    if not recipient:
        log.error(f'{fn}: Email "{subject}"" has no recipients')
        return EmailResponse(
            is_sent=False,
            msg='Email delivery has failed due to no recipients')

    if config.sendgrid_mode not in ['production', 'development']:
        log.warning(f'{fn}: Held back email "{subject}" for {recipient}')
        return EmailResponse(
            is_sent=False,
            msg=f'Held back email on {config.sendgrid_mode}')

    if not isinstance(recipient, list):
        recipient = [recipient]

    # Filter out the non-qwikwire emails
    if config.sendgrid_mode == 'development':
        non_dev_emails = [r for r in recipient if not r.endswith(dev_whitelist)]
        recipient = list(filter(lambda x: x.endswith(dev_whitelist), recipient))
        log.info(f'{fn}: Holding back email "{subject}" for {non_dev_emails}')

    if len(recipient) == 0:
        log.error(f'{fn}: Email "{subject}"" has no recipients')
        return EmailResponse(
            is_sent=False,
            msg='Email delivery has failed due to no recipients')

    try:
        data = {
            'personalizations': [
                {
                    'to': [{'email': r} for r in recipient],
                    'subject': subject
                }
            ],
            'from': {
                'email': config.sendgrid_sender
            },
            'content': [
                {
                    'type': 'text/html',
                    'value': html
                }
            ]
        }

        response = __mailer.client.mail.send.post(request_body=data)

        if response.status_code >= 400:
            log.error(f'{fn}: Sending email failed with response of {response.status_code}')
            return EmailResponse(
                is_sent=False,
                msg=f'Email delivery has failed with response status {response.status_code}',
                res=response)

        log.info(f'{fn}: Sent "{subject}" email to {recipient}')
        return EmailResponse(
            is_sent=True,
            msg='Email has been sent to the recipients',
            res=response)
    except Exception as ex:
        log.error(f'{fn}: Unexpected error occurred ({str(ex)})')
        return EmailResponse(
            is_sent=False,
            msg='Exception has been thrown during email delivery',
            error=ex)
