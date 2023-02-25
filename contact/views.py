from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm
from django.contrib import messages




def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your message successfully send')
        return redirect('contact:index')
    ctx = {
        'form': form
    }
    return render(request, 'blog/contact.html', ctx)

