<<<<<<< Updated upstream
=======
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render
from .models import Entry

def entries_list(request):
    entries = Entry.objects.all()
    return render(request, 'your_template.html', {'entries': entries})

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

>>>>>>> Stashed changes
