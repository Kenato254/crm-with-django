import random
from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic

from leads.models import Agent, UserProfile
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin

PASSWORD = f'{random.randint(0, 1000000)}'

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm 

    def get_success_url(self):
        return reverse('agents:agent-list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(PASSWORD)
        user.save()
        Agent.objects.create(
            user=user,
            organisation = self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message=f"You were added as an agent on DJCRM. Please come login to start working. Your password is {PASSWORD}",
            from_email="kendygitonga@gmail.com", 
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        # return Agent.objects.all
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    model = Agent
    template_name = 'agents/agent_update.html'
    context_object_name = 'agent'
    form_class = AgentModelForm 

    def get_success_url(self):
        return reverse('agents:agent-list')
    
class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    model = Agent
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')
    
    # def get_queryset(self):
    #     return Agent.objects.all()


