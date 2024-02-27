from PyQt5 import QtCore, QtGui, QtWidgets
from math import log10
from numpy import linspace
import matplotlib.pyplot as plt

#R_3150 = False
#R_3150 = True
SLOI = 1
vibor = ""
vibor_2 = ""
sl_1_zag = "материал:"

ohi = ""

# ...или\с легкими зап-ми
tabl_9 = {"керамзитобетон": {"М-100 1500-1550": 1.1, "М-100 1300-1450": 1.2, "М-100 1200": 1.3, "М-100 1100": 1.4,
                            "M 150-200 1700-1750": 1.1, "M 150-200 1500-1650": 1.2, "M 150-200 1350-1450": 1.3,
                            "M 150-200 1250": 1.4},
         "перлитобетон": {"М-100 1400-1450": 1.2, "М-100 1300-1350": 1.3, "М-100 1100-1200": 1.4, "М-100 950-1000": 1.5},
         "аглопоритобетон": {"М-100 1300": 1.1, "М-100 1100-1200": 1.2, "М-100 950-1000": 1.3, "М-150 1500-1800": 1.2},
         "шлакопемзобетон": {"М-100 1600-1700": 1.2, "М-150 1700-1800": 1.2},
         "газобетон, пенобетон, газосиликат": {"М-70 1000": 1.5, "800": 1.6, "600": 1.7},
         "кладка из кирпича, пустотелых керам. блоков": {"1500-1600": 1.1, "1200-1400": 1.2},
         "гипсобетон, гипс (в т.ч. поризованный .....)": {"М 80-100 1300": 1.15, "М 80-100 1200": 1.25,
                                                          "М 80-100 1000": 1.35, "М 80-100 800": 1.45}}


def f_to_f_1_3_50_5000(f):
    etalon = {56: 50, 70: 63, 88: 80, 111: 100, 140: 125, 176: 160, 222: 200, 280: 250, 353: 315, 445: 400, 561: 500,
              707: 630, 890: 800, 1122: 1000, 1414: 1250, 1782: 1600, 2244: 2000, 2828: 2500, 3563: 3150, 4489: 4000}
    for i in etalon:
        if f <= i:
            return etalon[i]
        if i == 4489:
            return 5000

