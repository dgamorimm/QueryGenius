import os
import streamlit as st
import vanna as vn
from dotenv import load_dotenv


@st.cache_resource(ttl=3600)
def setup_vanna():
    if "vanna_api_key" in st.secrets and "gcp_project_id" in st.secrets:
        vn.set_api_key(st.secrets.get("vanna_api_key"))
        vn.set_model("thelook")
    else:
        load_dotenv()
        vn.set_api_key(os.environ.get("VANNA_API_KEY"))
        vn.set_model("thelook")


def setup_session_state(con:str):
    st.session_state["my_question"] = None