import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def work(url, city=None, programming_language=None):
    jobs = []
    errors = []

    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'programming_language_id': programming_language})
            else:
                errors.append({'url': url, 'title': 'Div not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def rabota(url, city=None, programming_language=None):
    jobs = []
    errors = []

    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table', attrs={'id': 'ctl00_content_ctl00_gridList'})
                if table:
                    tr_list = table.find_all('tr', attrs={'id': True})
                    for tr in tr_list:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('p', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.p.text
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text

                            jobs.append({'title': title.text, 'url': domain + href,
                                         'description': content, 'company': company,
                                         'city_id': city, 'programming_language_id': programming_language})
                else:
                    errors.append({'url': url, 'title': 'Table not exists'})
            else:
                errors.append({'url': url, 'title': 'Page is empty'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def dou(url, city=None, programming_language=None):
    jobs = []
    errors = []

    domain = 'https://jobs.dou.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'vacancyListId'})
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href']
                        cont = li.find('div', attrs={'class': 'sh-info'})
                        content = cont.text
                        company = 'No name'
                        a = title.find('a', attrs={'class': 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text, 'url': href,
                                     'description': content, 'company': company,
                                     'city_id': city, 'programming_language_id': programming_language})
            else:
                errors.append({'url': url, 'title': 'Div not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def djinni(url, city=None, programming_language=None):
    jobs = []
    errors = []

    domain = 'https://djinni.co/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'list-jobs__title'})
                        href = title.a['href']
                        cont = li.find('div', attrs={'class': 'list-jobs__description'})
                        content = cont.text
                        company = 'No name'
                        comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                        if comp:
                            company = comp.text
                        jobs.append({'title': title.text, 'url': domain + href,
                                     'description': content, 'company': company,
                                     'city_id': city, 'programming_language_id': programming_language})
            else:
                errors.append({'url': url, 'title': 'Div not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


# TODO hh.ua
def hh(url, city=None, programming_language=None):
    pass


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/?primary_keyword=C%2B%2B&location=%D0%9E%D0%B4%D0%B5%D1%81%D1%81%D0%B0&title_only=True'
    jobs, errors = djinni(url)

    h = codecs.open('work.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()