import os, json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, TOOL_FUNCS

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
MODEL = os.getenv("MODEL")

SYSTEM = ("You are a helpful company assistant. Use search_documents for questions "
          "about company information and calculator for any math. "
          "If the documents don't contain the answer, say so. Be concise.")

def run_agent(history, user_msg):
    messages = [{"role": "system", "content": SYSTEM}] + history + \
               [{"role": "user", "content": user_msg}]
    tokens_in = tokens_out = 0
    for _ in range(5):  # the agent loop, capped at 5 rounds
        r = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0.2)
        tokens_in += r.usage.prompt_tokens
        tokens_out += r.usage.completion_tokens
        m = r.choices[0].message
        if not m.tool_calls:
            return m.content, tokens_in, tokens_out
        messages.append(m)
        for tc in m.tool_calls:
            args = json.loads(tc.function.arguments)
            try:
                result = TOOL_FUNCS[tc.function.name](**args)
            except Exception as e:
                result = f"Error: {e}"
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    return "Sorry, I couldn't finish that.", tokens_in, tokens_out