import asyncio
import requests

from src.agent import MyAgent
from src.utils import Logger

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"

api_url = DEFAULT_API_URL
questions_url = f"{api_url}/questions"
submit_url = f"{api_url}/submit"

# Initialize the agent
agent = MyAgent()

LOGGER = Logger.get_logger()


# Define an asynchronous function to handle the requests and agent operations
async def process_questions():
    response = requests.get(questions_url, timeout=15)
    response.raise_for_status()
    questions_data = response.json()
    for question in questions_data:
        print(question.get("question"))
    LOGGER.info(f"Running agent on {len(questions_data)} questions...")
    answers_payload = []
    results_log = []

    # For each question, run the agent asynchronously
    iter = 0
    limit = 20
    indices_to_run = [2, 3, 4, 5]
    for idx in indices_to_run:
        item = questions_data[idx]
        iter += 1
        if iter > limit:
            break
        task_id = item.get("task_id")
        question_text = item.get("question")
        if not task_id or question_text is None:
            LOGGER.warning(f"Skipping item with missing task_id or question: {item}")
            continue
        try:
            # Use await to call the agent asynchronously
            # submitted_answer = await agent(question_text)
            LOGGER.info("=" * 100)
            LOGGER.info("Question: %s", question_text)
            # submitted_answer = await agent.run(user_msg=question_text)
            result = await agent(question_text)

            submitted_answer = str(result)

            LOGGER.info("Answer: %s", submitted_answer)
            answers_payload.append(
                {"task_id": task_id, "submitted_answer": submitted_answer}
            )
            results_log.append(
                {
                    "Task ID": task_id,
                    "Question": question_text,
                    "Submitted Answer": submitted_answer,
                }
            )
        except Exception as e:
            LOGGER.error(f"Error running agent on task {task_id}: {e}")
            results_log.append(
                {
                    "Task ID": task_id,
                    "Question": question_text,
                    "Submitted Answer": f"AGENT ERROR: {e}",
                }
            )

    # Optionally, submit the answers here
    response = requests.post(submit_url, json=answers_payload)


# Run the event loop
asyncio.run(process_questions())
