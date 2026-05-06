import sys
from pathlib import Path

import grpc
from concurrent import futures
import time

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import generated.ai_inference_pb2 as pb2
import generated.ai_inference_pb2_grpc as pb2_grpc

from ai_client import (
    analyze_sentiment,
    generate_stream,
    summarize,
    chat,
)




class AIInferenceService(pb2_grpc.AIInferenceServicer):

    # 🔹 Task 2: Unary
    def AnalyzeSentiment(self, request, context):
        label, confidence = analyze_sentiment(request.text)

        return pb2.SentimentResponse(
            label=label,
            confidence=confidence
        )

    # 🔹 Task 3: Server Streaming
    def GenerateStream(self, request, context):
        for token in generate_stream(request.prompt):
            yield pb2.TokenResponse(token=token)

    # 🔹 Task 4: Client Streaming
    def SummarizeStream(self, request_iterator, context):
        chunks = []

        for req in request_iterator:
            chunks.append(req.chunk)

        full_text = " ".join(chunks)

        summary = summarize(full_text)

        return pb2.SummaryResponse(summary=summary)

    # 🔹 Task 5: Bidirectional Streaming
    def ChatStream(self, request_iterator, context):
        history = []

        for message in request_iterator:
            history.append({
                "role": message.role,
                "content": message.content
            })

            # stream AI response
            for token in chat(history):
                yield pb2.ChatMessage(
                    role="assistant",
                    content=token
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pb2_grpc.add_AIInferenceServicer_to_server(
        AIInferenceService(),
        server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("🚀 gRPC Server with Groq running on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()