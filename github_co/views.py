from django.http import HttpResponse
from django.views import View
from github import Github
from github_co.models import User, Location, Repos
from alkanza_test.settings import GITHUB_USERNAME, GITHUB_PASS

github = Github(GITHUB_USERNAME, GITHUB_PASS)


def create_user_and_repos(collaborator):
    user = User.objects.filter(username=collaborator.login).first()
    if not user:
        user = User()
        user.username = collaborator.login

        location = Location.objects.filter(name=collaborator.location).first()
        if not location:
            location = Location(name=collaborator.location)
            location.save()

        user.location = location
        if user.location.name.lower().find("colombia") >= 0:
            user.colombian = True

        user.save()

        collaborator_repos = collaborator.get_repos()
        for repo in collaborator_repos:
            repository = Repos.objects.filter(name=repo.name).first()
            if not repository:
                repository = Repos()
                repository.name = repo.name
                repository.stars = repo.stargazers_count
                repository.save()
                repository.contributors.add(user)
                repository.save()

            user.repos.add(repository)

        user.save()


class CrawlUsersCo(View):
    def get(self, request):
        users_co = github.search_users(query="location:colombia", sort='repositories', order='desc')
        for collaborator in users_co:
            create_user_and_repos(collaborator)
        return HttpResponse(0)


class CrawlPopularRepos(View):
    def get(self, request):
        popular_repos = github.search_repositories(query="stars:>15000", sort="stars", order='desc')[:15]  # 162 total

        for repo in popular_repos:
            for collaborator in repo.get_collaborators():
                create_user_and_repos(collaborator)

        return HttpResponse(0)
