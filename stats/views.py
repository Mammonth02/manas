from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

def index(request):

    url = 'https://abiturient.manas.edu.kg/page/index.php?r=site%2Fmonitoring-all-deps'
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')

    links = soup.find_all('div', class_='col-xl-2 col-lg-3 col-md-4 col-sm-12 hoverDiv')

    lst = []

    for i in links:

        url1 = i.find('a').get('href')
        url1 = 'https://abiturient.manas.edu.kg/' + url1
        req1 = requests.get(url1)
        src1 = req1.text

        soup1 = BeautifulSoup(src1, 'lxml')

        kvota = soup1.find('p').text[33:35]
        reg = soup1.find_all('tr', class_='bg-success')
        reg1 = len(reg) + len(soup1.find_all('tr', {'class': 'bg-light'}))

        min = 1000.0
        max = 0.0
        med = 0.0


        for m in reg:
            m = m.find_all('td')
            m = float(m[2].text)

            if m < min:
                min = m
            if m > max:
                max = m

            med += m
        
        if len(reg) == 0:
            min = 0
            max = 0
            med = 0
        else:
            med = round(med/len(reg), 2)

        
        lst.append({'name': i.find('a').text, 'количествомест': int(kvota), 'конкуренция': reg1, 'минимальныйбалл': min, 'максимальныйбалл': max, 'среднийбалл': med})



    return render(request, 'index.html', {'lst': lst})