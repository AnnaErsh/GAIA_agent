from duckduckgo_search import DDGS
from llama_index.tools import FunctionTool


def web_search(query: str, num_results: int = 3) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=num_results)
        if not results:
            return "No results found."
        return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])


web_search_tool = FunctionTool.from_defaults(
    fn=web_search,
    name="web_search",
    description="Search the web for recent or factual information.",
)
