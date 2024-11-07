from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ-KEY")
model = ChatGroq(model= "Gemma2-9b-it" ,  groq_api_key = groq_api_key)

# Creating our prompt template 
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template ),
    ('user', '{text}')
]
)

# Getting the output format

parser = StrOutputParser()

# Combine all steps in a chain
chain = prompt_template|model|parser

# set up api
app = FastAPI(title="Lamgchain-serve",
              version = "1.0",
              description = "A simple API server using Langchain runnable interface")

# Adding the chain route
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1" , port = 8000)