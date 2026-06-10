import os
import requests
from bs4 import BeautifulSoup
from langchain_tavily import TavilySearch  # <--- UPDATED IMPORT
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Custom LangChain Tool for Deep Scraping
@tool
def scrape_url(url: str) -> str:
    """Scrape detailed text content from a specific URL. 
    Use this tool AFTER finding a relevant URL from the search tool to get deeper context."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        elements = soup.find_all(['h1', 'h2', 'h3', 'p'])
        text = '\n'.join([elem.get_text(strip=True) for elem in elements])
        return text[:3000] 
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def get_research_tools():
    """Initialize and return the tools. Called after API keys are set in Streamlit."""
    # <--- UPDATED CLASS NAME (TavilySearch instead of TavilySearchResults)
    tavily_search = TavilySearch(
        max_results=3, 
        search_depth="advanced",
        api_key=os.getenv("TAVILY_API_KEY")
    )
    return [tavily_search, scrape_url]