def fy_ro(ro):
    'таблица страницы 20 21'
    a_1 = [40000, 39000, 37000, 35000, 33000, 31000, 29000]
    a_2 = {600 + i * 200: a_1[i] for i in range(6)}
    for i in a_2:
        if ro <= i:
            return a_2[i]
        if i == 1600:
            return 29000


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.spi_1 = []
        MainWindow.setObjectName("MainWindow")
        if SLOI == 4:
            MainWindow.resize(1400, 560)
        else:
            MainWindow.resize(980, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font_1, font_2, font_3, font_4 = QtGui.QFont(), QtGui.QFont(), QtGui.QFont(), QtGui.QFont()

        self.spisok_f = [[font_1, 14], [font_2, 7], [font_3, 16], [font_4, 10]]

        for i in self.spisok_f:
            i[0].setFamily("Segoe Print")
            i[0].setPointSize(i[1])
            i[0].setBold(True)
            i[0].setWeight(75)

        self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_2_1, self.label_2_2 = \
            QtWidgets.QLabel(self.centralwidget), QtWidgets.QLabel(self.centralwidget),\
            QtWidgets.QLabel(self.centralwidget), QtWidgets.QLabel(self.centralwidget),\
            QtWidgets.QLabel(self.centralwidget), QtWidgets.QLabel(self.centralwidget),\
            QtWidgets.QLabel(self.centralwidget)

        self.textEdit, self.textEdit_2, self.textEdit_4, self.textEdit_5 = QtWidgets.QTextEdit(self.centralwidget), \
            QtWidgets.QTextEdit(self.centralwidget), QtWidgets.QTextEdit(self.centralwidget), \
            QtWidgets.QTextEdit(self.centralwidget)

        self.pushButton, self.pushButton_sbr = QtWidgets.QPushButton(self.centralwidget), QtWidgets.QPushButton(self.centralwidget)

        self.spisok_l_t_p = [[self.label, 50, 50, 150, 65, font_1, 'толщина \nограждения, м'],
                         [self.label_2, 260, 50, 240, 65, font_1, 'объемная плотность \nограждения, кг / м3'],
                         [self.label_3, 550, 50, 180, 40, font_1, sl_1_zag],
                         [self.label_4, 50, 220, 170, 65, font_1, 'толщина \nштукатурки, м'],
                         [self.label_5, 260, 220, 230, 65, font_1, 'объемная плотность \nштукатурки, кг / м3'],
                         [self.label_2_1, 20, 10, 290, 25, font_2, 'перевод, с "нормативного" в алгоритм: Субботкин А.О.'],
                         [self.label_2_2, 765, 10, 200, 25, font_2, 'разработка интерфейса: Тарасов Д. Л.'],
                         [self.textEdit, 50, 130, 130, 60, font_1, '0.27'],
                         [self.textEdit_2, 300, 130, 130, 60, font_1, '2400'],
                         [self.textEdit_4, 50, 310, 130, 60, font_1, '0.01'],
                         [self.textEdit_5, 300, 310, 130, 60, font_1, '1800'],
                         [self.pushButton, 305, 400, 150, 50, font_3, 'делать.'],
                         [self.pushButton_sbr, 680, 50, 125, 40, font_3, 'сбросить.']]

        for i in self.spisok_l_t_p:
            i[0].setGeometry(QtCore.QRect(i[1], i[2], i[3], i[4]))
            i[0].setFont(i[5])

        self.pushButton.clicked.connect(show_graph)
        self.pushButton_sbr.clicked.connect(sbros)


        if SLOI != 4:
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(15, 460, 1200, 50))
            self.label_6.setFont(font_1)

        if SLOI == 4:
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(15, 460, 100, 40))
            self.label_6.setFont(font_4)

            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(15, 500, 100, 40))
            self.label_7.setFont(font_4)

            self.spi_1 = []
            j = 1
            for i in SSS_1:
                self.label_t_1 = QtWidgets.QLabel(self.centralwidget)
                self.label_t_1.setGeometry(QtCore.QRect(85 + 60*j, 460, 40, 40))
                self.label_t_1.setFont(font_4)
                j += 1
                self.spi_1.append(self.label_t_1)

            self.spi_2 = []
            j = 1
            for i in SSS_2:
                self.label_t_2 = QtWidgets.QLabel(self.centralwidget)
                self.label_t_2.setGeometry(QtCore.QRect(85 + 60*j, 500, 40, 40))
                self.label_t_2.setFont(font_4)
                j += 1
                self.spi_2.append(self.label_t_2)

        if SLOI == 1:
            j = 0
            for i in tabl_9:
                self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_2.setGeometry(QtCore.QRect(550, 100 + j*50, 400, 40))
                self.pushButton_2.setFont(font_4)
                j += 1
                self.spi_1.append(self.pushButton_2)

            self.spi_1[0].clicked.connect(lambda: k_slo_1('керамзитобетон'))
            self.spi_1[1].clicked.connect(lambda: k_slo_1('перлитобетон'))
            self.spi_1[2].clicked.connect(lambda: k_slo_1('аглопоритобетон'))
            self.spi_1[3].clicked.connect(lambda: k_slo_1('шлакопемзобетон'))
            self.spi_1[4].clicked.connect(lambda: k_slo_1('газобетон, пенобетон, газосиликат'))
            self.spi_1[5].clicked.connect(lambda: k_slo_1('кладка из кирпича, пустотелых керам. блоков'))
            self.spi_1[6].clicked.connect(lambda: k_slo_1('гипсобетон, гипс (в т.ч. поризованный .....)'))

        if SLOI == 2:
            self.spi_1 = []
            j = 0
            for i in tabl_9[vibor]:
                self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_3.setGeometry(QtCore.QRect(550, 100 + j * 50, 400, 40))
                self.pushButton_3.setFont(font_4)
                self.spi_1.append(self.pushButton_3)
                j += 1

            if vibor == 'керамзитобетон':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М-100 1500-1550"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("М-100 1300-1450"))
                self.spi_1[2].clicked.connect(lambda: k_slo_2("М-100 1200"))
                self.spi_1[3].clicked.connect(lambda: k_slo_2("М-100 1100"))
                self.spi_1[4].clicked.connect(lambda: k_slo_2("M 150-200 1700-1750"))
                self.spi_1[5].clicked.connect(lambda: k_slo_2("M 150-200 1500-1650"))
                self.spi_1[6].clicked.connect(lambda: k_slo_2("M 150-200 1350-1450"))
                self.spi_1[7].clicked.connect(lambda: k_slo_2("M 150-200 1250"))

            if vibor == 'перлитобетон':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М-100 1400-1450"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("М-100 1300-1350"))
                self.spi_1[2].clicked.connect(lambda: k_slo_2("М-100 1100-1200"))
                self.spi_1[3].clicked.connect(lambda: k_slo_2("М-100 950-1000"))

            if vibor == 'аглопоритобетон':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М-100 1300"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("М-100 1100-1200"))
                self.spi_1[2].clicked.connect(lambda: k_slo_2("М-100 950-1000"))
                self.spi_1[3].clicked.connect(lambda: k_slo_2("М-150 1500-1800"))

            if vibor == 'шлакопемзобетон':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М-100 1600-1700"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("М-150 1700-1800"))

            if vibor == 'газобетон, пенобетон, газосиликат':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М-70 1000"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("800"))
                self.spi_1[2].clicked.connect(lambda: k_slo_2("600"))

            if vibor == 'кладка из кирпича, пустотелых керам. блоков':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("1500-1600"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("1200-1400"))

            if vibor == 'гипсобетон, гипс (в т.ч. поризованный .....)':
                self.spi_1[0].clicked.connect(lambda: k_slo_2("М 80-100 1300"))
                self.spi_1[1].clicked.connect(lambda: k_slo_2("М 80-100 1200"))
                self.spi_1[2].clicked.connect(lambda: k_slo_2("М 80-100 1000"))
                self.spi_1[3].clicked.connect(lambda: k_slo_2("М 80-100 800"))


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "СП"))
        for i in self.spisok_l_t_p:
            i[0].setText(_translate("MainWindow", i[6]))

        if SLOI != 4:
            self.label_6.setText(_translate("MainWindow", ohi))#*тех. строка*
        if SLOI == 4:
            self.label_6.setText(_translate("MainWindow", "      частота: "))
            self.label_7.setText(_translate("MainWindow", "звукоизоляция: "))
            j = 0
            for i in self.spi_1:
                i.setText(str(SSS_1[j]))
                j += 1
            j = 0
            for i in self.spi_2:
                i.setText(str(iii(SSS_2[j])))
                j += 1

        if SLOI == 1:
            j = 0
            for i in tabl_9:
                self.spi_1[j].setText(i)
                j += 1

        if SLOI == 2:
            j = 0
            for i in tabl_9[vibor]:
                self.spi_1[j].setText(i)
                j += 1


