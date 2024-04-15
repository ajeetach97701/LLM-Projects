import os, requests
import torch
from math import pi 
from PIL import Image
from typing import Union 
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent

openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(openai_api_key = openai_api_key,temperature = 0.2,model_name = 'gpt-3,5-turbo')
conversational_memory = ConversationBufferWindowMemory(memory_key='chat_history', k = 5, return_messages= True)


class CircumferenctTool(BaseTool):
    name = "Circumference Calculator"
    description = "Use this tool when you need to calculate circumference using radius of a circle"
    
    def _run(self, radius:Union[int, float]):
        return float(radius) * 2.0 * pi
    
    def _arun(self,radius:Union[int, float]):
        raise NotImplementedError("This tool does not support async")



tools = [CircumferenctTool()]


agent = initialize_agent(
    agent = 'chat-conversational-react-description',
    llm = llm, 
    tools = tools, 
    verbose = True,
    max_iterations = 3,
    early_stopping_methods ='generate',
    memory = conversational_memory
)
agent("can you calculate the circumference of a circle that has a radius of 7.81mm")
