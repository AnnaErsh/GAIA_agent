from duckduckgo_search import DDGS
from llama_index.core.tools import FunctionTool


def web_search(query: str, num_results: int = 3) -> str:
    try:
        with DDGS() as ddgs:
            print(f"Web search tool is being invoked with query: {query}")
            results = list(ddgs.text(query, max_results=num_results))
            if not results:
                return "No results found."
            return "\n\n".join(
                [f"{r['title']}: {r['body']}\n{r['href']}" for r in results]
            )
    except Exception as e:
        return f"Error during search: {e}"


web_search_tool = FunctionTool.from_defaults(
    fn=web_search,
    name="web_search",
    description="Search the web for recent or factual information.",
)
