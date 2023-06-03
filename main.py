from customtkinter import *
from customtkinter import CTk as Tk
from customtkinter import CTkLabel as Label
from customtkinter import CTkButton as Button
import tkinter.ttk
from ttkthemes import ThemedTk
import requests
import re
from bs4 import BeautifulSoup
import json

window = ThemedTk(theme="black")
window.title('한국공대 나침반')
window.geometry("783x400+600+200")
window.resizable(False, False)

#########################################################################################################################
def get_oversea_buy():
    url = 'https://finance.naver.com/sise/sise_deal_rank.naver?investor_gubun=1000'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    company_name = soup.find_all('a', class_='company')
    company_price = soup.find_all('td', class_='number')

    alllist = list()
    title_total_organ = list()
    price_total_organ = list()

    for companies in company_name[0:7]:
        alllist.append(companies.text.strip())

    for o2 in range(len(alllist)):
        title = company_name[o2].text.strip()
        price = company_price[o2].text.strip()

        company_title = title
        prices = price

        title_total_organ.append(company_title)
        price_total_organ.append(prices)
    name_companies = title_total_organ
    company_prices = price_total_organ

    return name_companies, company_prices

#########################################################################################################################

#외인 매수량 상위 7개 표시

treeview = tkinter.ttk.Treeview(window, height=7, column=["rank", "name"], displaycolumns=["rank", "name"])
treeview.place(x=520, y=165)
treeview.column("#0", width=30, anchor='w')

treeview.column("name", width=100, anchor="center")
treeview.heading("name", text= "주가", anchor="center")

treeview.column("rank", width=130, anchor="center")
treeview.heading("rank", text='외인매수 상위7', anchor='center')

names, prices = get_oversea_buy()
treelist_overseas = [(name, price) for name, price in zip(names, prices)]

for i in range(len(treelist_overseas)):
    treeview.insert('', 'end', text=i+1, values=treelist_overseas[i], iid=str(i) + "번")

#########################################################################################################################

def get_organization_buy():

    url = 'https://finance.naver.com/sise/sise_deal_rank.nhn'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    organ_name = soup.find_all('a', class_='company')
    organ_price = soup.find_all('td', class_='number')

    alllist = list()
    title_total_organ = list()
    price_total_organ = list()

    for companies in organ_name[0:7]:
        alllist.append(companies.text.strip())

    for o2 in range(len(alllist)):
        title = organ_name[o2].text.strip()
        price = organ_price[o2].text.strip()
        company_title = title
        prices = price

        title_total_organ.append(company_title)
        price_total_organ.append(prices)
    title_organ_data = title_total_organ
    price_organ_data = price_total_organ

    return title_organ_data, price_organ_data

#########################################################################################################################
#기관매수량 상위 7개 표시

treeview = tkinter.ttk.Treeview(window, height=7, column=["rank", "name"], displaycolumns=["rank", "name"])
treeview.place(x=520, y=0)
treeview.column("#0", width=30, anchor='w') #순위 번호
treeview.column("name", width=100, anchor="center")
treeview.heading("name", text= "주가", anchor="center")
treeview.column("rank", width=130, anchor="center")
treeview.heading("rank", text='기관매수 상위7', anchor='center')
names, prices = get_organization_buy()
treelist_overseas = [(name, price) for name, price in zip(names, prices)]

for i in range(len(treelist_overseas)):
    treeview.insert('', 'end', text=i+1, values=treelist_overseas[i], iid=str(i) + "번")


#########
# 학사 공지사항가져오기
def school_notice(treeview):
    url = "https://www.tukorea.ac.kr/tukorea/1096/subview.do"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    a_tags = soup.select('a > strong')

    for i, tag in enumerate(a_tags):
        text = tag.text.strip()
        link = 'tukorea.ac.kr' + tag.parent['href']
        treeview.insert('', 'end', text=i+1, values=(text, link))


#학사 공지사항 부분 하늘색으로 설정
style = tkinter.ttk.Style()
style.configure("Notice.Treeview", background="sky blue", fieldbackground="sky blue", foreground='black')
treeview1 = tkinter.ttk.Treeview(window, column=["title", "link"], displaycolumns=["title"], style="Notice.Treeview")

