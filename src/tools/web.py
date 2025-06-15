from duckduckgo_search import DDGS
from llama_index.core.tools import FunctionTool
from src.utils import Logger

LOGGER = Logger.get_logger()

from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.tools.wikipedia import WikipediaToolSpec

tool_spec = DuckDuckGoSearchToolSpec()
web_search_tools = tool_spec.to_tool_list()

# Instantiate the tool spec
wikipedia_tool_spec = WikipediaToolSpec()

# Get the tool(s)
wikipedia_tools = wikipedia_tool_spec.to_tool_list()


# def web_search(query: str, num_results: int = 3) -> str:
#     try:
#         with DDGS() as ddgs:
#             LOGGER.info(f"Web search tool is being invoked with query: {query}")
#             results = list(ddgs.text(query, max_results=num_results))
#             if not results:
#                 LOGGER.info("No results found.")
#                 return "No results found."
#             return "\n\n".join(
#                 [f"{r['title']}: {r['body']}\n{r['href']}" for r in results]
#             )
#     except Exception as e:
#         LOGGER.error("Error during search: %s", e)
#         return f"Error during search: {e}"


# web_search_tool = FunctionTool.from_defaults(
#     fn=web_search,
#     name="web_search",
#     description="Search the web for recent or factual information.",
# )
