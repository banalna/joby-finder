import os
import sys
import datetime

import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()
from scraping.models import Vacancy, Error, Url, ProgrammingLanguage, City
from scraping_service.settings import EMAIL_HOST_USER

ADIMN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий {today}'
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по ващим предпостениям данных нет...</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'programming_language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['programming_language']), [])
    users_dict[(i['city'], i['programming_language'])].append(i['email'])

if users_dict:
    params = {'city_id__in': [], 'programming_language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['programming_language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['programming_language_id']), [])
        vacancies[(i['city_id'], i['programming_language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])

            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADIMN_USER
_html = ''

if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p>'
    subject = f'Ошибки скрапинга {today}'
    text_content = 'Ошибки скрапинга'

    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>Город: {i["city"]}, Специальность:{i["programming_language"]} Email: {i["email"]} </a></p>'
        subject = f'Пожелания пользователей {today}'
        text_content = 'Пожелания пользователей'


qs = Url.objects.all().values('city', 'programming_language')
urls_dict = {(i['city'], i['programming_language']): True for i in qs}
urls_err = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            _names = (City.objects.filter(id=keys[0]).first().name,
                      ProgrammingLanguage.objects.filter(id=keys[1]).first().name)

            urls_err += f'<p>Для города {_names[0]} и ЯП: {_names[1]} отсутствуют urls.</p>'
if urls_err:
    subject += ' Отсутствующие urls'
    _html += urls_err
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])

    msg.attach_alternative(_html, "text/html")
    msg.send()

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart('alternative')
# msg['Subject'] = 'Список вакансий за  {}'.format(today)
# msg['From'] = EMAIL_HOST_USER
# mail = smtplib.SMTP()
# mail.connect(EMAIL_HOST, 25)
# mail.ehlo()
# mail.starttls()
# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
# html_m = "<h1>Hello world</h1>"
# part = MIMEText(html_m, 'html')
# msg.attach(part)
# mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
# mail.quit()