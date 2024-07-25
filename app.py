# Импортируем необходимые библиотеки
import cv2
import pytesseract
from pytesseract import Output
import streamlit as st
import os

# Указываем путь к Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Функция для обработки изображения и извлечения данных
def process_image(image_path):
    image = cv2.imread(image_path)
    custom_config = r'--oem 3 --psm 6 -l rus'
    d = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
    
    phone_number = None
    call_date = None
    call_duration = None
    
    for i in range(len(d['text'])):
        if d['text'][i] == '+7':
            phone_number = d['text'][i] + ' ' + d['text'][i+1] + ' ' + d['text'][i+2] + ' ' + d['text'][i+3]
        if 'г.' in d['text'][i]:
            call_date = d['text'][i-2] + ' ' + d['text'][i-1] + ' ' + d['text'][i]
        if 'секунд' in d['text'][i]:
            call_duration = d['text'][i-3] + ' ' + d['text'][i-2] + ' ' + d['text'][i-1] + ' ' + d['text'][i]
    
    return phone_number, call_date, call_duration

# Интерфейс Streamlit
st.title("WhatsApp Call Data Extractor")
uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp_image.jpg", caption="Загруженное изображение", use_column_width=True)
    
    phone_number, call_date, call_duration = process_image("temp_image.jpg")
    
    st.write(f'Номер телефона: {phone_number}')
    st.write(f'Дата звонка: {call_date}')
    st.write(f'Длительность звонка: {call_duration}')