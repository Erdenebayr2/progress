from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import FileResponse
from django.views import View
from django.http import Http404
import requests,os
from bs4 import BeautifulSoup
from datetime import date,datetime,timedelta
import xlsxwriter


class DownloadFileView(View):
    def get(self, request, *args, **kwargs):
        urlss = mlink
        print(urlss)
        response = requests.get(urlss)
        soup = BeautifulSoup(response.content,'html.parser')

        number = soup.find('ul',class_='number-list')
        if number:
            number = number.text.split('\n')
            number = list(filter(lambda x: x.strip() != '', number))[-1]
        else:
            number = '1'
        ulist = []
        while int(number) > 0:
            urls = urlss + str(number)
            response = requests.get(urls)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all('a',{"class": "announcement-block__title"})
            link_urls = [link.get("href") for link in links]
            for Ulink in link_urls:
                Ulink = "https://www.unegui.mn" + str(Ulink)
                ulist.append(Ulink)
                ulist = list(set(ulist))
            number = int(number) - 1

        url = ulist
        print(url)
        link = []

        for i in range(0,len(url)):
            response = requests.get(url[i])
            soup = BeautifulSoup(response.content,'html.parser')

            mark = soup.find('ul',class_='breadcrumbs').text.split('\n')
            mark = list(filter(lambda x:x.strip() != '',mark))
            mark = mark[-2] + ' / ' +  mark[-1]

            data = soup.find('ul',class_='chars-column').text.split('\n')
            data = list(filter(lambda x: x.strip() != '', data))

            if 'Мотор багтаамж:' in data:
                data[1] = data[1][:3]
                data[1] = float(data[1])*1000
                data[-5] = data[-5][:-4]
            
            if 'Хаяг байршил:' not in data:
                data[2:4] = ('Хаяг байршил:','')

            if 'Шинэ / Хуучин:' not in data:
                data[8:10] = ('Шинэ / Хуучин:','')

            desc = soup.find('div',class_='js-description').text.split('\n')
            desc = list(filter(lambda x: x.strip() != '', desc))
            desc = ''.join(desc)
            
            prince = soup.find('div',class_='announcement-price__wrapper')
            price = prince.find('meta', {'itemprop': 'price'})['content']

            ogno = soup.find('span', class_='date-meta').text[11:-6]
            unuudr = 'Өнөөдөр'
            uchigdur = 'Өчигдөр'
            yester = datetime.now() - timedelta(days=1)
            yesterday = str(yester.date())
            today = str(date.today())
            if ogno == unuudr:ogno = today
            elif ogno == uchigdur:ogno = yesterday
            else:ogno

            dict = {}
            for i in range(0,len(data), 2):
                key = data[i].strip(':')
                value = data[i+1]
                dict[key] = value
            
            dict['Тайлбар'] = desc
            dict['Үнэ'] = price
            dicts = {'Марк':mark,'Зарын огноо':ogno}
            dicts.update(dict)
            link.append(dicts)
            print(dicts)

            file_name = mlink[22:-7]
            file_name = file_name.replace("/", "_")
            workbook = xlsxwriter.Workbook(f"{file_name}.xlsx")
            worksheet = workbook.add_worksheet("firstSheet")

            l = list(dicts.keys())
            for i in range(0,len(l)):
                worksheet.write(0,i,l[i])
                for index, entry in enumerate(link):
                    worksheet.write(index+1, i, entry[l[i]])
            workbook.close()

        file_path = f"{file_name}.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = FileResponse(fh.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404

def test(request):
    global mlink
    if request.method == "POST":
        if request.POST.get("autoZ"):
            mlink ="https://www.unegui.mn/avto-mashin/-avtomashin-zarna/?page="
            print(mlink)
        elif request.POST.get("autoT"):
            mlink ="https://www.unegui.mn/avto-mashin/avto-treesllne/?page="
            print(mlink)
        elif request.POST.get("test"):
            mlink = "https://www.unegui.mn/kompyuter-busad/printer-xuvilagch-skanner/?page"
            print(mlink)
            return redirect('index')
        return redirect('test')
    return render(request,template_name = 'test.html')

def index(request):
    return render(request, 'progress.html')