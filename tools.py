from langchain.tools import tool
from tavily import TavilyClient
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

# Setup API Clients
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Initialize Firecrawl 
firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


@tool
def search_web(query: str) -> list:
    """
    Search the web for the given query and return structured results.
    """
    try:
        results = tavily.search(query=query, max_results=5)
        structured_results = []

        for r in results.get("results", []):
            structured_results.append({
                "title": r.get("title", "No Title"),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:300]
            })

        return structured_results

    except Exception as e:
        return [{"error": str(e)}]


@tool
def scrape_web(url: str) -> str:
    """
    Scrape the content of the given URL and return clean Markdown text using Firecrawl.
    """
    try:
        # FIX: Using the modern SDK syntax payload for formats
        # If your version uses .scrape_url, it expects the parameters inside a flat dictionary or explicit kwargs
        scraped_data = firecrawl_app.scrape_url(
            url, 
            params={
                'formats': ['markdown']
            }
        )
        
        # Check if the result is directly returning a dictionary containing the markdown
        if scraped_data and 'markdown' in scraped_data:
            return scraped_data['markdown'][:6000]
            
        # Alternate fallback layout check for newer SDK nested response objects
        if hasattr(scraped_data, 'markdown') and scraped_data.markdown:
            return scraped_data.markdown[:6000]
            
        return f"Warning: Firecrawl successfully connected but could not extract markdown content from {url}."

    except TypeError:
        # Fallback block if your installed version uses the direct scrape method with flat arguments
        try:
            scraped_data = firecrawl_app.scrape(url=url, formats=['markdown'])
            if isinstance(scraped_data, dict) and 'markdown' in scraped_data:
                return scraped_data['markdown'][:6000]
            if hasattr(scraped_data, 'markdown') and scraped_data.markdown:
                return scraped_data.markdown[:6000]
        except Exception as inner_e:
            return f"Error using Firecrawl fallback methods: {str(inner_e)}"

    except Exception as e:
        return f"Error scraping {url} with Firecrawl: {str(e)}"