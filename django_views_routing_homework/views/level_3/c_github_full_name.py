"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

from django.http import HttpResponse, HttpRequest
import requests


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> HttpResponse:
    r = requests.get(url='https://api.github.com/users/' + github_username)
    user_data = None
    status = 200
    content = ''

    try:
        user_data = r.json()
    except ValueError:
        status = 400

    if user_data:
        message = user_data.get('message')
        if message == 'Not Found':
            status = 404
            content = '{"name": None}'
        else:
            full_name = user_data.get('name')
            content = f'{{"name": "{full_name}"}}'

    return HttpResponse(content=content, status=status)
