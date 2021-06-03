from random import randint

from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from TWT.context import get_discord_context

from ...challenges.models.challenge import Challenge
from ..models.submission import Submission
from ..models.team import Team


class PastChallenge:
    def __init__(self, challenge, submissions):
        self.challenge = challenge
        self.submissions = submissions


class PreviousView(View):
    def get_context(self, request: WSGIRequest) -> dict:
        return get_discord_context(request=request)

    def get(self, request: WSGIRequest) -> HttpResponse:
        context: dict = self.get_context(request=request)
        if not context["is_verified"]:
            messages.add_message(
                request, messages.WARNING, "You are not in the server."
            )
            return redirect("/")

        challenge_list = []
        challenges = Challenge.objects.filter(ended=True, posted=True, type="MO")

        for challenge in challenges:
            submissions = Submission.objects.filter(
                team__in=Team.objects.filter(
                    challenge=challenge, submitted=True
                ).exclude(winner=0)
            )
            for submission in submissions:
                discord_members = []
                for member in submission.team.members.all():
                    new_member = {}
                    try:
                        user = SocialAccount.objects.get(user_id=member.id)
                    except SocialAccount.DoesNotExist:
                        pass
                    else:
                        new_member["user_id"] = user.uid
                        avatar_url = user.get_avatar_url()
                        if avatar_url.endswith("None.png"):
                            random = randint(0, 4)
                            avatar_url = (
                                f"https://cdn.discordapp.com/embed/avatars/{random}.png"
                            )
                        new_member["avatar_url"] = avatar_url
                        new_member["username"] = user.extra_data["username"]
                        new_member["discriminator"] = user.extra_data["discriminator"]
                        discord_members.append(new_member)
                submission.team.discord_members = discord_members
            challenge_list.append(
                PastChallenge(challenge=challenge, submissions=submissions)
            )
        context["challenge_list"] = challenge_list

        return render(request, "timathon/codejam_listView.html", context)
