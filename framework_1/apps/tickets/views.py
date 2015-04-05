from .models import Tickets, Answer
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, View, UpdateView


class TicketsView(ListView):
    model = Tickets
    template_name = 'tickets.html'

    def get_queryset(self, user):
        return self.model.objects.filter(creator=user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(request.user)
        opened_tickets = None
        unassigned_tickets = None
        if request.user.is_staff:
            opened_tickets = self.model.objects.filter(status=True, staff=request.user)
            unassigned_tickets = self.model.objects.filter(staff=None)
        return render(request, self.template_name, {'object_list': self.object_list, 'opened_tickets': opened_tickets,
                                                    'unassigned_tickets': unassigned_tickets})


class TicketsCreate(CreateView):
    model = Tickets
    fields = ['type', 'title', 'body', 'priority']
    template_name = 'tickets_create.html'
    success_url = reverse_lazy('tickets_view')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            priority = form.cleaned_data.get('priority')
            creator = request.user
            ticket = Tickets(type=type, title=title, body=body, priority=priority, creator=creator, staff=None)
            ticket.save()
            messages.success(request, _('Ticket successfully created'))
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, _('Please enter valid information.'))
            return render(request, self.template_name, {'form': form})


class TicketsAnswer(CreateView):
    model = Answer
    fields = ['answer']
    template_name = 'tickets_answer.html'

    def get(self, request, *args, **kwargs):
        ticket_pk = kwargs.get('pk')
        ticket = Tickets.objects.filter(pk=ticket_pk)[0]
        if request.user == ticket.creator or request.user.is_staff:
            answers = Answer.objects.filter(related=ticket)
            form = None
            if ticket.status is True:
                form_class = self.get_form_class()
                form = self.get_form(form_class)
            return render(request, self.template_name, {'ticket': ticket, 'answers': answers, 'form': form})
        else:
            return redirect('tickets_view')

    def post(self, request, *args, **kwargs):
        ticket_pk = kwargs.get('pk')
        ticket = Tickets.objects.filter(pk=ticket_pk)[0]
        if request.user == ticket.creator or request.user.is_staff:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                body = form.cleaned_data.get('answer')
                new_answer = Answer(answer=body, answer_creator=request.user, related=ticket)
                new_answer.save()
                return redirect('tickets_answer', pk=ticket_pk)
            else:
                messages.error(request, _('Invalid answer'))
                return redirect('tickets_answer', pk=ticket_pk)
        else:
            return redirect('tickets_view')


class TicketsOpen(View):

    def get(self, request, *args, **kwargs):
        return redirect('tickets_view')

    def post(self, request, *args, **kwargs):
        ticket_pk = kwargs.get('pk')
        ticket = Tickets.objects.get(pk=ticket_pk)
        if request.user == ticket.creator or request.user.is_staff:
            ticket.status = True
            ticket.save()
            messages.success(request, _('Ticket re-opened'))
            return redirect('tickets_answer', pk=ticket_pk)
        else:
            messages.error(request, _('Could not re-open ticket'))
            return redirect('tickets_view')


class TicketsClose(View):

    def get(self, request, *args, **kwargs):
        return redirect('tickets_view')

    def post(self, request, *args, **kwargs):
        ticket_pk = kwargs.get('pk')
        ticket = Tickets.objects.get(pk=ticket_pk)
        if request.user == ticket.creator or request.user.is_staff:
            ticket.status = False
            ticket.save()
            messages.success(request, _('Ticket closed'))
            return redirect('tickets_answer', pk=ticket_pk)
        else:
            messages.error(request, _('Could not close ticket'))
            return redirect('tickets_view')


class TicketsAssign(SuccessMessageMixin, UpdateView):
    model = Tickets
    fields = ['staff']
    template_name = 'tickets_assign.html'
    success_url = reverse_lazy('tickets_view')
    success_message = _('Ticket successfully assigned')