treeview1.place(x=0, y=0)

treeview1.column("#0", width=30, anchor='w')
treeview1.column("title", width=380, anchor="center")
treeview1.heading("title", text= "학사 공지사항", anchor="center")

#학사 공지사항 클릭시 웹브라우저 실행
import webbrowser

def open_link(event):
    item = treeview1.selection()[0]
    link = treeview1.item(item, 'values')[1]
    webbrowser.open(link)

treeview1.bind('<<TreeviewSelect>>', open_link)

school_notice(treeview1)

#########################################################################################################################

def weather_siheung(tree):

    apikey = "621e61191203925138f6d5f2c2421fa4"
    city = "siheung-si"
    lang = "kr"

    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"

    result = requests.get(api)
    # json 타입으로 변환
    data = json.loads(result.text)

    #기존내용 삭제 후
    for i in tree.get_children():
        tree.delete(i)

    # 새 내용 입력
    tree.insert('', 'end', values=("날씨", data["weather"][0]["description"]))
    tree.insert('', 'end', values=("기온", str(data["main"]["temp"]) + '°C'))
    tree.insert('', 'end', values=("체감기온", str(data["main"]["feels_like"]) + '°C'))
    tree.insert('', 'end', values=("최저기온", str(data["main"]["temp_min"]) + '°C'))
    tree.insert('', 'end', values=("최고기온", str(data["main"]["temp_max"]) + '°C'))
    tree.insert('', 'end', values=("습도", str(data["main"]["humidity"])+ '%'))
    tree.insert('', 'end', values=("풍속", str(data["wind"]["speed"]) + 'm/s'))

style = tkinter.ttk.Style()

style.configure("Weather.Treeview", background="white", fieldbackground="white", foreground="black")
weather_tree = tkinter.ttk.Treeview(window, columns=('Attribute', 'Value'), show='headings', style="Weather.Treeview")

weather_tree.heading('Attribute', text='한국공대 날씨')
weather_tree.heading('Value', text='정보')

weather_tree.column('Attribute', width=85, stretch=NO)
weather_tree.column('Value', width=70, stretch=NO)
weather_tree.place(x=0, y=230)

weather_siheung(weather_tree)

#########################################################################################################################
#식단이미지 다운로드
import requests
import os

# 이미지가 저장될 폴더를 만듭니다.
if not os.path.exists('images'):
    os.makedirs('images')

# 이미지 URL
img_url = "https://contents.kpu.ac.kr/contents/2/29L/29LGCCEQKALC/images/scale1/LEV6VYJN4MVI.jpg"
img_url2 = "https://contents.kpu.ac.kr/contents/2/29L/29LGCCEQKALC/images/scale1/O84NSS425LC3.jpg"

# 이미지 파일을 다운로드합니다.
responses_schoolcal = requests.get(img_url, stream=True)
response2 = requests.get(img_url2, stream=True)

# 이미지 파일을 저장합니다.
with open('images/' + 'E동'+img_url.split('/')[-1], 'wb') as out_file:
    out_file.write(responses_schoolcal.content)

with open('images/' + 'TIP'+img_url.split('/')[-1], 'wb') as out_file:
    out_file.write(response2.content)
#########################################################################################################################

#식단 이미지 출력
from PIL import Image, ImageTk
from tkinter import Toplevel
from customtkinter import CTkLabel

def show_image_E():
    top = Toplevel()
    img = Image.open("images/E동LEV6VYJN4MVI.jpg")

    my_img = ImageTk.PhotoImage(img)
    label = CTkLabel(master=top, image=my_img, text="")

    label.image = my_img
    label.pack()


def show_image_TIP():
    top = Toplevel()
    img = Image.open("images/TIPLEV6VYJN4MVI.jpg")
    tip_img = ImageTk.PhotoImage(img)
    label = CTkLabel(master=top, image=tip_img, text="")
    label.image = tip_img  # 참조를 유지하기 위해 필요
    label.pack()

