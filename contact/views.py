from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages

from contact.forms import ContactForm
from contact.models import Contact


class ContactView(generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you! Your Message sent successfully.')
        return redirect('contact:contact')

    def form_invalid(self, form):
        messages.error(self.request, 'Oops, Something went wrong! try again.')
        return redirect('contact:contact')

# Create your views here.
