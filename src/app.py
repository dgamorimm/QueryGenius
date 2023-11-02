import time
import streamlit as st
from streamlit.components import v1 as components
from code_editor import code_editor
from static.html.title import TITLE
from utils.connection import setup_vanna, setup_session_state
from utils.calls import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
)

st.set_page_config(layout="wide")
setup_vanna()

st.sidebar.title("Configurações de saída")
st.sidebar.checkbox("SQL", value=True, key="show_sql")
st.sidebar.checkbox("Table", value=True, key="show_table")
st.sidebar.checkbox("Código Plotly", value=True, key="show_plotly_code")
st.sidebar.checkbox("Gráfico", value=True, key="show_chart")
st.sidebar.checkbox("Perguntas de acompanhamento", value=True, key="show_followup")
st.sidebar.button("Rerun", on_click=setup_session_state, use_container_width=True)

components.html(html=TITLE)
st.sidebar.write(st.session_state)

def set_question(question):
    st.session_state["my_question"] = question

assistant_message_suggested = st.chat_message(
    "assistant", avatar="src/images/querygenius-logo.png"
)
if assistant_message_suggested.button("Clique para mostrar perguntas sugeridas"):
    st.session_state["my_question"] = None
    questions = generate_questions_cached()
    for i, question in enumerate(questions):
        time.sleep(0.05)
        button = st.button(
            question,
            on_click=set_question,
            args=(question,),
        )

my_question = st.session_state.get("my_question", default=None)

if my_question is None:
    my_question = st.chat_input(
        "Faça-me uma pergunta sobre seus dados",
    )

if my_question:
    st.session_state["my_question"] = my_question
    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")

    sql = generate_sql_cached(question=my_question)

    if sql:
        if st.session_state.get("show_sql", True):
            assistant_message_sql = st.chat_message(
                "assistant", avatar="src/images/querygenius-logo.png"
            )
            assistant_message_sql.code(sql, language="sql", line_numbers=True)

        user_message_sql_check = st.chat_message("user")
        user_message_sql_check.write(f"Você está satisfeito com o código SQL gerado?")
        with user_message_sql_check:
            happy_sql = st.radio(
                "Feliz",
                options=["", "Sim", "Não", "Yes", "No"],
                key="radio_sql",
                index=0,
            )

        if happy_sql.lower() in ["não","no"]:
            st.warning(
                "Corrija o código SQL gerado. Quando terminar, pressione Shift + Enter para enviar"
            )
            sql_response = code_editor(sql, lang="sql")
            fixed_sql_query = sql_response["text"]

            if fixed_sql_query != "":
                df = run_sql_cached(sql=fixed_sql_query)
            else:
                df = None
        elif happy_sql.lower() in ["yes","sim"]:
            df = run_sql_cached(sql=sql)
        else:
            df = None

        if df is not None:
            st.session_state["df"] = df

        if st.session_state.get("df") is not None:
            if st.session_state.get("show_table", True):
                df = st.session_state.get("df")
                assistant_message_table = st.chat_message(
                    "assistant",
                    avatar="src/images/querygenius-logo.png",
                )
                if len(df) > 10:
                    assistant_message_table.text("Primeiras 10 linhas de dados")
                    assistant_message_table.dataframe(df.head(10))
                else:
                    assistant_message_table.dataframe(df)

            code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)

            if st.session_state.get("show_plotly_code", False):
                assistant_message_plotly_code = st.chat_message(
                    "assistant",
                    avatar="src/images/querygenius-logo.png",
                )
                assistant_message_plotly_code.code(
                    code, language="python", line_numbers=True
                )

            user_message_plotly_check = st.chat_message("user")
            user_message_plotly_check.write(
                f"Você está satisfeito com o código Plotly gerado?"
            )
            with user_message_plotly_check:
                happy_plotly = st.radio(
                    "Feliz",
                    options=["", "Sim", "Não", "Yes", "No"],
                    key="radio_plotly",
                    index=0,
                )

            if happy_sql.lower() in ["não","no"]:
                st.warning(
                    "Corrija o código Python gerado. Quando terminar, pressione Shift + Enter para enviar"
                )
                python_code_response = code_editor(code, lang="python")
                code = python_code_response["text"]
            elif happy_plotly == "":
                code = None

            if code is not None and code != "":
                if st.session_state.get("show_chart", True):
                    assistant_message_chart = st.chat_message(
                        "assistant",
                        avatar="src/images/querygenius-logo.png",
                    )
                    fig = generate_plot_cached(code=code, df=df)
                    if fig is not None:
                        assistant_message_chart.plotly_chart(fig)
                    else:
                        assistant_message_chart.error("Não consegui gerar um gráfico")

                if st.session_state.get("show_followup", True):
                    assistant_message_followup = st.chat_message(
                        "assistant",
                        avatar="src/images/querygenius-logo.png",
                    )
                    followup_questions = generate_followup_cached(
                        question=my_question, df=df
                    )
                    st.session_state["df"] = None

                    if len(followup_questions) > 0:
                        assistant_message_followup.text(
                            "Aqui estão algumas possíveis perguntas de acompanhamento"
                        )
                        # Print the first 5 follow-up questions
                        for question in followup_questions[:5]:
                            time.sleep(0.05)
                            assistant_message_followup.write(question)

    else:
        assistant_message_error = st.chat_message(
            "assistant", avatar="src/images/querygenius-logo.png"
        )
        assistant_message_error.error("Não consegui gerar SQL para essa pergunta")