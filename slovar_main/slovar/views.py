from django.shortcuts import render
from slovar_main.settings import YANDEX_API_KEY_SLOVAR
import json
from django.contrib import messages
import requests
# from PIL import Image
# from io import BytesIO
# import base64
from .models import ImageTest
from django.http import HttpResponse

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
    print(data)
    return render(request, 'slovar/index.html', data)

# API

#Получение данных
def get_data_for_word(request, word:str) -> json:
    data = {'slovar': {}}
    
    url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YANDEX_API_KEY_SLOVAR}&lang=ru-ru&text={word}'
    res = requests.get(url=url)
    try:
        res = json.loads(res.content.decode('utf-8'))['def'][0]
        data['slovar'] = []
        for i in res['tr']:
            main_syn = {'text': i['text'], 'syn': []}
            try:
                for j in i['syn']:
                    main_syn['syn'].append(j['text'])
            except KeyError:
                pass
            data['slovar'].append(main_syn)
    except IndexError:
        data =  {'slovar': []}
    print(data)
    return render(request, 'slovar/index.html', data)
        
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