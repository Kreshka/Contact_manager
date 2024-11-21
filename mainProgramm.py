import sys
import sqlite3
import io
from PyQt6 import uic, QtCore, QtWidgets  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QButtonGroup, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path

msg = MIMEMultipart()

addForm = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>382</width>
    <height>355</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Добавить клиента</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>20</y>
     <width>51</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>ФИО</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="fns">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>20</y>
     <width>291</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="layoutDirection">
    <enum>Qt::LeftToRight</enum>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>80</y>
     <width>51</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Mail</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="mail">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>80</y>
     <width>291</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="layoutDirection">
    <enum>Qt::LeftToRight</enum>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>140</y>
     <width>151</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Номер телефона</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="tfnm">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>140</y>
     <width>201</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="layoutDirection">
    <enum>Qt::LeftToRight</enum>
   </property>
   <property name="text">
    <string>+7</string>
   </property>
  </widget>
  <widget class="QPushButton" name="addBtn">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>280</y>
     <width>321</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Добавить</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>190</y>
     <width>151</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Дата рождения</string>
   </property>
  </widget>
  <widget class="QDateEdit" name="dateb">
   <property name="geometry">
    <rect>
     <x>160</x>
     <y>200</y>
     <width>211</width>
     <height>31</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
  </widget>
  <widget class="QRadioButton" name="wm">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>250</y>
     <width>71</width>
     <height>21</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Жен</string>
   </property>
  </widget>
  <widget class="QRadioButton" name="m">
   <property name="geometry">
    <rect>
     <x>200</x>
     <y>250</y>
     <width>101</width>
     <height>21</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Муж</string>
   </property>
  </widget>
  <widget class="Line" name="line">
   <property name="geometry">
    <rect>
     <x>180</x>
     <y>250</y>
     <width>20</width>
     <height>21</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Vertical</enum>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
addForm = io.StringIO(addForm)

deleteForm = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>485</width>
    <height>456</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Найти/Удалить клиента</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>20</y>
     <width>191</width>
     <height>61</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Параметр удаления</string>
   </property>
  </widget>
  <widget class="QComboBox" name="chB">
   <property name="geometry">
    <rect>
     <x>200</x>
     <y>30</y>
     <width>271</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <item>
    <property name="text">
     <string>ID</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Имя</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Фамилия</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Провайдер почты</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Номер телефона</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Пол(М/Ж)</string>
    </property>
   </item>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>90</y>
     <width>191</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Значение параметра</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="inp">
   <property name="geometry">
    <rect>
     <x>200</x>
     <y>100</y>
     <width>271</width>
     <height>31</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
  </widget>
  <widget class="QPushButton" name="delBtn">
   <property name="geometry">
    <rect>
     <x>260</x>
     <y>380</y>
     <width>211</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Удалить</string>
   </property>
  </widget>
  <widget class="QPushButton" name="findB">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>380</y>
     <width>221</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Найти</string>
   </property>
  </widget>
  <widget class="QTableWidget" name="table2">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>160</y>
     <width>451</width>
     <height>201</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>7</pointsize>
    </font>
   </property>
  </widget>
  <widget class="Line" name="line">
   <property name="geometry">
    <rect>
     <x>190</x>
     <y>140</y>
     <width>118</width>
     <height>16</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Horizontal</enum>
   </property>
  </widget>
  <widget class="Line" name="line_2">
   <property name="geometry">
    <rect>
     <x>240</x>
     <y>380</y>
     <width>20</width>
     <height>51</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Vertical</enum>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
deleteForm = io.StringIO(deleteForm)

mailingForm = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>503</width>
    <height>630</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Создать рассылку</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>20</y>
     <width>191</width>
     <height>61</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Параметр рассылки</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>90</y>
     <width>191</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Значение параметра</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="inp">
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>100</y>
     <width>271</width>
     <height>31</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
  </widget>
  <widget class="QComboBox" name="chB">
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>30</y>
     <width>271</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <item>
    <property name="text">
     <string>ID</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Имя</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Фамилия</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Провайдер почты</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Номер телефона</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Пол(М/Ж)</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Всем</string>
    </property>
   </item>
  </widget>
  <widget class="QPushButton" name="crtBtn">
   <property name="geometry">
    <rect>
     <x>90</x>
     <y>560</y>
     <width>321</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Создать</string>
   </property>
  </widget>
  <widget class="Line" name="line">
   <property name="geometry">
    <rect>
     <x>190</x>
     <y>530</y>
     <width>118</width>
     <height>16</height>
    </rect>
   </property>
   <property name="orientation">
    <enum>Qt::Horizontal</enum>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>210</y>
     <width>191</width>
     <height>81</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Введите текст 
