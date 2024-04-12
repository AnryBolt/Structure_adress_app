import streamlit as sl
import pandas as pd
from structure_adress import structure_adress



sl.title('Унификация географических адресов')
#sl.subheader('Подтверждения')

inp = sl.chat_input('Введи адреса стопкой')

if inp != None:
    col1, col2 = sl.columns(2)
    addresses = inp.split('\n')
    df = pd.DataFrame({'Исходный адрес': addresses})
    sl.dataframe(structure_adress(df, 'Исходный адрес'))

    sl.text('1. Наведи на нулевую строку нужного столбца \
            \n2. Нажми CTRL + SHIFT + ↓ \
            \n3. Нажми CTRL + C для копирования выделенного\
            \n4. Нажми CTRL + V в нужном месте документа для вставки')



