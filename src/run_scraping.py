import asyncio
import codecs
import os
import sys
import datetime

from django.db import DatabaseError

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, ProgrammingLanguage, Error, Url

user = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (rabota, 'rabota'),
    (djinni, 'djinni'),
)

jobs, errors = [], []


def get_settings():
    qs = user.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['programming_language_id']) for q in qs)

    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['programming_language_id']): q['url_data'] for q in qs}
    urls = []

    for pair in _settings:
        if pair in url_dict:
            tmp = {
                'city': pair[0],
                'programming_language': pair[1],
                'url_data': url_dict[pair]
            }
            urls.append(tmp)

    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_task = [(func, data['url_data'][key], data['city'], data['programming_language'])
            for data in url_list
            for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], programming_language=data['programming_language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists:
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}')

# h = codecs.open('work.json', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