def k_slo_1(a):
    global SLOI, vibor, sl_1_zag
    vibor = a
    SLOI = 2
    sl_1_zag = "плотность:"
    ui.setupUi(MainWindow)


def k_slo_2(a):
    global SLOI, vibor_2, sl_1_zag
    vibor_2 = a
    SLOI = 3
    sl_1_zag = f"K = {tabl_9[vibor][vibor_2]}"
    ui.setupUi(MainWindow)


def sbros():
    global SLOI, vibor, sl_1_zag, vibor_2
    SLOI = 1
    vibor = ""
    vibor_2 = ""
    sl_1_zag = "материал:"
    ui.setupUi(MainWindow)


def snrika_1(a, b):
    'формирование строки для "таблицы"'
    a = str(a)
    for i in b:
        b_2 = str(i)
        b_2 = b_2.rjust(6, " ")
        b_2 = b_2.ljust(8, " ")
        a += b_2
        a += "|"
    return a


def iii(a):
    if a % 1 == 0:
        return int(a)
    return a


def show_graph():
    global SLOI, SSS_1, SSS_2
    #global R_3150
    #R_3150 = False
    if vibor == "" or vibor_2 == "":
        ui.label_6.setText("    Нет «К». Выберите материал и плотность. . ")
        return False

    try:
        h_m = float(ui.textEdit.toPlainText())  # толщина ограждения, м
        ro_m = float(ui.textEdit_2.toPlainText()) # объемная плотность ограждения, кг / м3
        K = tabl_9[vibor][vibor_2]# float(ui.textEdit_3.toPlainText())  # коэффициент из таблицы

        h_sh = float(ui.textEdit_4.toPlainText()) # толщина штукатурки, м
        ro_sh = float(ui.textEdit_5.toPlainText())  # объемная плотность штукатурки, кг / м3
    except:
        ui.label_6.setText("     есть не корректные значения. ")
        return False
    #R_3150 = True

    EEEtalon = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
                1250, 1600, 2000, 2500, 3150, 4000, 5000]
    SSS_1 = EEEtalon

    gamma_m = ro_m * h_m  # поверхностная плотность материала
    gamma_sh = ro_sh * h_sh  # поверхностная плотность штукатурки
    gamma = gamma_m + gamma_sh  # Общая поверхностная плотность
    gamma_eq = K * (gamma_m + gamma_sh)  # эквивалентная поверхностная плотность ограждения

    R_B = 20 * log10(gamma_eq) - 12
    R_B = round(R_B - 0.5) + 0.5

    h = (h_m + h_sh) * 1000  # толщинa ограждения, мм
    ro = (gamma_m + gamma_sh) / (h_m + h_sh)  # объемная плотность ограждения, кг / м3

    f_B = fy_ro(ro) / h

    f_B = f_to_f_1_3_50_5000(f_B)

    R_1_3_50_5000 = linspace(0, 0, 21)
    z = 0
    while z <= 20:
        if EEEtalon[z] <= f_B:
            R_1_3_50_5000[z] = R_B
            if R_1_3_50_5000[z] >= 65:
                R_1_3_50_5000[z] = 65
        elif EEEtalon[z] > f_B:
            if z == 0:
                R_1_3_50_5000[z] = R_B
                if R_1_3_50_5000[z] >= 65:
                    R_1_3_50_5000[z] = 65
            else:
                R_1_3_50_5000[z] = R_1_3_50_5000[z - 1] + 2
                if R_1_3_50_5000[z] >= 65:
                    R_1_3_50_5000[z] = 65
        z += 1

    R_1_3_100_3150 = list(R_1_3_50_5000[3:18])

    SSS_2 = list(R_1_3_50_5000)

    ui.setupUi(MainWindow)
    print('f_1_3_50_50000 =', EEEtalon)
    print()
    print('R_1_3_50_5000 = ', R_1_3_50_5000)
    print()
    print('R_1_3_100_3150 =', R_1_3_100_3150)

    stroka = "[  "
    for i in R_1_3_100_3150:
        stroka += str(i)
        stroka += "  "
    stroka += "]"
    print()
    print('R_1_3_100_3150 =', stroka)
    SLOI = 4

    ui.setupUi(MainWindow)
    x = EEEtalon
    y = R_1_3_50_5000

    plt.loglog(x, y)

    plt.title('Расчет') #имя графика вообще

    plt.xlim(50, 6000) #маштаб по x
    plt.ylim(20, 70) #маштаб по y

    plt.grid(True, color="violet",which='major', linestyle='-', alpha=1) #основная сетка
    plt.minorticks_on()
    plt.grid(True, which='minor', color="violet", linestyle='-', alpha=0.25) #второстепенная сетка

    # plt.xticks(np.arange(min(x), max(x) + 1, 1.0))  # изменяем шаг делений на оси X

    plt.xlabel('Частота f, Гц') #название x оси
    plt.ylabel('ЗИ, дБ') #название y оси
    plt.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
