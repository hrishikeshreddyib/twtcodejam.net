from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from ..models.team import Team
from TWT.context import get_discord_context
from django import forms
from ...challenges.models.challenge import Challenge
from django.contrib import messages


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class Create_team(View):
    def get_context(self, request: WSGIRequest) -> dict:
        return get_discord_context(request=request)

    def post(self, request: WSGIRequest):
        if not request.user.is_authenticated:
            return redirect('/')
        context = self.get_context(request=request)
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            user = request.user
            challenge = Challenge.objects.get(ended=False, posted=True, type='MO')
            name = form.cleaned_data["name"]
            user_teams = Team.objects.filter(challenge=challenge, members=user)
            if len(user_teams) !=0:
                messages.add_message(request,
                                     messages.WARNING,
                                     "You are Already in a Team")
                return redirect('/')
            new_team = Team.objects.create(
                name=name,
                challenge=challenge
            )
            new_team.members.add(user)
            new_team.save()
            messages.add_message(request,
                                 messages.INFO,
                                 "Team successfully created!")
            return redirect('timathon:Home')
        messages.add_message(request,
                             messages.WARNING,
                             'Invalid Form')
        return redirect('timathon:Create_Team')

    def get(self, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('/')
        context = self.get_context(request=request)
        return render(
            request=request,
            template_name="timathon/create_teams.html",
            context=context
        )