"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, JsonResponse
from typing import Mapping
import json


def full_name_is_valid(full_name: str) -> bool:
    return 5 <= len(full_name) <= 256


def email_is_valid(email: str) -> bool:
    try:
        validate_email(email)
    except ValidationError:
        return False

    return True


def registered_from_is_valid(registered_from: str) -> bool:
    return registered_from in {'website', 'mobile_app'}


def age_is_valid(age: str) -> bool:
    return age.isdigit()


def user_data_is_valid(user_data: Mapping) -> bool:
    user_data_keys = set(user_data.keys())

    if not user_data_keys.issubset({'full_name', 'email', 'registered_from', 'age'}):
        return False

    full_name = user_data.get('full_name')
    email = user_data.get('email')
    registered_from = user_data.get('registered_from')
    age = user_data.get('age')

    if not all([full_name, email, registered_from]):
        return False

    validation_result = [
        full_name_is_valid(full_name),
        email_is_valid(email),
        registered_from_is_valid(registered_from),
    ]

    if age:
        validation_result.append(age_is_valid(age))

    return all(validation_result)


def validate_user_data_view(request: HttpRequest) -> JsonResponse:
    user_data = None
    status = 200
    data = {}

    try:
        user_data = json.loads(request.body)
    except ValueError:
        data = {'data': {}, 'errors': 'invalid json'}
        status = 400

    if user_data:
        if user_data_is_valid(user_data):
            data = {'data': {'is_valid': True}}
        else:
            data = {'data': {'is_valid': False}}

    return JsonResponse(data=data, status=status)
