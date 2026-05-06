from groq import Groq

client = Groq()  # API key will be read from environment


# 🔹 Task 2: Sentiment
def analyze_sentiment(text: str):
    prompt = f"""
Classify the sentiment of this text as POSITIVE, NEGATIVE, or NEUTRAL.
Also give a confidence score between 0 and 1.

Text: "{text}"

Respond in this format:
LABEL: <label>
CONFIDENCE: <number>
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content

    label = "NEUTRAL"
    confidence = 0.5

    try:
        for line in content.splitlines():
            if "LABEL:" in line:
                label = line.split("LABEL:")[1].strip()
            if "CONFIDENCE:" in line:
                confidence = float(line.split("CONFIDENCE:")[1].strip())
    except Exception:
        pass

    return label, confidence


# 🔹 Task 3: Streaming generation
def generate_stream(prompt: str):
    stream = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# 🔹 Task 4: Summarization
def summarize(text: str):
    prompt = f"Summarize the following text:\n\n{text}"

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


# 🔹 Task 5: Chat (single turn, history handled outside)
def chat(messages):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        stream=True,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
