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
import os
import datetime
from ics import Calendar, Event
from PIL import Image, ImageTk
from tkinter import Toplevel
from customtkinter import CTkLabel



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
    name_all = list()
    price_all = list()

    for companies in company_name[0:7]:
        alllist.append(companies.text.strip())

    for i in range(len(alllist)):
        title = company_name[i].text.strip()
        price = company_price[i].text.strip()

        company_title = title
        prices = price

        name_all.append(company_title)
        price_all.append(prices)
    name_companies = name_all
    company_prices = price_all

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

    company_name = soup.find_all('a', class_='company')
    company_price = soup.find_all('td', class_='number')

    alllist = list()
    name_all = list()
    price_all = list()

    for companies in company_name[0:7]:
        alllist.append(companies.text.strip())

    for i in range(len(alllist)):
        title = company_name[i].text.strip()
        price = company_price[i].text.strip()
        company_title = title
        prices = price

        name_all.append(company_title)
        price_all.append(prices)
    title_datas = name_all
    price_datas = price_all

    return title_datas, price_datas

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
    data = json.loads(result.text)

    #기존내용 삭제 후
    for i in tree.get_children():
        tree.delete(i)

    # 업데이트된 내용 입력
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

# 이미지가 저장될 폴더를 생성
if not os.path.exists('images'):
    os.makedirs('images')
    
img_url = "https://contents.kpu.ac.kr/contents/2/29L/29LGCCEQKALC/images/scale1/LEV6VYJN4MVI.jpg"
img_url2 = "https://contents.kpu.ac.kr/contents/2/29L/29LGCCEQKALC/images/scale1/O84NSS425LC3.jpg"

# 이미지 파일을 다운로드합니다.
responses_schoolfood = requests.get(img_url, stream=True)
responses_schoolfood2 = requests.get(img_url2, stream=True)

# 이미지 파일을 저장합니다.
with open('images/' + 'E동'+img_url.split('/')[-1], 'wb') as out_file: #/로 구분, 맨 뒤에있는 파일명 가져옴
    out_file.write(responses_schoolfood.content)

with open('images/' + 'TIP'+img_url.split('/')[-1], 'wb') as out_file:
    out_file.write(responses_schoolfood2.content)
#########################################################################################################################

#식단 이미지 출력


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

# 버튼 클릭시 식단표 팝업 표시
button = Button(window, text="E동식단표", command=show_image_E, width=105)
button.place(x=415, y=0)

button = Button(window, text='TIP식단표', command=show_image_TIP, width=105)
button.place(x=415, y=30)

#########################################################################################################################

#이번달 학사력 가져오기

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
        cleaned_text = ' '.join(part.strip() for part in tag.text.split('\n')) #공백 제거
        cleaned_text = re.sub(r'\d{4}\.', '', cleaned_text) #연도 제거
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
def on_tree_select(event):
    item = treeview_school_cal.selection()[0]
    selected_event = treeview_school_cal.item(item, 'values')
    event_name, event_range = selected_event
    start_date_str, end_date_str = event_range.split('~')

    # 현재 연도를 앞에 다시 붙여주기
    current_year = datetime.datetime.now().year
    start_date_str = str(current_year) + '.' + start_date_str.strip()
    end_date_str = str(current_year) + '.' + end_date_str.strip()

    # datetime으로 변환해줌
    start_date = datetime.datetime.strptime(start_date_str, "%Y.%m.%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y.%m.%d")

    # 종료일을 하루 뒤로 설정 (컴퓨터 프로그램에서 끝나는 날짜가 하루 빨라짐에 대한 오류 수정 사항)
    end_date = end_date + datetime.timedelta(days=1)

    # 시작일 = 종료일 이면, 종료일을 하루 뒤 자정으로 설정
    if start_date == end_date:
        end_date = end_date.replace(hour=0, minute=0, second=0)

    event = Event()
    event.name = event_name
    event.begin = start_date
    event.end = end_date

    # 달력에 일정 추가
    calendar = Calendar()
    calendar.events.add(event)

    # .ics 파일로 저장
    with open("event.ics", "w", encoding="utf-8") as f:
        f.write(str(calendar))

    # .ics 파일 열어 달력 프로그램으로 .ics 파일 실행
    os.startfile("event.ics")

# 선택 항목이 변경될 때마다 함수 호출
treeview_school_cal.bind('<<TreeviewSelect>>', on_tree_select)


#################################
# 학교 로고 출력

with Image.open("images/로고.png") as img:
    # 로고 크기 조정
    img = img.resize((280, 75))
    logo_img = ImageTk.PhotoImage(img)

label_logo = Label(window, image=logo_img, text="")
label_logo.place(x=520, y=325)



def stop(event=None):
    window.quit()

window.bind('<Escape>', stop)
window.mainloop()