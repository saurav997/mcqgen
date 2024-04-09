import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.llms import HuggingFaceHub

KEY=os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceHub(
    repo_id="google/flan-t5-xxl",
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 30,
        "temperature": 0.1,
        "repetition_penalty": 1.03,
    },
)

load_dotenv()

template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""
quiz_generation_prompt = PromptTemplate(template=template,input_variables={"text","number","subject","tone","respone_json"})
quiz_generator_chain = LLMChain(llm=llm,prompts = quiz_generation_prompt,output_key = "quiz",verbose = True)

template2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_review_prompt = PromptTemplate(template = template2,input_variables={"quiz"})
quiz_review_chain = LLMChain(llm =llm,prompt = quiz_review_prompt,verbose =True,output_key ={"review"})
mcq_generator_chain = SequentialChain(chains = [quiz_generation_chain,quiz_review_chain],input_variables = ["text","number","subject","tone","respone_json"],output_variables=["quiz","review"],verbose=True)

response = mcq_generator_chain(
    [
        "text":text,
        "number":number,
        "subject":subject,
        "tone":tone,
        "respone_json":json.dumps(RESPONSE_JSON)
    ]
    )
