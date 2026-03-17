# ADK Streaming — Real-Time Voice + Analysis Agent

A real-time voice and text conversation app powered by **Google Agent Development Kit (ADK)** and **Gemini**. It streams audio and text through a FastAPI WebSocket server, orchestrates two specialized agents, and delivers detailed post-turn analysis to the browser.

---

## Architecture
 
![adk_streaming_architecture](https://github.com/user-attachments/assets/66ffe235-7e8f-4571-ac66-bec598e38f7a)

### Agent orchestration

The app uses a **manual sequential** pattern instead of `SequentialAgent` because:

- The **Live Agent** requires `runner.run_live()` for bidirectional audio streaming — incompatible with `SequentialAgent`.
- The **Detail Agent** uses the standard `runner.run()` for synchronous text generation.
- Both agents share conversation context via **session state** (transcripts written after each turn).

---

## Key Components

| File / Module | Role |
|---|---|
| `main.py` | FastAPI app, WebSocket endpoint, agent orchestration |
| `google_search_agent/agent.py` | Live agent — handles real-time audio/text conversation |
| `detail_agent/agent.py` | Detail agent — post-turn analysis of transcripts |
| `static/index.html` | Browser client (audio capture + WebSocket messaging) |
| `.env` | API credentials (see Setup) |

---

## Message Flow

### Audio mode (`is_audio=true`)

1. Browser captures microphone audio (PCM) → encodes as base64 → sends over WebSocket.
2. **Live Agent** transcribes user speech (`input_audio_transcription`) and speaks back (`AUDIO` modality + `output_audio_transcription`).
3. Partial transcripts stream to the browser in real time with `"is_input_transcript": true` / `"is_output_transcript": true` flags.
4. On `turn_complete`, full transcripts are written to a new **Detail Agent session state**.
5. **Detail Agent** reads both transcripts and produces a structured analysis, streamed back with `"is_detailed_analysis": true`.

### Text mode (`is_audio=false`)

Steps 1–3 use plain `text/plain` messages; step 4–5 are skipped (analysis only runs in audio mode).

---

## WebSocket Message Schema

### Client → Server

```json
{ "mime_type": "text/plain", "data": "Hello!" }
{ "mime_type": "audio/pcm",  "data": "<base64-encoded PCM>" }
```

### Server → Client

```json
{ "mime_type": "text/plain", "data": "...", "partial": true,  "is_input_transcript": true }
{ "mime_type": "text/plain", "data": "...", "partial": false, "is_output_transcript": true }
{ "mime_type": "audio/pcm",  "data": "<base64 PCM>" }
{ "mime_type": "application/json", "data": "...", "partial": false, "is_detailed_analysis": true }
{ "turn_complete": true, "interrupted": false }
```

---

## Setup

### 1. Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`
- A Google AI / Gemini API key

### 2. Install dependencies

```bash
uv sync
# or: pip install fastapi google-adk google-generativeai python-dotenv python-multipart uvicorn
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set:
# GOOGLE_API_KEY=your_key_here
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser.

---

## Project Structure

```
.
├── main.py                    # FastAPI app + WebSocket + agent orchestration
├── google_search_agent/
│   └── agent.py               # Live agent definition
├── detail_agent/
│   └── agent.py               # Detail analysis agent definition
├── static/
│   └── index.html             # Browser client
├── pyproject.toml
├── uv.lock
└── .env                       # API key (git-ignored)
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `google-adk` | Agent Development Kit — runners, sessions, live streaming |
| `google-generativeai` | Gemini API client |
| `fastapi` | WebSocket + HTTP server |
| `uvicorn` | ASGI server |
| `python-dotenv` | Environment variable loading |
| `python-multipart` | Multipart form support |

---

## Configuration Notes

- `APP_NAME` is set to `"ADK Streaming example"` — used as the session namespace.
- Audio mode uses `AUDIO` response modality with both `input_audio_transcription` and `output_audio_transcription` enabled.
- Text mode uses `TEXT` modality with no transcription config.
- The Detail Agent receives a **fresh `InMemoryRunner` and session** per turn to avoid state pollution.
- Logging for `google.genai` and `google.adk` is set to `ERROR` to suppress verbose streaming warnings.

---

## License

MIT
