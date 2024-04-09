import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import mcq_generator_chain

with open('C:\Users\saura\Downloads\Telegram Desktop\mcqgen-main\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.title("Quiz Creator")
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload the quiz material")
    mcq_count = st.number_input("Number of questions you want",min_value= 3,max_value =50)
    subject = st.text_input("Quiz subject",max_chars=20)
    tone = st.text_input("Quiz difficulty",max_chars=20,placeholder="Simple")
    button=st.form_submit_button("Generate Quiz")
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating...")
            try:
                text=read_file(uploaded_file)
                response = mcq_generator_chain({
                    "text":text,
                    "number": mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(RESPONSE_JSON)
                })
            
            except Exception as e:
                st.error("Error")

