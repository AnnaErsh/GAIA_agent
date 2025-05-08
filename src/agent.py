import asyncio
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from src.tools import web_search_tool
from src.utils import hf_oauth


class MyAgent:
    def __init__(self):
        system_prompt = """
        You are an expert AI agent participating in the GAIA benchmark.
        Your goal is to provide accurate, helpful, and well-reasoned answers to a wide variety of academic and general knowledge questions.
        Use the available tools when needed, especially for factual lookups.
        Avoid guessing. If uncertain, say so clearly. Provide only the answer, no explanations.
        """

        llm = HuggingFaceInferenceAPI(
            model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
            api_key=hf_oauth,
        )  # Or switch to your GPT-4 line if needed
        self.tools = self.load_tools()

        self.agent = ReActAgent(
            name="web_browsing_agent",
            tools=self.tools,
            llm=llm,
            system_prompt=system_prompt,
        )

    def load_tools(self):
        return [web_search_tool]

    async def __call__(self, question: str) -> str:
        print(f"Agent is running with question: {question}")
        return await self.agent.run(user_msg=question)