# 이미지를 표시할 버튼 생성
button = Button(window, text="E동식단표", command=show_image_E, width=105)
button.place(x=415, y=0)


button = Button(window, text='TIP식단표', command=show_image_TIP, width=105)
button.place(x=415, y=30)

#########################################################################################################################

#학사력

def get_school_cal_tree():
    url = "https://ksc.tukorea.ac.kr/sso/login_stand.jsp"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    academic_area = soup.find('div', class_='academicArea')
    a_tags = academic_area.find_all('a')

    iljung_name = list()
    gigan = list()

    for tag in a_tags:
        iljung_name.append(tag.text.strip())

    span_tags = academic_area.find_all('span', class_='date')

    for tag in span_tags:
        # Split the text at newline characters, remove leading/trailing whitespace from each part, then join with a single space
        cleaned_text = ' '.join(part.strip() for part in tag.text.split('\n'))
        cleaned_text = re.sub(r'\d{4}\.', '', cleaned_text)
        gigan.append(cleaned_text)

    return iljung_name, gigan


treeview_school_cal = tkinter.ttk.Treeview(window, height=8, column=["name", "range"], displaycolumns=["name", "range"], show='headings')

treeview_school_cal.column("name", width=225, anchor="center")
treeview_school_cal.heading("name", text='일정', anchor="center")

treeview_school_cal.column("range", width=135, anchor="center")
treeview_school_cal.heading("range", text="기간", anchor="center")

school_cal_names, calranges = get_school_cal_tree()

school_calendar_list = [(name, range) for name, range in zip(school_cal_names, calranges)]

for i in range(len(school_calendar_list)):
    treeview_school_cal.insert('', 'end', values=school_calendar_list[i])

treeview_school_cal.place(x=158, y=230)

#############################################################################################

#컴퓨터 캘린더에 일정 추가
import os
import datetime
from ics import Calendar, Event

# 이전에 정의한 함수
def on_tree_select(event):
    item = treeview_school_cal.selection()[0]
    selected_event = treeview_school_cal.item(item, 'values')
    event_name, event_range = selected_event
    start_date_str, end_date_str = event_range.split('~')

    # 현재 연도를 붙여줍니다.
    current_year = datetime.datetime.now().year
    start_date_str = str(current_year) + '.' + start_date_str.strip()
    end_date_str = str(current_year) + '.' + end_date_str.strip()

    # datetime 객체로 변환합니다.
    start_date = datetime.datetime.strptime(start_date_str, "%Y.%m.%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y.%m.%d")

    # 종료일을 하루 뒤로 설정합니다.
    end_date = end_date + datetime.timedelta(days=1)

    # 만약 시작일과 종료일이 같다면, 종료일을 하루 뒤의 자정으로 설정합니다.
    if start_date == end_date:
        end_date = end_date.replace(hour=0, minute=0, second=0)

    # 새로운 이벤트를 만듭니다.
    event = Event()
    event.name = event_name
    event.begin = start_date
    event.end = end_date

    # 캘린더에 이벤트를 추가합니다.
    calendar = Calendar()
    calendar.events.add(event)

    # .ics 파일로 저장합니다.
    with open("event.ics", "w", encoding="utf-8") as f:
        f.write(str(calendar))

    # .ics 파일을 열어 일정을 추가합니다.
    os.startfile("event.ics")

# Treeview의 선택 항목이 변경될 때마다 on_tree_select 함수를 호출합니다.
treeview_school_cal.bind('<<TreeviewSelect>>', on_tree_select)




#################################
#로고 출력
# Create a new Tkinter window
# Open an image file
with Image.open("images/로고.png") as img:
    # Convert the image to a Tkinter-compatible photo image
    img = img.resize((280, 75))
    logo_img = ImageTk.PhotoImage(img)

# Create a label and set its image to the one we just created
label_logo = Label(window, image=logo_img, text="")
label_logo.place(x=520, y=325)



def stop(event=None):
    window.quit()

window.bind('<Escape>', stop)
window.mainloop()