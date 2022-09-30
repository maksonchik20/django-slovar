from django.shortcuts import render
from slovar_main.settings import YANDEX_API_KEY_SLOVAR
import json
from django.contrib import messages
import requests

def main_slovar(request):
    data = {'method': 'GET'}
    if request.method == 'GET':
        data['title'] = 'Онлайн словарь'
        return render(request, 'slovar/main_slovar.html', data)
    elif request.method == 'POST':
        text = request.POST['text']
        data['title'] =  f'Значение слова {text} | Онлайн словарь'
        data['method'] = 'POST'
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

        return render(request, 'slovar/main_slovar.html', data)