рассылки или 
выберите файл</string>
   </property>
  </widget>
  <widget class="QPushButton" name="openTxt">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>300</y>
     <width>121</width>
     <height>91</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Выбрать файл
(txt)</string>
   </property>
  </widget>
  <widget class="QPlainTextEdit" name="body">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>220</y>
     <width>321</width>
     <height>291</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
  </widget>
  <widget class="QLineEdit" name="tm">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>160</y>
     <width>321</width>
     <height>31</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>150</y>
     <width>191</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Тема рассылки</string>
   </property>
  </widget>
  <widget class="QPushButton" name="infBtn">
   <property name="geometry">
    <rect>
     <x>480</x>
     <y>0</y>
     <width>21</width>
     <height>21</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>11</pointsize>
    </font>
   </property>
   <property name="text">
    <string>i</string>
   </property>
  </widget>
  <widget class="QPushButton" name="delB">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>400</y>
     <width>121</width>
     <height>91</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Удалить
учетную
запись</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
mailingForm = io.StringIO(mailingForm)

main = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Base</class>
 <widget class="QMainWindow" name="Base">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>844</width>
    <height>407</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string> </string>
  </property>
  <property name="layoutDirection">
   <enum>Qt::RightToLeft</enum>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="addB">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>180</y>
      <width>171</width>
      <height>61</height>
     </rect>
    </property>
    <property name="text">
     <string>Добавить клиента</string>
    </property>
   </widget>
   <widget class="QPushButton" name="createB">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>320</y>
      <width>171</width>
      <height>61</height>
     </rect>
    </property>
    <property name="text">
     <string>Сделать рассылку</string>
    </property>
   </widget>
   <widget class="QPushButton" name="updateB">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>110</y>
      <width>171</width>
      <height>61</height>
     </rect>
    </property>
    <property name="cursor">
     <cursorShape>ArrowCursor</cursorShape>
    </property>
    <property name="text">
     <string>Обновить таблицу</string>
    </property>
   </widget>
   <widget class="QPushButton" name="deleteB">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>250</y>
      <width>171</width>
      <height>61</height>
     </rect>
    </property>
    <property name="text">
     <string>Найти/Удалить клиента</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>20</y>
      <width>371</width>
      <height>61</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>24</pointsize>
     </font>
    </property>
    <property name="focusPolicy">
     <enum>Qt::TabFocus</enum>
    </property>
    <property name="layoutDirection">
     <enum>Qt::RightToLeft</enum>
    </property>
    <property name="autoFillBackground">
     <bool>false</bool>
    </property>
    <property name="text">
     <string>Менеджер контактов</string>
    </property>
   </widget>
   <widget class="QTableView" name="table">
    <property name="geometry">
     <rect>
      <x>210</x>
      <y>110</y>
      <width>621</width>
      <height>271</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>MS Shell Dlg 2</family>
      <pointsize>10</pointsize>
      <weight>50</weight>
      <italic>false</italic>
      <bold>false</bold>
     </font>
    </property>
    <property name="cursor" stdset="0">
     <cursorShape>ArrowCursor</cursorShape>
    </property>
    <property name="layoutDirection">
     <enum>Qt::LeftToRight</enum>
    </property>
   </widget>
   <widget class="QPushButton" name="cleanB">
    <property name="geometry">
     <rect>
      <x>800</x>
      <y>0</y>
      <width>21</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>C</string>
    </property>
   </widget>
   <widget class="Line" name="line">
    <property name="geometry">
     <rect>
      <x>190</x>
      <y>110</y>
      <width>21</width>
      <height>271</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Vertical</enum>
    </property>
   </widget>
   <widget class="Line" name="line_2">
    <property name="geometry">
     <rect>
      <x>370</x>
      <y>80</y>
      <width>118</width>
      <height>21</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
main = io.StringIO(main)

regForm = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>481</width>
    <height>230</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>481</width>
    <height>0</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Регистрация</string>
  </property>
  <widget class="QLineEdit" name="mailinp">
   <property name="geometry">
    <rect>
     <x>250</x>
     <y>30</y>
     <width>221</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>20</y>
     <width>281</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Введите почту, с которой
 хотите делать рассылку</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>90</y>
     <width>231</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <family>MS Shell Dlg 2</family>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Введите пароль от почты</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="passwordinp">
   <property name="geometry">
    <rect>
     <x>250</x>
     <y>90</y>
     <width>221</width>
     <height>41</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>14</pointsize>
    </font>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="addBtn">
   <property name="geometry">
    <rect>
     <x>90</x>
     <y>160</y>
     <width>321</width>
     <height>51</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>12</pointsize>
    </font>
   </property>
   <property name="text">
    <string>Зарегестрироваться</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
