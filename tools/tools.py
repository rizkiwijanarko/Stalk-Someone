from langchain_community.tools.tavily_search import TavilySearchResults

def search_profile_url_tavily(name: str):
    """
    Search for linkedin or Twitter profile page using Tavily.
    """

    search = TavilySearchResults()
    results = search.run(f"{name} linkedin")

    return results[0]["url"]