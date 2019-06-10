import requests
from bs4 import BeautifulSoup as bs

#маскируемся под юзера
headers1 = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
headers2 = {'accept' : '*/*',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#стандартная страница для парсера
base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'

def hh_parse(base_url, headers):
    jobs = []
    session = requests.Session() #иммулирует действия одного пользователя, а не разные запросы
    request = session.get(base_url, headers = headers1)
    #проверка данных, которые отдает нам сервер
    if request.status_code == 200: #код успешного запроса
        #обработка полученных данных
        soup = bs(request.content, #ответ который нам отправляет сервер
                  'html.parser') #разбивает ответ на блоки html
        # print(soup) #весь ответ, если нужно
        #разбиваем ответ на блоки по шаблону
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        #обрабатываем каждый блок
        for div in divs:
            title1 = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}) #отображает полный html код блоки <a />
            title2 = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text #вакансия
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'] #ссылка на вакансию
            company = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            description1 = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            description2 = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            description = description1 + description2
            jobs.append({
                'title': title2,
                'href': href,
                'company': company,
                'description': description,
            })
            print(jobs)
            print('--'*8)
    else:
        print('Error')

hh_parse(base_url, headers1)
