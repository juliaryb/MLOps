import json
import polars as pl
from dotenv import load_dotenv
from google import genai

load_dotenv()


APISTOX_CSV_URL = (
    "https://raw.githubusercontent.com/j-adamczyk/ApisTox_dataset/master/outputs/dataset_final.csv"
)

TLC_YELLOW_PARQUET_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
)


client = genai.Client()
MODEL_NAME = "gemini-3-flash-preview"


def read_remote_csv(url: str, n_rows: int = 5) -> str:
    df = pl.read_csv(url).head(n_rows)
    return df.write_csv()


def read_remote_parquet(url: str, n_rows: int = 5) -> str:
    df = pl.read_parquet(url).head(n_rows)
    return df.write_csv()


TOOLS = {
    "read_remote_csv": read_remote_csv,
    "read_remote_parquet": read_remote_parquet,
}


TOOL_INSTRUCTIONS = """
You have access to the following tools:

1. read_remote_csv(url: string, n_rows: int)
2. read_remote_parquet(url: string, n_rows: int)

If you need to use a tool, respond ONLY with a valid JSON object in this format:

{
  "tool_name": "<tool name>",
  "arguments": {
    "url": "<url>",
    "n_rows": 5
  }
}

Do not include any explanation, markdown, or extra text.
If no tool is needed, respond with normal text.
"""

# LLM interaction loop
def ask_llm(prompt: str) -> str:
    full_prompt = f"{TOOL_INSTRUCTIONS}\n\nUser question:\n{prompt}"

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
    )

    return response.text.strip()


def handle_tool_call(response_text: str) -> str | None:
    """
    Try to parse a tool call from the LLM response.
    Return tool result if a tool was called, otherwise None.
    """
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        return None

    tool_name = data.get("tool_name")
    arguments = data.get("arguments", {})

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool_fn = TOOLS[tool_name]
    return tool_fn(**arguments)


def run_conversation(user_prompt: str) -> str:
    # first LLM call
    response = ask_llm(user_prompt)

    print("\n--- LLM RESPONSE (step 1) ---")
    print(response)


    # check if the model requested a tool
    tool_result = handle_tool_call(response)
    print("\n--- TOOL OUTPUT ---")
    print(tool_result)


    if tool_result is None:
        # no tool needed
        return response

    # tool was called - send result back to LLM
    followup_prompt = f"""
The original user question was:

{user_prompt}

The tool returned the following data (this is ONLY a small sample, not the full dataset):

{tool_result}

Now answer the original question in natural language.
"""

    final_response = client.models.generate_content(
        model=MODEL_NAME,
        contents=followup_prompt,
    )

    return final_response.text.strip()


if __name__ == "__main__":
    question = (
        f"The dataset is available at {TLC_YELLOW_PARQUET_URL}. "
        "Can you answer these questions: \n 1. What does the dataset seem to represent? \n 2. What columns does it contain and of what type? \n 3. What analysis could I run on the full dataset?"
    )

    answer = run_conversation(question)

    print("USER PROMPT:\n")
    print(question)

    print("FINAL ANSWER:\n")
    print(answer)

client.close()