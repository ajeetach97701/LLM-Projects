# retrieve three prime umbers from a Tool
# multiply these together
from langchain.agents import AgentType,initialize_agent
from langchain.chains import LLMMathChain
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from langchain.agents import AgentType,Tool, initialize_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain import hub
from langchain.memory import ConversationBufferWindowMemory
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyD8XGPR2OwqCw5gw526--5KB1K--d-DE4I"
llm=ChatGoogleGenerativeAI(temperature=0,model="gemini-1.0-pro", convert_system_message_to_human=True)
llm_math_chain=LLMMathChain.from_llm(llm)
memory = ConversationBufferWindowMemory(memory_key="chat_history",k=2,return_messages=True)
# class CalculatorInput(BaseModel):
#     question: str = Field()
# class PrimeInput(BaseModel):
#     n: int = Field()
def is_prime(n: int) -> bool:
    print(type(n),":::::::::::::::::")
    n=int(n)
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
# def get_prime(n: int, primes: dict = primes) -> str:
#     return str(primes.get(int(n)))
# async def aget_prime(n: int, primes: dict = primes) -> str:
#     return str(primes.get(int(n)))
tools = [
    Tool(
        name="GetPrime",
        func=is_prime,
        description="A tool that returns the `n`th prime number",
        # args_schema=PrimeInput,
        # coroutine=aget_prime,
    ),
    # Tool.from_function(
    #     func=llm_math_chain.run,
    #     name="Calculator",
    #     description="Useful for when you need to compute mathematical expressions",
    #     args_schema=CalculatorInput,
    #     coroutine=llm_math_chain.arun,
    # ),
]
# prompt = hub.pull("hwchase17/react-chat")
# prompt = prompt.partial(
#     tools = render_text_description(tools),
#     tool_names=", ".join([t.name for t in tools])
# )
# llm_with_stop = llm.bind(stop=["\nObservation"])
# agent = (
#     {
#         "input": lambda x:x["input"],
#         "agent_scratchpad":lambda x: format_log_to_str(x["intermediate_steps"]),
#         "chat_history": lambda x: x["chat_history"],
#     }
#     | prompt
#     | llm_with_stop
#     | ReActSingleInputOutputParser()
# )
agent = initialize_agent(tools=tools,
                         llm=llm,
                         agent='chat-conversational-react-description',
                         verbose=True,
                         max_iterations=3,
                         early_stopping_method = 'generate',
                         memory = memory,
                         handle_parsing_errors=True
                         )
print(agent("Is 48 a prime number"))
