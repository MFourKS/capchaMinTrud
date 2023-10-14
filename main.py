import json
import sys
import xlsxwriter
import array
import random
import time
import requests
import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup
from pytesseract import Output
import pytesseract
import argparse
import cv2
import easyocr
from PIL import Image, ImageEnhance
from keras.models import load_model
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np

def readspisok(INN):
        url = "https://declaration.rostrud.gov.ru/declaration/index?DeclarationSearch%5Binn%5D=" + INN + "&DeclarationSearch%5Bregion_id%5D=&DeclarationSearch%5Btele%5D=&DeclarationSearch%5Bverify%5D=0"

        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        # website page loaded
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        # ------------------------------------search for html elements on a page-----------------------------------
        table_header = soup.find(class_="table-responsive kv-grid-container").find("thead").find_all("th")
        all_character = soup.find(class_="table-responsive kv-grid-container").find("tbody").find_all("td")
        # ---------------------------------------------------------------------------------------------------------

        # set of variables for further use
        item_num = all_character[0].text

        if item_num.find('Ничего не найдено') != -1:
            return None

        return all_character


def mywritelnxls(full):
        # открываем новый файл на запись
        t = time.localtime()
        current_time = time.strftime("%Y.%m.%d_%H-%M-%S", t)

        filename = 'found_inn_' + current_time + '.xlsx'
        workbook = xlsxwriter.Workbook(filename)

        # создаем там "лист"
        worksheet = workbook.add_worksheet()

        # в ячейки пишем текст
        worksheet.write('A1', 'Полное наименование юр лица')
        worksheet.write('B1', 'Дата внесения сведений в реестр')
        worksheet.write('C1', 'Адрес')
        worksheet.write('D1', 'ИНН')
        worksheet.write('E1', 'ОГРН')
        worksheet.write('F1', 'Индивидуальный номер рабочего места')
        worksheet.write('G1', 'Профессия, должность, специальность работника')
        worksheet.write('H1', 'Численность работников на данном рабочем месте')
        worksheet.write('I1', 'Наименование организации проводившей спец оценку УТ')
        worksheet.write('J1', 'Реквизиты заключения эксперта организации, проводившей спец оценку УТ')
        worksheet.write('K1', 'Срок действия декларации')
        worksheet.write('L1', 'Дата прекращения действия декларации')

        for j in range(len(full)):
                all_character = full[j]

                worksheet.write('A' + str(j+2), all_character[1])
                worksheet.write('B' + str(j+2), all_character[2])
                worksheet.write('C' + str(j+2), all_character[3])
                worksheet.write('D' + str(j+2), all_character[4])
                worksheet.write('E' + str(j+2), all_character[5])
                worksheet.write('F' + str(j+2), all_character[6])
                worksheet.write('G' + str(j+2), all_character[7])
                worksheet.write('H' + str(j+2), all_character[8])
                worksheet.write('I' + str(j+2), all_character[9])
                worksheet.write('J' + str(j+2), all_character[10])
                worksheet.write('K' + str(j+2), all_character[11])
                worksheet.write('L' + str(j+2), all_character[12])

        # сохраняем и закрываем
        workbook.close()
        return 0


if __name__ == '__main__':
    # with open("INN.json") as file:
    #     INNspisok = file.readlines()
    #
    # full = []
    # i = 1
    # j = 1
    # for INN in INNspisok:
    #     INN = INN.rstrip()
    #     all_character = readspisok(INN)
    #
    #     uspeh = "Не найден"
    #
    #     if all_character != None:
    #         uspeh = "Найден на сайте Минтруда"
    #
    #         full.append({1 : all_character[2].text,
    #                      2 : all_character[1].text,
    #                      3 : all_character[3].text,
    #                      4 : all_character[4].text,
    #                      5 : all_character[5].text,
    #                      6 : all_character[6].text,
    #                      7 : all_character[7].text,
    #                      8 : all_character[8].text,
    #                      9 : all_character[9].text,
    #                      10 : all_character[10].text,
    #                      11 : all_character[11].text,
    #                      12 : all_character[12].text})
    #
    #     else:
    #         full.append({1:"", 2:"", 3:"", 4:INN, 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", 11:"", 12:""})
    #
    #     slp = random.uniform(5, 25)
    #     time.sleep(slp)
    #
    #     print(i, " ИНН : ", INN, " Результат запроса : " + uspeh)
    #     i += 1
    #
    #     #if j > 1000:
    #     if j >= 300:
    #         mywritelnxls(full)
    #         full.clear()
    #         j = 1
    #
    #     j += 1

    im = Image.open('captcha.jfif')
    filename = ''

    for i in range(4):
        filename = ''.join([str(i), '.png'])
        if i != 3 : im_crop = im.crop((25*i, 0, 34*(i+1), 55))
        else: im_crop = im.crop((30*i, 0, 120, 55))
        enhancer = ImageEnhance.Contrast(im_crop)
        im_output = enhancer.enhance(1.5)
        im_output = im_output.resize((30,55))
        im_output.save(filename, quality=95)



    reader = easyocr.Reader(["ru"])
    result = []
    for i in range(4):
        filename = ''.join([str(i),'.png'])
        if reader.readtext(filename, detail=0) != []:
            result +=reader.readtext(filename, detail=0)
        else:
            im = Image.open(filename)
            im_crop = im.crop((5, 10, 30, 55))
            enhancer = ImageEnhance.Contrast(im_crop)
            im_output = enhancer.enhance(1.5)
            im_output = im_output.resize((120,220))
            im_output.save(filename, quality=95)

            result += (reader.readtext(filename, detail=0))

    t = ''.join(result)

    url = "https://akot.rosmintrud.ru/sout/Statistics/varorganization?Inn=7325041274&Ogrn=&Captcha=" + t

    # headers = {
    #     "Accept": "*/*",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    # }
    # # website page loaded
    # req = requests.get(url, headers=headers)
    # src = req.text
    #
    # soup = BeautifulSoup(src, "lxml")
    #
    #
    # table_info = soup.find(class_="table table-striped table-hover").find("tr").find_all("td")


    print(url)