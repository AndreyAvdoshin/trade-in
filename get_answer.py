from xml.etree import ElementTree
import requests


def get_barcode(bc):
    url = 'https://www.1c-interes.ru/yml/trade_tg.php'
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    answer = 'Такой штрихкод не найден'
    for i in tree.iter('offer'):
        global name
        element = i
        barcode = int(element.find('barcode').text)
        name = element.find('name').text
        pc = element.find('price_certificate').text
        pcash = element.find('price_cash').text
        if barcode == bc:
            answer = name + ': сертификат на сумму - ' + pc + 'р' ', ' + 'наличными - ' + pcash + 'р.'
            break
    return answer


def get_title(bc):
    url = 'https://www.1c-interes.ru/yml/trade_tg.php'
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    answer = ['Такой игры не найдено']
    data = []
    data2 = []
    for i in tree.iter('offer'):
        element = i
        name = element.find('name').text
        pc = element.find('price_certificate').text
        pcash = element.find('price_cash').text
        if bc in name.lower():
            data.append(name + ': сертификат - ' + pc + 'р' ', ' + 'наличными - ' + pcash + 'р.')
    
    data = sorted(list(set(data)))

    for minus in data:
        data2.append(minus)
        data2.append('--------')
    
    if data2:
        return data2
    else:
        return answer


#print(get_barcode(3391892010558))