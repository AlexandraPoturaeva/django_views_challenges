"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

import random
import string

from django.http import HttpResponse, HttpRequest


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def length_is_valid(length: str) -> int | None:
    try:
        length = int(length)
    except ValueError:
        return None

    return length if length in range(1, 100000) else None


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    length = request.GET.get('length')

    if length:
        length = length_is_valid(length)

    if not length:
        return HttpResponse(status=403)

    else:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="filename.txt"'
        response.write(random_string(length))
        return response
