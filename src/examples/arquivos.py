import streamlit as st
from json import loads
from pandas import read_csv

st.markdown('''
    # Exibidor de arquivos
    
    ## Suba um arquivo e vejamos o que acontece :smile::heart:
''')

arquivo = st.file_uploader(
    'Suba seu arquivo aqui',
    type=['jpg', 'png', 'py', 'wav', 'csv', 'json']
)

st.text_input('Email', max_chars=100, autocomplete=True)
st.text_input('Senha', type='password')

if arquivo:
    print(arquivo.type)
    match arquivo.type.split('/'):
        case 'application', 'json':
            st.json(loads(arquivo.read()))
        case 'image', _:
            st.image(arquivo)
        case 'text', 'csv':
            df = read_csv(arquivo)
            st.dataframe(df)
            st.bar_chart(df[['Education']])
        case 'audio', _:
            st.audio(arquivo)
        case 'text', 'x-python':
            st.code(body=arquivo.read().decode(), line_numbers=True,language='python')
else:
    st.error('Ainda não tenho arquivo')