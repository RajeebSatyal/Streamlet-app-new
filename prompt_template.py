from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableParallel

email_prompt_template = PromptTemplate(
    input_variables=["name", "topic", "tone"],
    template="""
Write an email to {name} about {topic}.
The tone should be {tone}.
"""
)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

chain = email_prompt_template | model


draft_email_prompt=PromptTemplate(
    input_variables=["email_topic", "receipient", "name"],
    template="""
    You are a helpful email assistant. Your task is to write a draft email for the following email.
    Topic: {email_topic}
    Receipient: {receipient}
    Name: {name}
    
    Give me the draft email in the following JSON format:
    {{
        "draft_email": "This is the draft email"
    }}
    """
)


draft_email_chain=draft_email_prompt|model
grammer_chain_prompt=PromptTemplate(
    input_variables=["draft_email"],
    template="""
You are a helpful email assistant. Check and validate the grammar of the following email.
Email: {draft_email}
Also humanize the email to make it more natural and readable.
Give me the response in the following JSON format:
{{
    "grammar_check_complete": "Grammar check result",
    "final_email": "This is the humanized email"
}}
"""
)

grammar_chain=grammer_chain_prompt|model|JsonOutputParser()
Combined_chain=(draft_email_chain|grammar_chain)


subject_line_prompt=PromptTemplate(
    input_variables=["question"],
    template="""
    You are a helpful email assistant. Your task is to write a subject line for the following email.
    question: {question}

    Give me the subject line in the following JSON format:
    {{
        "subject_line": "This is the subject line"
    }}
    """
)
subject_line_chain=subject_line_prompt|model|JsonOutputParser()

parallel_chain=RunnableParallel({"combined_chain":Combined_chain,
         "subject_line": subject_line_chain
         }
        )
