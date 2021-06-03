from django import forms
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from TWT.context import get_discord_context
from TWT.discord import client

from ....challenges.models.challenge import Challenge
from ...models.submission import Submission
from ...models.vote import Vote


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["c1", "c2", "c3", "c4", "notes"]


class JudgeVote(View):
    def get_context(self, request: WSGIRequest) -> dict:
        return get_discord_context(request=request)

    def post(self, request: WSGIRequest, submission_id):
        context = self.get_context(request=request)
        if not context["is_staff"]:
            messages.add_message(
                request, messages.INFO, "Only staff can access the judging panel."
            )
            return redirect("timathon:Home")

        form = VoteForm(request.POST)
        if form.is_valid():
            user = request.user
            submission = get_object_or_404(Submission, id=submission_id)
            challenge = get_object_or_404(
                Challenge, ended=False, posted=True, type="MO"
            )

            # Check if submission is in the ongoing Timathon.
            if submission.team.challenge != challenge:
                messages.add_message(request, messages.INFO, "Invalid submission.")
                return redirect("timathon:Judge")

            c1 = form.cleaned_data["c1"]
            c2 = form.cleaned_data["c2"]
            c3 = form.cleaned_data["c3"]
            c4 = form.cleaned_data["c4"]
            notes = form.cleaned_data["notes"]

            # Check if user has already voted.
            previous_votes = Vote.objects.filter(user=user, submission=submission)
            if previous_votes:
                messages.add_message(
                    request, messages.WARNING, "You cannot add more than 1 vote!"
                )
                return redirect("timathon:Judge")

            new_vote = Vote.objects.create(
                user=user,
                submission=submission,
                c1=c1,
                c2=c2,
                c3=c3,
                c4=c4,
                notes=notes,
            )

            idv_score = c1 + c2 + c3 + c4
            messages.add_message(request, messages.INFO, "Successfully voted!")
            client.send_webhook(
                "Judging",
                f"<@{context['discord_user'].uid}> added a vote!",
                [
                    {"name": "Team", "value": submission.team.ID},
                    {"name": "Individual score", "value": idv_score},
                ],
            )
            return redirect("timathon:Judge")

        messages.add_message(request, messages.WARNING, "Invalid form.")
        return redirect("timathon:Judge")

    def get(self, request: WSGIRequest, submission_id) -> HttpResponse:
        context = self.get_context(request=request)
        if not context["is_staff"]:
            messages.add_message(
                request, messages.INFO, "Only staff can access the judging panel."
            )
            return redirect("timathon:Home")

        submission = get_object_or_404(Submission, id=submission_id)
        challenge = get_object_or_404(Challenge, ended=False, posted=True, type="MO")

        # Check if submission is in the ongoing Timathon.
        if submission.team.challenge != challenge:
            messages.add_message(request, messages.INFO, "Invalid submission.")
            return redirect("timathon:Judge")

        context["submission"] = submission
        return render(
            request=request, template_name="timathon/judge_vote.html", context=context
        )
