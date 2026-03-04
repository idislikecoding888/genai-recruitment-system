from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool("internet_search")
def internet_search(query: str):
    """Useful for searching the internet about market trends, salary benchmarks, and talent demand. 
    Input should be a search query string."""
    try:
        if not query:
            return "No search query provided."
        search = DuckDuckGoSearchRun()
        return search.run(query)
    except Exception as e:
        return f"Error performing search: {str(e)}"

def get_search_tool():
    return internet_search
