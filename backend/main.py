from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# In production would need to configure CORSMiddleware differently, obviously

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the summarization pipeline
# Using a smaller model for demonstration purposes.
# For better quality, consider 'facebook/bart-large-cnn' or 'sshleifer/distilbart-cnn-12-6'
summarizer = pipeline("summarization", model="t5-small")

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Read PDF content
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF or PDF is empty.")

        # Summarize the extracted text
        # The 'max_length' and 'min_length' can be adjusted based on desired summary length
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

        return JSONResponse(content={"summary": summary[0]["summary_text"]})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "PDF Summarizer API. Go to /docs for API documentation."}
