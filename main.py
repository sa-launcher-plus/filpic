import sys
import os
import easygui
import sqlite3

from PIL import Image, ImageFilter, ImageDraw, ImageFont
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QSlider


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data\\window.ui', self)
        self.text_status.setReadOnly(True)
        self.last_filter_line.setReadOnly(True)
        self.take_img_but.clicked.connect(self.take_img)
        self.folder_to_img_but.clicked.connect(self.folder_img)
        self.blur_but.clicked.connect(self.blur)
        self.contour_but.clicked.connect(self.contour)
        self.ee_but.clicked.connect(self.ee)
        self.eem_but.clicked.connect(self.eem)
        self.emboss_but.clicked.connect(self.emboss)
        self.fe_but.clicked.connect(self.fe)
        self.but_quant.clicked.connect(self.quant)
        self.negativ_but.clicked.connect(self.negativ)
        self.but_gaus.clicked.connect(self.gaus)
        self.gbr_but.clicked.connect(self.gbr)
        self.rbg_but.clicked.connect(self.rbg)
        self.pushButton_3.clicked.connect(self.grb)
        self.bgr_but.clicked.connect(self.bgr)
        self.hbi_but.clicked.connect(self.hbe)
        self.inst_but.clicked.connect(self.open_instruction)
        self.dop_info_but.clicked.connect(self.open_information)
        self.open_converter_but.clicked.connect(self.open_converter)
        self.save_img_but.clicked.connect(self.img_save)
        self.text_status.setText('Перед началом работы, выберите изображение')
        self.quant_slider.setMinimum(1)
        self.quant_slider.setMaximum(35)
        self.quant_slider.valueChanged.connect(self.slider_quant)
        self.gaus_slider.setMinimum(1)
        self.gaus_slider.setMaximum(35)
        self.gaus_slider.valueChanged.connect(self.slider_gaus)

        self.fname = None
        self.quant_num = 35
        self.gaus_num = 1

        self.font = ImageFont.truetype('data\\8477.ttf')
        self.filt = ''

        self.db = sqlite3.connect('data\\server.db')
        self.sql = self.db.cursor()

        for value in self.sql.execute("SELECT filter FROM data"):
            self.txt = ('Последний вами используемый фильтр - ' + value[0])
        self.last_filter_line.setText(self.txt)

    def img_save(self):
        self.img.save('images\\' + self.filt + '_filpic.png')
        self.text_status.setText('Готово, изображение ' + self.filt + ' сохранено в папку')

    def take_img(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', "*.png *.jpg *.bmp *.webp *.pdf *.gif")[0]
        if self.fname != '':
            self.text_status.setText('Вы выбрали изображение, используйте теперь фильтры')
        else:
            self.text_status.setText('Вы не выбрали изображение, повторите попытку')
            self.fname = None

    def folder_img(self):
        dir = os.path.abspath(os.curdir)
        os.system(r"explorer.exe " + dir + '\images')

    def slider_quant(self, value):
        self.quant_num = value
        self.res_quant_label.setText(str(value))

    def slider_gaus(self, value):
        self.gaus_num = value
        self.res_gaus_label.setText(str(value))

    def blur(self):
        if self.fname is not None:  # Проверка взятия изображение перед использованием функции
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.BLUR)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра BLUR,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра BLUR')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.BLUR)
            self.filt = 'BLUR'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('BLUR', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием BLUR, выберите изображение!')

    def contour(self):
        if self.fname is not None:  # Проверка взятия изображение перед использованием функции
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.CONTOUR)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра CONTOUR,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра CONTOUR')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.CONTOUR)
            self.filt = 'CONTOUR'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('CONTOUR', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием CONTOUR, выберите изображение')

    def ee(self):
        if self.fname is not None:  # Проверка взятия изображение перед использованием функции
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.EDGE_ENHANCE)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра EDGE ENHANCE,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра EDGE ENHANCE')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.EDGE_ENHANCE)
            self.filt = 'EDGE ENHANCE'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('EDGE ENHANCE', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием EDGE ENHANCE, выберите изображение')

    def eem(self):
        if self.fname is not None:  # Проверка взятия изображение перед использованием функции
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра EDGE ENHANCE MORE,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра EDGE ENHANCE MORE')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            self.filt = 'EDGE ENHANCE MORE'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('EDGE ENHANCE MORE', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием EEM, выберите изображение')

    def emboss(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.EMBOSS)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра EMBOSS,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра EMBOSS')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.EMBOSS)
            self.filt = 'EMBOSS'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('EMBOSS', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием EMBOSS, выберите изображение')

    def fe(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.FIND_EDGES)
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра FIND EDGES,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра FIND EDGES')

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.FIND_EDGES)
            self.filt = 'FIND EDGES'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('EMBOSS', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием FIND EDGES, выберите изображение')

    def quant(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()
            x, y = im2.size
            im2 = im2.quantize(self.quant_num)
            self.text_status.setText('Предворительный просмотр фильтра QUANT')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            self.img = self.img.quantize(self.quant_num)
            self.filt = 'QUANT'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('QUANT', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием QUANT, выберите изображение')

    def negativ(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = 255 - r, 255 - g, 255 - b
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра НЕГАТИВ,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра НЕГАТИВ')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = 255 - r, 255 - g, 255 - b
            self.filt = 'НЕГАТИВ'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('НЕГАТИВ', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием НЕГАТИВ, выберите изображение')

    def gaus(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            im2 = im2.filter(ImageFilter.GaussianBlur(radius=self.gaus_num))
            self.text_status.setText('Предворительный просмотр размытого изображения')
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр размытого изображения,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))

            im2.show()

            self.img = Image.open(self.fname)
            self.img = self.img.filter(ImageFilter.GaussianBlur(radius=self.gaus_num))
            self.filt = 'RAZMYTIE'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('Размытие по Гаусу', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием размытия, выберите изображение')

    def gbr(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = g, b, r
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра GBR,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра GBR')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = g, b, r
            self.filt = 'GBR'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('GBR', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием GBR, выберите изображение')

    def rbg(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = r, b, g
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра RBG,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра RBG')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = r, b, g
            self.filt = 'RBG'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('RBG', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием RBG, выберите изображение')

    def grb(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = g, r, b
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра GRB,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра GRB')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = g, r, b
            self.filt = 'GRB'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('GRB', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием GRB, выберите изображение')

    def bgr(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = b, g, r
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр фильтра BGR,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр фильтра BGR')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    pixels[i, j] = b, g, r
            self.filt = 'BGR'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('BGR', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием BGR, выберите изображение')

    def hbe(self):
        if self.fname is not None:
            im2 = Image.open(self.fname)
            pixels = im2.load()  # список с пикселями
            x, y = im2.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    bw = (r + g + b) // 3
                    pixels[i, j] = bw, bw, bw
            draw_text = ImageDraw.Draw(im2)
            draw_text.text((1, 1),
                           'Предворительный просмотр черно-белого фильтра,\nпосле нажатия на кнопку "Сохранить изображение"\nизображение сохраниться в папку\n \nИзображение можно не сохранять,\nа выбрать другой фильтр или изображение..',
                           font=self.font,
                           fill=('#ff3b3b'))
            self.text_status.setText('Предворительный просмотр чёрно-белого фильтра')

            im2.show()

            self.img = Image.open(self.fname)
            pixels = self.img.load()  # список с пикселями
            x, y = self.img.size  # ширина (x) и высота (y) изображения
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    bw = (r + g + b) // 3
                    pixels[i, j] = bw, bw, bw
            self.filt = 'ЧБИ'

            self.sql.execute("DELETE FROM data")
            self.db.commit()
            self.sql.execute(f"INSERT INTO data VALUES (?, ?)", ('Черно-белое изображение (ЧБИ)', ''))
            self.db.commit()
            for value in self.sql.execute("SELECT filter FROM data"):
                self.txt = ('Последний вами используемый фильтр - ' + value[0])
                break
            self.last_filter_line.setText(self.txt)
        else:
            self.text_status.setText('Перед использованием ЧБИ, выберите изображение')

    def open_converter(self):
        self.second_form = SecondForm(self, "Данные для второй формы")
        self.second_form.show()

    def open_instruction(self):
        self.third_form = ThirdForm(self, "Данные для второй формы")
        self.third_form.show()

    def open_information(self):
        self.info_form = InfodForm(self, "Данные для второй формы")
        self.info_form.show()


class ThirdForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('data\\instruction.ui', self)
        self.plainTextEdit.setReadOnly(True)


class InfodForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('data\\information.ui', self)
        self.text_info.setReadOnly(True)


class SecondForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('data\\converter.ui', self)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText('Перед началом работы, выберите изображения')
        self.pushButton.clicked.connect(self.img_folder)
        self.more_imgs_but.clicked.connect(self.img_more)
        self.png_but.clicked.connect(self.png)
        self.jpg_but.clicked.connect(self.jpg)
        self.bmp_but.clicked.connect(self.bmp)
        self.gif_but.clicked.connect(self.gif)
        self.pdf_but.clicked.connect(self.pdf)
        self.webp_but.clicked.connect(self.webp)
        self.ultrahd_but.clicked.connect(self.ultra_hd)
        self.fullhd_but.clicked.connect(self.full_hd)
        self.hd_but.clicked.connect(self.hd)
        self.p480_but.clicked.connect(self.p480)
        self.p360_but.clicked.connect(self.p360)
        self.p240_but.clicked.connect(self.p240)
        self.input_file = None

    def img_more(self):
        self.input_file = easygui.fileopenbox(filetypes=["*.png"], multiple=True)
        if self.input_file is not None:
            self.lineEdit.setText('Изображения выбрано, используйте конвертер')
            self.stat = 1
        else:
            self.lineEdit.setText('Изображения не выбрано, повторите попытку')

    def img_folder(self):
        dir = os.path.abspath(os.curdir)
        os.system(r"explorer.exe " + dir + '\images')

    def png(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'PNG_ConPic.png')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .PNG изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием PNG, выберите картинки')

    def jpg(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'JPG_ConPic.jpg')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .JPG изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием JPG, выберите картинки')

    def bmp(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'BMP_ConPic.bmp')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .BMP изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием BMP, выберите картинки')

    def gif(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'GIF_ConPic.gif')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .GIF изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием GIF, выберите картинки')

    def pdf(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'PDF_ConPic.pdf')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .PDF изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием PDF, выберите картинки')

    def webp(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                result = ('images\\' + str(num) + 'WebP_ConPic.webp')
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, .WebP изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием WebP, выберите картинки')

    def ultra_hd(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((3840, 2160))
                result = ('images\\' + str(num) + '_ULTRA_HD_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 4K изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием 4K, выберите картинки')

    def full_hd(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((1920, 1080))
                result = ('images\\' + str(num) + '_FULL_HD_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 1080p изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием FULL HD, выберите картинки')

    def hd(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((1280, 720))
                result = ('images\\' + str(num) + '_HD_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 720p изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием HD, выберите картинки')

    def p480(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((854, 480))
                result = ('images\\' + str(num) + '_480p_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 480p изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием 480p, выберите картинки')

    def p360(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((480, 360))
                result = ('images\\' + str(num) + '_360p_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 360p изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием 360p, выберите картинки')

    def p240(self):
        if self.input_file is not None:
            num = 1
            for i in self.input_file:
                img = Image.open(i)
                img.thumbnail((320, 240))
                result = ('images\\' + str(num) + '_240p_ConPic.' + i.split('.')[-1])
                img.save(result)
                num += 1

            self.lineEdit.setText('Готово, 240p изображения сохранено в папку')
        else:
            self.lineEdit.setText('Перед использованием 240p, выберите картинки')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
