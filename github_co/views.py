from django.shortcuts import render
from github import Github
from github_co.models import User, Location, Repos
from alkanza_test.settings import GITHUB_USERNAME, GITHUB_PASS

# Create your views here.
github = Github(GITHUB_USERNAME, GITHUB_PASS)


def crawl_users_co():
    users_co = github.search_users(query="location:colombia", sort='repositories', order='desc')[1]
    for api_user in users_co:
        user = User.objects.filter(name=api_user.login).first()
        if not user:
            user = User()
            user.username = api_user.login

            location = Location.objects.filter(name=api_user.location).first()
            if not location:
                location = Location(name=api_user.location)

            user.location = location

            collaborator_repos = api_user.get_repos()
            for repo in collaborator_repos:
                repository = Repos.objects.filter(name=repo.name).first()
                if not repository:
                    repository = Repos()
                    repository.name = repo.name
                    repository.stars = repo.stargazers_count
                    repository.save()

            user.save()


def crawl_popular_repos():
    popular_repos = github.search_repositories(query="stars:>15000", sort="stars", order='desc')[:15]  # 162 total

    for repo in popular_repos:
        for collaborator in repo.get_collaborators():
            user = User()

            location = Location.objects.filter(name=collaborator.location).first()
            if not location:
                location = Location(name=collaborator.location)
                location.save()

            user.location = location
            user.username = collaborator.login

            collaborator_repos = collaborator.get_repos()
            for repo in collaborator_repos:

                repository = Repos.objects.filter(name=repo.name).first()
                if not repository:
                    repository = Repos()
                    repository.name = repo.name
                    repository.stars = repo.stargazers_count
                repository.save()

            user.save()
