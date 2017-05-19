from django.shortcuts import render
from contact.models import Contact
from django_email import mail
from contact.forms import ContactForm
from demosite import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.


def index(request):
    page_title = "Contact" + "  -  " + settings.SITE_NAME
    template_name = "contact/contact.html"
    if (request.method == 'POST'):
        # form = UserCreationForm(postdata)
        form = ContactForm(data=request.POST.copy())
        if form.is_valid():
            # form.save()
            subject = form.cleaned_data['subject']
            subject = "User Request : " + subject
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            message = "Sender : " + sender + "\n" + message
            cc_myself = form.cleaned_data['cc_myself']
            recipients = [settings.CONTACT_MAIL]
            if(cc_myself):
                recipients.append(sender)
            mail.dispatchEmail(subject=subject, content=message,
                               from_email=None, to_email=recipients)
            contact = form.save(commit=False)
            contact.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

        else:
            print("ContactForm is invalid...")

    else:
        form = ContactForm()
    context = {'page_title': page_title, 'form': form}
    return render(request, template_name, context)
