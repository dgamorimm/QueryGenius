import streamlit as st
import vanna as vn


@st.cache_data(show_spinner="Gerando exemplos de perguntas ...")
def generate_questions_cached():
    return vn.generate_questions()


@st.cache_data(show_spinner="Gerando consulta SQL ...")
def generate_sql_cached(question: str):
    return vn.generate_sql(question=question)


@st.cache_data(show_spinner="Executando consulta SQL ...")
def run_sql_cached(sql: str):
    return vn.run_sql(sql=sql)


@st.cache_data(show_spinner="Gerando código Plotly ...")
def generate_plotly_code_cached(question, sql, df):
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Executando código Plotly ...")
def generate_plot_cached(code, df):
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Gerando perguntas de acompanhamento ...")
def generate_followup_cached(question, df):
    return vn.generate_followup_questions(question=question, df=df)