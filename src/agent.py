import asyncio
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from src.tools import (
    web_search_tools,
    wikipedia_tools,
    speech_to_text_tool,
    video_to_text_tool,
)
from src.utils import Logger

LOGGER = Logger.get_logger()


class MyAgent:
    def __init__(self):
        system_prompt = """
        You are an expert AI agent participating in the GAIA benchmark.
        Your goal is to provide accurate, helpful, and well-reasoned answers to a wide variety of academic and general knowledge questions.
        Use the available tools when needed, especially for factual lookups.
        Avoid guessing. If uncertain, say so clearly. Provide only the answer, no explanations. Example:
        Question: What is the capital of France?
        Answer: Paris
        Wrong Answer: The capital of France is Paris.
        """

        llm = HuggingFaceInferenceAPI(
            model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        )  # Or switch to your GPT-4 line if needed
        self.tools = self.load_tools()

        self.agent = ReActAgent(
            name="GAIA_agent",
            tools=self.tools,
            llm=llm,
            system_prompt=system_prompt,
        )

    def load_tools(self):
        base_tools = (
            web_search_tools
            + wikipedia_tools
            + [speech_to_text_tool, video_to_text_tool]
        )
        return base_tools

    async def __call__(self, question: str) -> str:
        # LOGGER.info(f"Agent is running with question: {question}")
        return await self.agent.run(user_msg=question)
