# utils/summarizer.py
from transformers import pipeline

# Load summarization model (once)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    """
    Summarizes given text using a pre-trained model.
    Returns a clean, short summary even if input is short.
    """
    try:
        if not text or not text.strip():
            return "No text available to summarize."

        # Adjust summary length depending on input size
        max_len = min(100, max(30, len(text.split()) // 2))
        min_len = min(20, max(5, len(text.split()) // 4))

        print(f"Summarizing text (min_len={min_len}, max_len={max_len})...")
        summary_list = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        summary = summary_list[0]['summary_text']

        return summary.strip()

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error during summarization."
