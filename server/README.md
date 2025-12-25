# Flask Server for Real-Time LLM Agentic AI (Azure OpenAI)

- Run: `pip install -r requirements.txt && python app.py`
- Set env vars for Azure: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY` (see app.py for integration)
- Endpoint: `GET /stream?prompt=...` (SSE)
