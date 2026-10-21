import ast, operator as op
from rag import search

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
       ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg}

def _eval(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return n.value
    if isinstance(n, ast.BinOp):
        return OPS[type(n.op)](_eval(n.left), _eval(n.right))
    if isinstance(n, ast.UnaryOp):
        return OPS[type(n.op)](_eval(n.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    return str(_eval(ast.parse(expression, mode="eval").body))

def search_documents(query: str) -> str:
    return search(query)

TOOL_FUNCS = {"calculator": calculator, "search_documents": search_documents}

TOOLS = [
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate a math expression like '12*(3+4)'.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "search_documents",
        "description": "Search the company documents for relevant information.",
        "parameters": {"type": "object",
                       "properties": {"query": {"type": "string"}},
                       "required": ["query"]}}},
]