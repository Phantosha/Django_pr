from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Tournament, TournamentParticipant, Match
from .tournament_engine import TournamentEngine

class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/list.html'
    context_object_name = 'tournaments'

class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['participants'] = self.object.participants.all().order_by('-points')
        ctx['matches'] = self.object.matches.all().order_by('round_number', 'match_number')
        return ctx

@login_required
def register_for_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    # Проверка формата: одиночный или командный
    if tournament.get_format_category() == 'singles':
        # одиночная регистрация
        TournamentParticipant.objects.get_or_create(
            tournament=tournament,
            player=request.user,
            defaults={'rating_at_start': request.user.rating}
        )
    else:
        # нужно выбрать существующую команду или создать новую (логика упрощена)
        pass
    return redirect('tournaments:detail', pk=pk)

@login_required
def start_round(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    engine = TournamentEngine(tournament)
    engine.generate_round(tournament.current_round)
    tournament.current_round += 1
    tournament.save()
    return redirect('tournaments:detail', pk=pk)
