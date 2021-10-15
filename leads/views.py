from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import query
from django.shortcuts import render, redirect, reverse
from django.views import generic

from.forms import LeadCategoryUpdateForm, LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm
from .models import Lead, Agent, Category
from agents.mixins import OrganizerAndLoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = "landing_page.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "leads"
    template_name = "leads/lead_list.html"

    def get_queryset(self):
        user = self.request.user

        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile,  agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            # Filter
            queryset = queryset.filter(agent__user=user)        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset,
            })
        return context

class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email= "kendygitonga@gmail.com",
            recipient_list= ["kenedygitonga@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)
    
class LeadDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
            # queryset = Lead.objects.all()
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            print(queryset, user.userprofile)

            # Filter for the agent is logged in 
            queryset = queryset.filter(agent__user=user)        
        return queryset

class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    # queryset = Lead.objects.all()
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm 

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        print(lead)
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            "ussassigned_lead_count":queryset.filter(category__isnull=True).count(),
            "ussassigned_lead":queryset.filter(category__isnull=True)
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     # Getting objects methods
    #     # qs = Lead.objects.filter(category=self.get_object()) 

    #     leads = self.get_object()

    #     context.update({
    #         'leads': leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user

        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm         

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={'pk': self.get_object().id})

def landing_page(request):
    return render(request, "landing_page.html")

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request):

    if request.method == "POST":
        form = LeadModelForm(request.POST, auto_id=True)
        if form.is_valid():
            form.save()
            return redirect("leads:lead-list")
    
    # if request.method == "POST":
        # form = LeadForm(request.POST, auto_id=True)
        # if form.is_valid():
        #     first_name = form.cleaned_data['first_name']
        #     last_name = form.cleaned_data['last_name']
        #     age = form.cleaned_data['age']
        #     agent = form.cleaned_data['agent']
        #     lead = Lead.objects.create(
        #         first_name = first_name,
        #         last_name = last_name,
        #         age = age,
        #         agent = agent
        #     )
        #     lead.save()
        #     return redirect("leads:lead-list")


    context = {
        "form": LeadForm()
    }
    return render(request, "leads/lead_create.html", context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)

    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("leads:lead-list")

    # if request.method == "POST":
        # form = LeadForm(request.POST)
    # if form.is_valid():
    #     first_name = form.cleaned_data['first_name']
    #     last_name = form.cleaned_data['last_name']
    #     age = form.cleaned_data['age']
    #     agent = form.cleaned_data['agent']

    #     # Update
    #     lead.first_name = first_name
    #     lead.last_name = last_name
    #     lead.age = age
    #     lead.agent = agent
    #     lead.save()
    #     return redirect("leads:lead-list")

    context = {
        "lead":lead,
        "form":form
    }
    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('leads:lead-list')




 