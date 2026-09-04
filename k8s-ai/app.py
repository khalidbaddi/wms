from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = FastAPI()

# templates folder
templates = Jinja2Templates(directory="templates")

# Kubernetes troubleshooting data
docs = [
    "CrashLoopBackOff pod restarting issue",
    "ImagePullBackOff image pull failed",
    "Pending pod insufficient resources",
    "Service not reachable selector issue"
]

# Load model
print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert docs to vectors
embeddings = model.encode(docs)

# Create FAISS index
index = faiss.IndexFlatL2(384)
index.add(np.array(embeddings))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"response": ""}
    )


@app.post("/ask", response_class=HTMLResponse)
async def ask(
    request: Request,
    query: str = Form(...)
):

    query_embedding = model.encode([query])

    D, I = index.search(
        np.array(query_embedding),
        k=1
    )

    best_match = docs[I[0][0]]

    response = ""

    if "CrashLoopBackOff" in best_match:
        response = """
CrashLoopBackOff detected

Fix:
kubectl logs <pod-name>
kubectl describe pod <pod-name>

Reason:
- App crash
- Wrong ENV variable
- DB connection failed
"""

    elif "ImagePullBackOff" in best_match:
        response = """
ImagePullBackOff detected

Fix:
kubectl describe pod <pod-name>

Check:
- Image name
- Docker registry access
- Image tag
"""

    elif "Pending" in best_match:
        response = """
Pending pod issue

Fix:
kubectl get nodes

Reason:
- CPU/Memory insufficient
"""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "response": response
        }
    )