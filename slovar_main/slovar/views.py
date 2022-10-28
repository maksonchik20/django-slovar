from django.shortcuts import render
from slovar_main.settings import YANDEX_API_KEY_SLOVAR
import json
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from fake_useragent import UserAgent
from urllib.request import getproxies

def main_slovar(request):
    data = {}
    data['title'] = 'Онлайн словарь'
    text = ""
    try:
        text = request.GET.get('text')
    except:
        pass

    if text:
        data['title'] =  f'Значение слова {text} | Онлайн словарь'
        data['slovar'] = {}
        url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YANDEX_API_KEY_SLOVAR}&lang=ru-ru&text={text}'
        res = requests.get(url=url)
        res = json.loads(res.content.decode('utf-8'))
        data['slovar']['text'] = text
        try:
            res = res['def'][0]
            
            data['slovar']['main'] = []
            for i in res['tr']:
                main_syn = {'text': i['text'], 'syn': []}
                try:
                    for j in i['syn']:
                        main_syn['syn'].append(j['text'])
                except KeyError:
                    pass
                data['slovar']['main'].append(main_syn)
        except:
            messages.error(request, f'Слово "{text}" не найдено!')
    return render(request, 'slovar/index.html', data)

def render_project(request):
    return render(request, 'slovar/project.html')

# API

#Получение данных
def get_data_for_word(request, word:str) -> json:
    data = {'slovar': {'syn': []}}
    # Получение синонимов
    url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YANDEX_API_KEY_SLOVAR}&lang=ru-ru&text={word}'
    res = requests.get(url=url)
    try:
        res = json.loads(res.content.decode('utf-8'))['def'][0]
        for i in res['tr']:
            data['slovar']['syn'].append(i['text'])
            try:
                for j in i['syn']:
                    data['slovar']['syn'].append(j['text'])
            except KeyError:
                pass
    except IndexError:
        data =  {'slovar': {'syn': []}}
    
    # Получение антонимов
    url = f'https://synonyms.su/antonyms/m/{word}/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "User_agent": UserAgent().chrome,
        'referer': 'https://yandex.ru/',
        }
    antonims = []
    responce = requests.get(url, headers=headers, proxies=getproxies()).text
    html = BeautifulSoup(responce, "lxml")
    try:
        table_tr = html.find('table', class_='synonyms-table').find('tbody').findAll('tr')
        for tr in table_tr:
            antonims.append(tr.findAll('td')[1].find('a').text)
    except:
        pass
    data['slovar']['antonims'] = antonims

    # Получение данных о морфемном разборе
    morfems = {'wordComposition': []}
    url = f'https://morphemeonline.ru/С/{word.lower()}'
    responce = requests.get(url, headers=headers, proxies=getproxies()).content
    html = BeautifulSoup(responce, "lxml")
    # print(html)
    try:
        morf = html.find('main', class_ = 'col-md-9').find('p')
        if 'Часть речи' in morf.text:
            morfems['speech'] = morf.find('br').next_element.text.split()[2]
        for el in morf.findAll('span', class_ = 'marker'):
            morfems['wordComposition'].append(f'{el.text}{el.next_element.next_element.text.replace(",", "")}')
    except Exception as _ex:
        print('ошибка', _ex)

    data['slovar']['morfems'] = morfems

    return HttpResponse(HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json; encoding=utf-8"))
        

# def get_and_save_img(request):
#     if request.method == 'POST':
#         img_base64 = json.loads(request.body.decode('utf-8'))['data']
#         img = img_base64.replace('data:image/png;base64,', '')
#         im = Image.open(BytesIO(base64.b64decode(img)))
#         path_save = im.save('./files/image_user/2.png')
#         ImageTest.objects.create(image='image_user/2.png')
#         return HttpResponse({'Access-Control-Allow-Origin': 'https://localhost:8000'})
#     else:
#         return HttpResponse({'Method GET not allowed': 'True'})