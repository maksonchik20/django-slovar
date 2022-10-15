from django.shortcuts import render
from slovar_main.settings import YANDEX_API_KEY_SLOVAR
import json
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from fake_useragent import UserAgent

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
    data = {'slovar': []}
    # Получение синонимов
    url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YANDEX_API_KEY_SLOVAR}&lang=ru-ru&text={word}'
    res = requests.get(url=url)
    try:
        res = json.loads(res.content.decode('utf-8'))['def'][0]
        for i in res['tr']:
            all_syn = {'syn' : []}
            all_syn['syn'].append(i['text'])
            try:
                for j in i['syn']:
                    all_syn['syn'].append(j['text'])
            except KeyError:
                pass
            data['slovar'].append(all_syn)
    except IndexError:
        data =  {'slovar': []}
    
    # Получение антонимов
    url = f'https://sinonim.org/a/{word}'
    # user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.62"
    responce = requests.get(url, headers={"User_agent": UserAgent().chrome}).text
    html = BeautifulSoup(responce, "lxml")
    print(html)
    info_good_or_error = html.find('div', class_ = 'onlywords')
    print(info_good_or_error)
    tbody = html.find('tbody')

    return HttpResponse(HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json; encoding=utf-8"))
    # return JsonResponse(data)
        

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