regForm = io.StringIO(regForm)


def send_emails(receiver_emails, subject, body, sender_email, password):
    smtp_server = smtplib.SMTP(f"smtp.{sender_email.split('@')[1]}", 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, password)
    # Настройка параметров сообщения
    msg["From"] = sender_email
    msg["To"] = ''
    msg["Subject"] = subject

    # Добавление текста в сообщение
    msg.attach(MIMEText(body, "plain"))
    smtp_server.sendmail(sender_email, receiver_emails, msg.as_string())

    # Закрытие соединения
    smtp_server.quit()


class RegDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(regForm, self)  # Загружаем дизайн
        self.addBtn.clicked.connect(self.reg)

    def reg(self):
        with open('date.txt', "w") as file:
            mail = self.mailinp.text()
            password = self.passwordinp.text()
            file.write(f"{mail}\n{password}")
        QMessageBox.information(self, " ", "Вы успешно зарегестрировались!")
        self.close()


class MailingDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(mailingForm, self)  # Загружаем дизайн
        self.crtBtn.clicked.connect(self.createM)
        self.d = RegDialog()
        self.openTxt.clicked.connect(self.opnTxt)
        self.delB.clicked.connect(self.delReg)

    def delReg(self):
        if os.path.exists("date.txt"):
            os.remove("date.txt")
            QMessageBox.information(self, " ", "Учетная запись сброшена!")
        else:
            QMessageBox.critical(self, " ", "Вы не зарегестрировались!")

    def createDialog(self):
        self.show()
        if not os.path.exists("date.txt"):
            self.d.show()

    def opnTxt(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберете файл', '', "Текст (*.txt)")[0]
        with open(fname, "r", encoding="utf-8") as file:
            self.body.setPlainText(file.read())

    def createM(self):
        try:
            with open('date.txt', "r") as file:
                date = file.read().split("\n")
                mail = date[0]
                password = date[1]
        except:
            QMessageBox.critical(self, " ", "Вы не зарегестрировались!")
            self.close()
        else:
            tp = self.chB.currentIndex()
            gt = self.inp.text()
            com = ""
            if tp == 0:
                if gt.isdigit():
                    com = f"""
                                    SELECT mail FROM users
                                    WHERE id = {int(gt)};
                                    """
                else:
                    QMessageBox.critical(self, " ", "Введите число")

            elif tp == 1:
                com = f"""
                                SELECT mail FROM users
                                WHERE name = "{gt}";
                                """
            elif tp == 2:
                com = f"""
                                SELECT mail FROM users
                                WHERE surname = "{gt}";
                                """
            elif tp == 3:
                com = f"""
                                SELECT mail FROM users
                                WHERE mail LIKE "%{gt}%";
                                """
            elif tp == 4:
                com = f"""
                                SELECT mail FROM users
                                WHERE phone_number = "{gt}";
                                """
            elif tp == 5:
                com = f"""
                                SELECT mail FROM users
                                WHERE gender = "{gt}";
                                """
            elif tp == 6:
                com = f"""
                                SELECT mail FROM users;
                                """

            con = sqlite3.connect("dbUsers.sqlite")
            cur = con.cursor()
            cur.execute(com)
            lst = list(map(lambda x: x[0], cur.fetchall()))
            con.close()
            try:
                send_emails(lst, self.tm.text(), self.body.toPlainText(), mail, password)
                QMessageBox.information(self, " ", "Рассылка успешно отправлена!")
            except:
                QMessageBox.critical(self, " ", "Рассылка прервалась из-за ошибки")
            self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(deleteForm, self)  # Загружаем дизайн
        self.delBtn.clicked.connect(self.delete)
        self.findB.clicked.connect(self.findd)

    def findd(self):
        self.table2.clear()
        self.table2.setRowCount(0)
        self.table2.setColumnCount(0)
        tp = self.chB.currentIndex()
        gt = self.inp.text()
        com = ""
        if tp == 0:
            if gt.isdigit():
                com = f"""
                        SELECT * FROM users
                        WHERE id = {int(gt)};
                        """
            else:
                QMessageBox.critical(self, " ", "Введите число")
        elif tp == 1:
            com = f"""
                    SELECT * FROM users
                    WHERE name = "{gt}";
                    """
        elif tp == 2:
            com = f"""
                    SELECT * FROM users
                    WHERE surname = "{gt}";
                    """
        elif tp == 3:
            com = f"""
                    SELECT * FROM users
                    WHERE mail LIKE "%{gt}%";
                    """
        elif tp == 4:
            com = f"""
                    SELECT * FROM users
                    WHERE phone_number = "{gt}";
                    """
        elif tp == 5:
            com = f"""
                    SELECT * FROM users
                    WHERE gender = "{gt}";
                    """

        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute(com)
        lst = cur.fetchall()
        con.close()
        if len(lst):
            self.table2.setRowCount(len(lst))
            self.table2.setColumnCount(len(lst[0]) - 1)
            self.table2.setHorizontalHeaderLabels(
                ("name", "surname", "patronymic", "mail", "phone_number", "date_of_birth", "gender"))
            for i, j in enumerate(lst):
                for i2, k in enumerate(j[1:]):
                    self.table2.setItem(i, i2, QTableWidgetItem(k))
            self.table2.resizeColumnsToContents()

    def delete(self):
        f = 0
        tp = self.chB.currentIndex()
        gt = self.inp.text()
        com = ""
        if tp == 0:
            if not gt.isdigit():
                QMessageBox.critical(self, " ", "Введите число")
                f = 1
            else:
                com = f"""
                DELETE FROM users
                WHERE id = {int(gt)};
                """
        elif tp == 1:
            com = f"""
            DELETE FROM users
            WHERE name = "{gt}";
            """
        elif tp == 2:
            com = f"""
            DELETE FROM users
            WHERE surname = "{gt}";
            """
        elif tp == 3:
            com = f"""
            DELETE FROM users
            WHERE mail LIKE "%{gt}%";
            """
        elif tp == 4:
            com = f"""
            DELETE FROM users
            WHERE phone_number = "{gt}";
            """
        elif tp == 5:
            com = f"""
            DELETE FROM users
            WHERE gender = "{gt}";
            """

        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute(com)
        con.commit()
        con.close()
        self.close()
        if not f:
            QMessageBox.information(self, " ", "Контакт удален")
        self.inp.clear()


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(addForm, self)  # Загружаем дизайн
        self.addBtn.clicked.connect(self.crt)
        self.wm.setAutoExclusive(False)
        self.m.setAutoExclusive(False)

    def crt(self):
        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        try:
            f, n, s = self.fns.text().split()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО через пробел")
        else:
            mail = self.mail.text()
            tfnm = self.tfnm.text()
            dbb = self.dateb.text()
            gender = "Ж" if self.wm.isChecked() else "М" if self.m.isChecked() else "-"
            if not "@" in mail:
                QMessageBox.warning(self, "Ошибка", "Введите правильный mail")
            elif tfnm == "+7":
                QMessageBox.warning(self, "Ошибка", "Введите правильный номер телефона")
            else:
                cur.execute(f'''INSERT INTO users(name, surname, patronymic, mail, phone_number, date_of_birth, gender) 
                VALUES ("{n}", "{f}", "{s}", "{mail}", "{tfnm}", "{dbb}", "{gender}")''')
                con.commit()
        self.close()
        self.fns.clear()
        self.mail.clear()
        self.tfnm.setText("+7")
        self.dateb.setDateTime(QDateTime(2000, 1, 1, 10, 20))
        self.wm.setChecked(False)
        self.m.setChecked(False)
        con.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(main, self)  # Загружаем дизайн
        self.addB.clicked.connect(self.add)
        self.updateB.clicked.connect(self.updatee)
        self.cleanB.clicked.connect(self.cleann)
        self.deleteB.clicked.connect(self.delete)
        self.createB.clicked.connect(self.createe)

        self.d1 = AddDialog()
        self.d2 = DeleteDialog()
        self.d3 = MailingDialog()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('dbUsers.sqlite')
        self.db.open()
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('users')
        self.model.select()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        # self.table.hideColumn(0)
        self.table.verticalHeader().setVisible(0)

    def add(self):
        self.d1.show()

    def cleann(self):
        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM sqlite_sequence")
        con.commit()
        con.close()

    def createe(self):
        self.d3.createDialog()

    def delete(self):
        self.d2.show()

    def updatee(self):
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('users')
        self.model.select()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
