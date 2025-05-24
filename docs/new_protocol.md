# HTTP Protocol for Faster-Whisper

This document describes the new HTTP API used to interact with the Faster-Whisper service. Wyoming support has been removed due to latency issues.

## Endpoints

### `POST /speech`
Generate spoken audio from input text. This endpoint is not yet implemented and currently returns `501 Not Implemented`.

### `POST /transcriptions`
Upload a **.wav** file and receive a transcription in the source language. The request must use `multipart/form-data` with a single field named `file` containing the audio. Optional parameters such as `model` and `language` can be passed as query strings.

### `POST /translations`
Upload a **.wav** file and receive an English translation. The request format matches the transcription endpoint.

### `GET /health`
Simple health check that returns:

```json
{"status": "ok"}
```

## Notes

* Only `.wav` files are accepted. Conversion from other formats should be handled by a separate service.
* Streaming responses are not supported.
* The service listens on a single HTTP port specified by the `PORT` environment variable (default `8000`).
