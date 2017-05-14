from django.core.mail import send_mail


class Emailsender():
    def __init__(self):
        self.name = "Emailsender"

    def sendTo(self, subject, usermaillist, content):
        send_mail(subject=subject,
                  message=content, recipient_list=usermaillist)
        pass

    def sendFile(self, userlist, file, message):
        pass


def dispatchEmail(subject, content,   from_email,  to_email):
    send_mail(
        subject,
        content,
        None,
        [to_email],
        fail_silently=False,
    )
