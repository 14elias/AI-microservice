import grpc
import time
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import generated.ai_inference_pb2 as pb2
import generated.ai_inference_pb2_grpc as pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.AIInferenceStub(channel)

    # 🔹 Task 2: Unary RPC
    print("\n--- Sentiment Analysis ---")
    res = stub.AnalyzeSentiment(
        pb2.SentimentRequest(text="This product is amazing!")
    )
    print(f"Label: {res.label}, Confidence: {res.confidence}")

    # 🔹 Task 3: Server Streaming (REAL streaming now)
    print("\n--- Streaming LLM Response ---")

    stream = stub.GenerateStream(
        pb2.PromptRequest(prompt="Explain what AI is in simple terms.")
    )

    for token in stream:
        print(token.token, end="", flush=True)  # no space, real token flow
    print("\n")

    # 🔹 Task 4: Client Streaming
    print("\n--- Batch Summarization ---")

    def generate_chunks():
        text_parts = [
            "Artificial intelligence is transforming industries.",
            "It enables machines to learn from data.",
            "Many companies are adopting AI rapidly.",
            "However, it also raises ethical concerns."
        ]

        for part in text_parts:
            print(f"Sending chunk: {part}")
            time.sleep(0.5)
            yield pb2.ChunkRequest(chunk=part)

    summary = stub.SummarizeStream(generate_chunks())
    print("\nSummary:")
    print(summary.summary)

    # 🔹 Task 5: Bidirectional Streaming (REAL CHAT)
    print("\n--- Live Chat ---")

    def chat_messages():
        user_inputs = [
            "Hello!",
            "What is machine learning?",
            "Give me a short example."
        ]

        for msg in user_inputs:
            print(f"\nYou: {msg}")
            yield pb2.ChatMessage(role="user", content=msg)
            time.sleep(1)  # simulate thinking time

    responses = stub.ChatStream(chat_messages())

    print("\nAI:", end=" ", flush=True)

    for res in responses:
        print(res.content, end="", flush=True)


if __name__ == "__main__":
    run()