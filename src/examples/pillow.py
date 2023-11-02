import streamlit as st
from PIL import Image, ImageFont, ImageDraw

def text_on_image(image, text, font_size, color):
    img = Image.open(image)
    font = ImageFont.truetype()
    draw = ImageDraw.Draw(img)
    iw, ih = img.size
    fw, fh = (15,15)
    draw.text(
        ((iw -fw) / 2, (ih - fh) / 2),
        text,
        fill=color,
        font=font
    )
    img.save('last_image.jpg')

image = st.file_uploader('Uma imagem', type=['jpg'])
text = st.text_input('Sua marca dágua')
color = st.selectbox(
    'Cor da sua marca', ['black', 'white', 'red', 'green']
)
color_2 = st.color_picker('Escolha uma cor')
font_size = st.number_input('Tamanho da fonte', min_value=50)

if image:
    result = st.button(
        'Aplicar',
        type='primary',
        on_click=text_on_image,
        args=(image, text, font_size, color)
    )
    if result:
        st.image('last_image.jpg')
        with open('last_image.jpg', 'rb') as file:
            st.download_button(
                'Baixe agora mesmo sua foto com marca',
                file_name='imagem_com_marca.jpg',
                data=file,
                mime='image/jpg'
            )
else:
    st.warning('Ainda não temos imagem')