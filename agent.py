from llama_index.agent import ReActAgent, OpenAIAgent, FnAgent
from llama_index.llms import OpenAI
from llama_index.tools import ToolMetadata, FunctionTool
from llama_index.indices.vector_store import VectorStoreIndex

from tools import web_search_tool


class MyAgent:
    def __init__(self):
        system_prompt = """
        You are an expert AI agent participating in the GAIA benchmark.
        Your goal is to provide accurate, helpful, and well-reasoned answers to a wide variety of academic and general knowledge questions.
        Use the available tools when needed, especially for factual lookups.
        Avoid guessing. If uncertain, say so clearly.
        """

        llm = OpenAI(model="gpt-4", temperature=0.3, system_prompt=system_prompt)
        self.tools = self.load_tools()

        # Choose one of the following:
        # self.agent = ReActAgent.from_tools(self.tools, llm=llm)
        # self.agent = OpenAIAgent.from_tools(self.tools, llm=llm)
        self.agent = FnAgent.from_tools(self.tools, llm=llm)  # Start simple

    def load_tools(self):
        # You can define custom tools like search, math, or reasoning steps
        return [web_search_tool]

    def __call__(self, question: str) -> str:
        return self.agent.query(question).response
