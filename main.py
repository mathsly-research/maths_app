from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from latex2sympy2 import latex2sympy
import sympy as sp

app = FastAPI()

# CORS per frontend JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puoi restringere a domini specifici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MathRequest(BaseModel):
    latex: str

@app.post("/solve")
def solve_math(req: MathRequest):
    try:
        expr = latex2sympy(req.latex)
        if isinstance(expr, sp.Equality):
            sol = sp.solve(expr, dict=True)
        elif isinstance(expr, sp.Basic):
            sol = {
                "derivative": sp.diff(expr),
                "integral": sp.integrate(expr),
                "simplified": sp.simplify(expr),
                "expanded": sp.expand(expr),
                "factorized": sp.factor(expr)
            }
        else:
            sol = str(expr)
        return {"success": True, "result": str(sol)}
    except Exception as e:
        return {"success": False, "error": str(e)}
