import os
from langchain_mistralai import ChatMistralAI
from langgraph.prebuilt import create_react_agent
from tools import get_research_tools
from dotenv import load_dotenv

load_dotenv()

def get_research_agent():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found. Please set it in your .env file or Streamlit sidebar.")
    
    # 1. Initialize Mistral LLM
    llm = ChatMistralAI(
        model="mistral-large-latest",
        mistral_api_key=api_key,
        temperature=0.1 
    )

    # 2. Get the tools (initialized here so they catch the sidebar API keys)
    research_tools = get_research_tools()

    # 3. Create the LangGraph ReAct Agent (The modern replacement for AgentExecutor)
    agent = create_react_agent(
        model=llm, 
        tools=research_tools
    )
    
    return agent