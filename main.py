from tkinter import *
from tkinter.ttk import Notebook, Frame
from tkinter.ttk import Combobox

import matplotlib

import datetime
import urllib.request
import matplotlib.pyplot as plt
from xml.dom import minidom


import datetime


global spisok
spisok = {"май":5, "апрель":4, "март":3, "февраль":2, "январь":1 }

global months, days
months = []
days = []
weeks = []
lst_weeks = []
kvartals = []


#получение года
def get_year(yr):
    months.clear()
    month = datetime.timedelta(days=30)
    if yr != 2021:
        now = datetime.datetime(yr, 12, 12)
    else:
        now = datetime.datetime.now()
    months.append(now.strftime("%d/%m/%Y"))
    d1 = now - month
    yrs = d1.strftime("%d/%m/%Y")
    months.append(yrs)

    for i in range(12):
        now = d1
        d1 = now - month
        if now.year > d1.year:
            break
        yrs = d1.strftime("%d/%m/%Y")
        months.append(yrs)
    return months

#получение месяца
def get_month(year, mnth):
    days.clear()
    day = datetime.timedelta(days=1)
    now = datetime.datetime(year, mnth, 1)
    days.append(now.strftime("%d/%m/%Y"))
    d1 = now + day
    yrs = d1.strftime("%d/%m/%Y")
    days.append(yrs)

    for i in range(30):
        now = d1
        d1 = now + day
        if now.month < d1.month:
            break
        yrs = d1.strftime("%d/%m/%Y")
        days.append(yrs)
    return days

#получение недель
def get_weeks(begin, end):
    weeks.clear()
    day = datetime.timedelta(days=1)
    start = datetime.datetime.strptime(begin,"%d/%m/%Y")
    finish = datetime.datetime.strptime(end,"%d/%m/%Y")
    while start != finish:
        start = start - day
        weeks.append(start.strftime("%d/%m/%Y"))
    return weeks


def get_week_list():
    lst_weeks.clear()
    day = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    now2 = now.strftime("%d/%m/%Y")
    d1 = now - day
    yrs = d1.strftime("%d/%m/%Y")
    vari = str(now2+"-"+yrs)
    lst_weeks.append(vari)
    for i in range(10):
        now = d1
        now2 = now.strftime("%d/%m/%Y")
        d1 = now - day
        yrs = d1.strftime("%d/%m/%Y")
        vari = str(now2 + "-" + yrs)
        lst_weeks.append(vari)
    return lst_weeks

#получение кварталов
def get_kvartal(nomer, god):
    kvartals.clear()
    day = datetime.timedelta(days=7)
    if nomer == "Первый":
        start = datetime.datetime.strptime("1/1/"+god, "%d/%m/%Y")
        finish = datetime.datetime.strptime("31/03/"+god, "%d/%m/%Y")
        kvartals.append(start.strftime("%d/%m/%Y"))
    elif nomer == "Второй":
        start = datetime.datetime.strptime("1/4/" + god, "%d/%m/%Y")
        finish = datetime.datetime.strptime("30/6/" + god, "%d/%m/%Y")
        kvartals.append(start.strftime("%d/%m/%Y"))
    elif nomer == "Третий":
        start = datetime.datetime.strptime("1/7/" + god, "%d/%m/%Y")
        finish = datetime.datetime.strptime("30/9/" + god, "%d/%m/%Y")
        kvartals.append(start.strftime("%d/%m/%Y"))
    elif nomer == "Четвертый":
        start = datetime.datetime.strptime("1/10/" + god, "%d/%m/%Y")
        finish = datetime.datetime.strptime("31/12/" + god, "%d/%m/%Y")
        kvartals.append(start.strftime("%d/%m/%Y"))
    while start < finish:
        start = start + day
        kvartals.append(start.strftime("%d/%m/%Y"))
    return kvartals

get_week_list()

