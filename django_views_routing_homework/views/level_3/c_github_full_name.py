"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

from django.http import HttpRequest, JsonResponse
import requests
from requests.models import Response


def convert_github_response_to_jsonresponse(github_response: Response) -> JsonResponse:
    user_data = None
    data = {}
    status = 200

    try:
        user_data = github_response.json()
    except ValueError:
        data = {'data': {}, 'errors': 'invalid json'}
        status = 400

    if user_data:
        github_response_status = github_response.status_code

        if github_response_status == 404:
            data = {'data': {}, 'errors': 'user not found'}
            status = 404
        else:
            full_name = user_data.get('name')
            data = {'data': {'name': full_name}}

    return JsonResponse(data=data, status=status)


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> JsonResponse:
    github_response = requests.get(url=f'https://api.github.com/users/{github_username}')
    return convert_github_response_to_jsonresponse(github_response=github_response)
