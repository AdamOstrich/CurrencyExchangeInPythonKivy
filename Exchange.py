#!usr/bin/env python3

import numpy as np
import requests
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


From = ""
To = ""
TAB = np.array(0)

class MyGrid(Widget):
    how_much = ObjectProperty(None)

    def spinner1(self, x):
        global From
        From = str(x)

    def spinner2(self, x):
        global To
        To = str(x)

    def submit_clicked(self):
        global From, To, TAB
        how_much = self.how_much.text
        print(how_much, From, To)

        try:
            how_much = float(how_much)
            for i in range(TAB.shape[0]):
                if From == TAB[i][2]:
                    From = i
                    break
            for i in range(TAB.shape[0]):
                if To == TAB[i][2]:
                    To = i
                    break
            print(how_much, From, To)
            x1, x2, y1, y2 = TAB[From][3], TAB[From][1], TAB[To][3], TAB[To][1]
            answear = float(y2) * float(x1) / float(x2) / float(y1) * how_much
            answear = round(answear, 2)
            print(answear)
            self.ids.ans.text = str(how_much) + TAB[From][2] + " = " + str(answear) + TAB[To][2]
        except ValueError:
            self.ids.ans.text = "Wrong data!"

class MyApp(App):
    def build(self):
        return MyGrid()

def commaToDot(string):
    """
    Function changes comma to dot
    :param string: random string
    :return: string with no commas, only possibly dots
    """
    for i in range(len(string)):
        if string[i] == ",":
            string = string[:i]+"."+string[i+1:]
    return string

def current_exchange():
    """
    Function takes current data from https://www.nbp.pl/kursy/xml/a099z210525.xml
    :return: a numpy array with current currency exchange data
    """
    global TAB
    url = "https://www.nbp.pl/kursy/xml/a099z210525.xml"
    timeout = 5
    try:
        r = requests.get(url, timeout=timeout)
        text1 = r.text
        with open("tekst_tablicy_nbp.txt", "w") as f:
            f.write(text1)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection, program will get last saved data.")

    currency = ["zloty (Polska)"]
    conventer = [1]
    CUR = ["PLN"]
    cur_exchange = [1.0]
    with open("tekst_tablicy_nbp.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        line = commaToDot(line) # changing ',' to '.'
        if "nazwa_waluty" in line:
            currency.append(line[20:-16])
        elif "przelicznik" in line:
            conventer.append(int(line[19:-15]))
        elif "kod_waluty" in line:
            CUR.append(line[18:-14])
        elif "kurs_sredni" in line:
            cur_exchange.append(line[19:-15])

    TAB = np.column_stack((np.array(currency), np.array(conventer), np.array(CUR), np.array(cur_exchange)))
    print(CUR)

if __name__ == "__main__":
    current_exchange()
    MyApp().run()