from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponse
import csv
from .services.reports import get_entries_for_period, build_report

def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.delete()
    return redirect('entries:list')

def custom_logout(request):
    logout(request)
    return redirect('register')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'moodtracker/entry_list.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entries:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class WeeklyReportView(LoginRequiredMixin, TemplateView):
    template_name = "moodtracker/report_week.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = get_entries_for_period(self.request.user, 7)
        report = build_report(entries)
        context['report'] = report
        return context

class MonthlyReportView(LoginRequiredMixin, TemplateView):
    template_name = "moodtracker/report_month.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = get_entries_for_period(self.request.user, 30)
        report = build_report(entries)
        context['report'] = report
        return context

def export_entries_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="mood_entries_{request.user.username}.csv"'
    writer = csv.writer(response)
    writer.writerow(['date', 'mood', 'note'])
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    for entry in entries:
        writer.writerow([entry.date, entry.mood, entry.note])
    return response
