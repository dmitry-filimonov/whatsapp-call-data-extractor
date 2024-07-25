# Импортируем необходимые библиотеки
from PIL import Image
import tesserocr
import streamlit as st
import os

# Функция для обработки изображения и извлечения данных
def process_image(image_path):
    image = Image.open(image_path)
    text = tesserocr.image_to_text(image, lang='rus')
    
    phone_number = None
    call_date = None
    call_duration = None
    
    lines = text.split('\n')
    for line in lines:
        if line.startswith('+7'):
            phone_number = line.strip()
        elif 'г.' in line:
            call_date = line.strip()
        elif 'секунд' in line:
            call_duration = line.strip()
    
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
