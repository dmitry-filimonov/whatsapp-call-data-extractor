# Импортируем необходимые библиотеки
from PIL import Image
import pytesseract
from pytesseract import Output
import streamlit as st
import os

# Установка Tesseract OCR
def install_tesseract():
    if not os.path.isfile('/usr/bin/tesseract'):
        st.write("Installing Tesseract OCR...")
        os.system('sudo apt-get update')
        os.system('sudo apt-get install -y tesseract-ocr')
        st.write("Tesseract OCR installed.")

install_tesseract()

# Указываем путь к Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Функция для обработки изображения и извлечения данных
def process_image(image_path):
    image = Image.open(image_path)
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
