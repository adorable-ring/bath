# bath - a tiny ML inference server
A <200-line Python FastAPI service that wraps a pre-trained automatic speech recognition model and exposes a JSON HTTP API for inference.

### Usage Instructions (Linux)
To start the server from the project repository's root, run the command:
ansible-playbook ansible\site.yml -i localhost,

### Usage Instructions (Windows)
To start the server, first Docker must be installed and running. 
Find installation instructions here: https://docs.docker.com/desktop/setup/install/windows-install/

Then from the project repository's root, run the command:
docker build -t myapp:latest .
docker run -d --name myapp -p 8000:8000 --restart unless-stopped myapp:latest

Use Swagger UI to test the API endpoints. In a browser, enter localhost:8000/docs in the URL

## Endpoints
- `GET /health` – server health check  
- `GET /model-info` – describes the model  
- `POST /transcribe` – transcribes an audio file

### To use `/transcribe`
Choose an audio file such as: wav, mp3, m4a, flac. Then execute the API endpoint. 

## Testing
Testing will require pytest and httpx to be install. If using pip, run:
pip install pytest httpx
To run the test, run:
python -m pytest -v