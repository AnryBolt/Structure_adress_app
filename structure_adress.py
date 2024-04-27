import numpy as np
import pandas as pd
def structure_adress(df,col_adr): 
  # на вход подаем датафрейм и название колонки с адресом

  # на выходе будет датафрейм с колонками:
  # col_adr	- исходный адрес в зависимости от названия колоки в датафрейме
  # adr_change	- структурированный адрес
  # type_str	- тип улицы
  # n_str	- номер улицы
  # street	- улица
  # number_house	- номер дома
  # corpus	- корпус
  # stroenie	- строение
  # kv - квартира

  import re
  import warnings
  warnings.simplefilter(action='ignore', category=FutureWarning)# уберем высвечивание предупреждений

  df['Исх_адр'] = df[col_adr]
  df[col_adr] = df[col_adr].str.replace(r"(?:бульвар|бульв|бул|б-р)\.?(?![А-я\-])","бульв.",regex=True)\
    .str.replace(r"аллея\.?(?![А-я\-])","аллея.",regex=True)\
    .str.replace(r"линия\.?(?![А-я\-])","линия.",regex=True)\
    .str.replace(r"просека?\.?(?![А-я\-])","просек.",regex=True)\
    .str.replace(r"тупик\.?(?![А-я\-])","тупик.",regex=True)\
    .str.replace(r"[Гг]ородок\.?(?![А-я\-])","городок.",regex=True)\
  \
    .str.replace(r"км\.?(?![А-я\-])|километр","км.",regex=True)\
    .str.replace(r"наб(ережная)?(?!\.])\.?(?![А-я\-])","наб.",regex=True)\
    .str.replace(r"пер(еулок)?\.?(?![А-я\-])","пер.",regex=True)\
    .str.replace(r"пл(ощадь)?\.?(?![А-я\-])","пл.",regex=True)\
    .str.replace(r"платформа\.?(?![А-я\-])","платф.",regex=True)\
    .str.replace(r"пос([её]лок)?\.?(?![А-я\-])","пос.",regex=True)\
    .str.replace(r"(?:пр-кт|проспект|просп)\.?(?![А-я\-])","пр-кт.",regex=True)\
    .str.replace(r"пр(-(з?д))?(оезд)?\.?(?![А-я\-])","пр-зд.",regex=True)\
    .str.replace(r"ул(ица)?\.?(?![А-я\-])","ул.",regex=True)\
    .str.replace(r"ш(оссе)?\.?(?![А-я\-])","ш.",regex=True)\
  \
    .str.replace("\.\.",".")
    
  df[col_adr] = np.where(df[col_adr].str.contains(r"\bБ\.",regex=True) & df[col_adr].str.contains(r"\b(?:аллея|линия|просек|наб|пл|платф|ул|)\.",regex=True),\
          df[col_adr].str.replace(r'\bБ\.', 'Большая',regex=True),\
          df[col_adr].str.replace(r'\bБ\.', 'Большой',regex=True))

  df[col_adr] = np.where(df[col_adr].str.contains(r"\bМ\.",regex=True) & df[col_adr].str.contains(r"\b(?:аллея|линия|просек|наб|пл|платф|ул|)\.",regex=True),\
          df[col_adr].str.replace(r'\bМ\.', 'Малая',regex=True),\
          df[col_adr].str.replace(r'\bМ\.', 'Малый',regex=True))

  type_str = r"(?:(аллея\.)|(бульв\.)|(городок\.)|(км\.)|(линия\.)|(наб\.)|(пер\.)|(пл\.)|(платф\.)|(пос\.)|(пр-зд\.)|(пр-кт\.)|(просек\.)|(тупик\.)|(ул\.)|(ш\.))"
  df['type_str'] = df[col_adr].astype(str).apply(lambda x: re.search(type_str, x).group() if re.search(type_str, x) is not None else "").to_frame()

  n_str = r"\b\d+-(я|го|й)\b|9(?= Мая)"
  df['n_str'] = df[col_adr].astype(str).apply(lambda x: re.search(n_str, x).group() if re.search(n_str, x) is not None else "").to_frame()

  reg_str = r"(?<=9 )Мая\b|(?:(?<=аллея\.)|(?<=бульв\.)|(?<=городок\.)|(?<=км\.)|(?<=линия\.)|(?<=наб\.)|(?<=пер\.)|(?<=пл\.)|(?<=платф\.)|(?<=пос\.)|(?<=пр-зд\.)|(?<=пр-кт\.)|(?<=просек\.)|(?<=тупик\.)|(?<=ул\.)|(?<=ш\.))( ?(\d+)(-(я|го|й))?)?( [БМ]\.)?( ?[А-Я][А-яё-]{2,}){1,2}\b|( [БМ]\.)?( ?[А-я][А-яё-]{2,}){1,2}\b\.?( [БМ]\.| Ср\.)?( ?(\d+)(-(я|го|й))?)? (?:(?=аллея\.)|(?=бульв\.)|(?=городок\.)|(?=км\.)|(?=линия\.)|(?=наб\.)|(?=пер\.)|(?=пл\.)|(?=платф\.)|(?=пос\.)|(?=пр-зд\.)|(?=пр-кт\.)|(?=просек\.)|(?=тупик\.)|(?=ул\.)|(?=ш\.))|\bМКАД,? \d+-й\b(?= км)"
  df['street'] = df[col_adr].astype(str).apply(lambda x: re.search(reg_str, x).group() if re.search(reg_str, x) is not None else "").to_frame()
  df['street'] = df['street'].str.replace(n_str, "",regex=True)

  corpus = r"(?:(?<=\bкорпус\b)|(?<=\bкорп\b)|(?<=\bк\b))\.? ?\d+(?: ?[А-Я]\b)?" #оставим только цифры и букву корпуса и некоторые символы
  df['corpus'] = df[col_adr].astype(str).apply(lambda x: re.search(corpus, x).group() if re.search(corpus, x) is not None else "").to_frame()
  corpus_number = r"\d+( ?[А-Я]\b)?" #удалим некоторые символы, оставив лишь только цифры
  df['corpus'] = df['corpus'].apply(lambda x: re.search(corpus_number, x).group() if re.search(corpus_number, x) is not None else "").to_frame()
  df['corpus'].str.replace(' ','')
  df['corpus'] = np.where(df['corpus'] == '', df['corpus'], "корп. " + df['corpus']) #добавим к номеру обозначение "корп."

  stroenie = r"(?:(?<=\bстроение\b)|(?<=\bстр\b)|(?<=\bст\b))\.? ?\d+\b" #оставим только цифры строения и некоторые символы
  df['stroenie'] = df[col_adr].astype(str).apply(lambda x: re.search(stroenie, x).group() if re.search(stroenie, x) is not None else "").to_frame()
  sroenie_number = r"\d+" #удалим некоторые символы, оставив лишь только цифры
  df['stroenie'] = df['stroenie'].apply(lambda x: re.search(sroenie_number, x).group() if re.search(sroenie_number, x) is not None else "").to_frame()
  df['stroenie'] = np.where(df['stroenie'] == '', df['stroenie'], "стр. " + df['stroenie']) #добавим к номеру обозначение "стр."

  kv = r"(?:(?<=\bкв\b))\.? ?\d+\b" #оставим только цифры квартиры и некоторые символы
  df['kv'] = df[col_adr].astype(str).apply(lambda x: re.search(kv, x).group() if re.search(kv, x) is not None else "").to_frame()
  kv_number = r"\d+" #удалим некоторые символы, оставив лишь только цифры
  df['kv'] = df['kv'].apply(lambda x: re.search(kv_number, x).group() if re.search(kv_number, x) is not None else "").to_frame()
  df['kv'] = np.where(df['kv'] == '', df['kv'], "кв. " + df['kv']) #добавим к номеру обозначение "кв."

  df['number_house'] = df[col_adr].str.replace(n_str,"",regex=True) # уберем номер счета улицы из адреса
  df['number_house'] = df['number_house'].str.replace(corpus,"",regex=True) # уберем номер корпуса из адреса
  df['number_house'] = df['number_house'].str.replace(stroenie,"",regex=True) # уберем номер строения из адреса
  df['number_house'] = df['number_house'].str.replace(kv,"",regex=True) # уберем номер квартиры из адреса

  number_house = r"(?:(?<=\bдом\b)|(?<=\bд.)|(?<=\bд\b)|(?<=владение\b)|(?<=влд\b)) ?\d+(?:/\d+)? ?([А-я]\b)?|\d+(?:/\d+)? ?([А-я]\b)?"
  df['number_house'] = df['number_house'].astype(str).apply(lambda x: re.search(number_house, x).group() if re.search(number_house, x) is not None else "").to_frame()#вычленим номер дома
  df['number_house'] = df['number_house'].str.replace("к","") #уберем лишние "к", так как они могут быть корпусом
  df['number_house'] = df['number_house'].str.replace(" ","")

  df['adr_change'] = df[['type_str', 'n_str', 'street', 'number_house', 'corpus', 'stroenie', 'kv']].agg(' '.join, axis=1)
  df['adr_change'] = df['adr_change'].str.replace("  ", " ").str.replace("  ", " ").str.replace("  ", " ")
  del df[col_adr]
  df = df[['Исх_адр', 'adr_change', 'type_str', 'n_str', 'street', 'number_house', 'corpus', 'stroenie', 'kv']]
  return df