#получение списка валют
valuti = {}
def get_data(k):
    if k != 0:
        x = ('http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + k)
        response = urllib.request.urlopen(x)
        doc = minidom.parse(response)
        doc.normalize()
    else:
        now = datetime.datetime.now()
        today = str(now.strftime("%d/%m/%Y"))
        x = ('http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + today)
        response = urllib.request.urlopen(x)
        doc = minidom.parse(response)
        doc.normalize()

    for i in range(34):
        name = doc.getElementsByTagName("Name")[i]
        val = doc.getElementsByTagName("Value")[i]
        nom = doc.getElementsByTagName("Nominal")[i]
        nazv = name.childNodes[0].nodeValue
        price = val.childNodes[0].nodeValue
        price = price.replace(',', '.')
        price = float(price)
        nominal = nom.childNodes[0].nodeValue
        nominal = float(nominal)
        valuti.update({nazv: price / nominal})
        if nazv == "Японских иен":
            break
    valuti.update({"� оссийский � убль": 1})

root = Tk()
radio_state = IntVar()
radio_state.set(4)

#обработчик нажатия

def clicked():

    global combotime
    timecut=radio_state.get()
    if (timecut==1):
        combotime = Combobox(tab2)
        combotime['value'] = lst_weeks
        combotime.grid(column=3,row=1)
        combotime.bind("<<ComboboxSelected>>", callbackFunc5)

    elif (timecut==2):
        combotime = Combobox(tab2)
        combotime["value"]=["май 2021", "апрель 2021", "март 2021", "февраль 2021", "январь 2021"]
        combotime.grid(column=3,row=1)
        combotime.bind("<<ComboboxSelected>>", callbackFunc4)

    elif (timecut==3):
        combotime = Combobox(tab2)
        combotime["value"]=["Первый 2021", "Четвертый 2020", "Третий 2020", "Второй 2020", "Первый 2020"]
        combotime.grid(column=3,row=1)
        combotime.bind("<<ComboboxSelected>>", callbackFunc6)

    elif (timecut==4):
        combotime = Combobox(tab2)
        combotime["value"]=["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011"]
        combotime.grid(column=3,row=1)
        combotime.bind("<<ComboboxSelected>>", callbackFunc3)

def callbackFunc6(event):
    global vybor
    vybor = combotime.get()
    vybor = vybor.split(" ")
    nomer = vybor[0]
    god = str(vybor[1])
    get_kvartal(nomer, god)
    valuti_data(kvartals)


def callbackFunc5(event):
    global vybor
    vybor = combotime.get()
    vybor = vybor.split("-")
    begin = vybor[0]
    end = vybor[1]
    get_weeks(begin, end)
    valuti_data(weeks)

def callbackFunc4(event):
    global vybor
    vybor = combotime.get()
    vybor = vybor.split(" ")
    if vybor[0] in spisok.keys():
        mnth = vybor[0]
        mnth = spisok.get(mnth)
        year = vybor[1]
        year = int(year)
    else:
        mnth = vybor[1]
        year = vybor[0]
    get_month(year, mnth)

    valuti_data(days)

def callbackFunc3(event):
    global vybor
    vybor = combotime.get()
    get_year(int(vybor))

    valuti_data(months)



def callbackFunc(event):
    chosen = (combobox1.get())
    global value1
    value1 = valuti.get(chosen)
    return value1


def callbackFunc2(event):
    chosen2 = (combobox2.get())
    global value2
    value2 = valuti.get(chosen2)
    return value2


def btnClick():
    global txt
    vyvod = float(txt.get())
    multi = vyvod * value1
    ans = multi / value2
    lbl["text"] = round(ans, 4)

def buildGraphic():
    matplotlib.use('TkAgg')
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()

    plt.plot(x, y)
    plt.grid()
    plot_widget.grid(row=5, column=4)

def valuti_data(srok):
    matplotlib.rcParams.update({'font.size': 8})
    xy = {}
    valuti2 = {}
    for i in srok:
        get_data(i)
        chosen3 = combobox3.get()
        global value3
        value3 = valuti.get(chosen3)
        xy.update({i:value3})
        print(chosen3, value3)
    print(xy)
    global x, y
    x = list(xy.keys())
    y = list(xy.values())

    if len(x) >= 28:
        for e in range(len(x)):
            x[e] = ('/'.join(x[e].split('/')[:-1]))
            x[e] = ('/'.join(x[e].split('/')[:-1]))

    elif len(x) == 7 or len(x) == 14:
        for e in range(len(x)):
            x[e] = ('/'.join(x[e].split('/')[:-1]))


    elif len(x) <= 12:
        x.reverse()
        y.reverse()

        x[0] = "янв"
        x[1] = "фев"
        x[2] = "мар"
        x[3] = "апр"
        x[4] = "май"
        x[5] = "июн"
        x[6] = "июл"
        x[7] = "авг"
        x[8] = "сен"
        x[9] = "окт"
        x[10] = "ноя"
        x[11] = "дек"






get_data(0)
root.title("Курс центро банка")
root.geometry("400x200")
root.resizable(width=False, height=False)

tab_control = Notebook(root)
tab1 = Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab2 = Frame(tab_control)
tab_control.add(tab2, text="Динамика курса")

btn1 = Button(tab1, text="Конвертировать", command=btnClick)
btn1.grid(column=3, row=1, padx=10)

combobox1 = Combobox(tab1)
combobox1["values"] = (list(valuti.keys()))
combobox1.grid(column=1, row=1)
combobox1.bind("<<ComboboxSelected>>", callbackFunc)

combobox2 = Combobox(tab1)
combobox2["values"] = (list(valuti.keys()))
combobox2.grid(column=1, row=2, pady=10)
combobox2.bind("<<ComboboxSelected>>", callbackFunc2)

combobox3 = Combobox(tab2)
combobox3["values"] = (list(valuti.keys()))
combobox3.grid(column=1, row=1, pady=0)
combobox2.bind("<<ComboboxSelected>>", callbackFunc2)

txt = Entry(tab1)
txt.grid(column=2, row=1, padx=10)

lbl = Label(tab1, text='')
lbl.grid(column=2, row=2, padx=10)

btn2 = Button(tab2, text="Построить график", command=buildGraphic)
btn2.grid(column=1, row=3)

radiobutton1 = Radiobutton(tab2, text = "Неделя",
value = 1, variable = radio_state,command=clicked)
radiobutton1.grid(row = 1, column = 2)
radiobutton2 = Radiobutton(tab2, text = "Месяц",
value = 2, variable = radio_state,command=clicked)
radiobutton2.grid(row = 2, column = 2)
radiobutton3 = Radiobutton(tab2, text = "Квартал",
value = 3, variable = radio_state,command=clicked)
radiobutton3.grid(row = 3, column = 2)
radiobutton4 = Radiobutton(tab2, text = "Год",
value = 4, variable = radio_state,command=clicked)
radiobutton4.grid(row = 4, column = 2)

root.resizable(True, True)
tab_control.pack()
root.mainloop()