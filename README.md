# AI Microservice

A lightweight gRPC microservice that exposes AI inference operations backed by the Groq API.

## Project structure

- `server/` - gRPC server implementation
- `client/` - client script that calls the local gRPC server
- `generated/` - generated protobuf Python stubs
- `protos/` - protobuf schema definitions
- `server/ai_client.py` - real Groq API integration
- `README.md` - project documentation

## Features

- Unary sentiment analysis
- Server streaming generation
- Client streaming summarization
- Bidirectional streaming chat

## Requirements

- Python 3.11+
- `grpcio`
- `grpcio-tools`
- `groq` Python SDK
- A Groq API key available in the environment

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```powershell
python -m pip install grpcio grpcio-tools groq
```

3. Set your Groq API key:

```powershell
$env:GROQ_API_KEY = "your-api-key"
```

## Running the server

Start the gRPC server from the project root:

```powershell
uv run server/server.py
```

The service listens on port `50051`.

## Running the client

In a second terminal, run:

```powershell
uv run client/client.py
```

The client will call the local gRPC server and demonstrate:

- sentiment analysis
- streaming generation
- batch summarization
- bidirectional chat

## Notes

- The server uses `server/ai_client.py` to call Groq's `llama3-8b-8192` model.
- This is a real API integration, not a mock.
- If you see errors, confirm the Groq key is set and the server is running before executing the client.

## Protobuf

The service contract is defined in `protos/ai_inference.proto`.
The generated Python modules are stored in `generated/`.

## Troubleshooting

- `ModuleNotFoundError: No module named 'generated'` — run from the project root or ensure the root is added to `sys.path`.
- `Connection refused` — verify the server is running on `localhost:50051`.
- `Groq API` errors — confirm `GROQ_API_KEY` is configured and valid.
