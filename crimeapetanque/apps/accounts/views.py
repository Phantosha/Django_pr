from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm  # можно расширить
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.rating = 50.0  # начальный рейтинг
        user.save()
        return super().form_valid(form)