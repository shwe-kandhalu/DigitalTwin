# VAPI Audio Analysis Client

This Python application provides a simple interface to interact with the VAPI API for audio analysis.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your API key:
```
VAPI_API_KEY=your_api_key_here
```

## Usage

The application provides a simple interface to analyze audio files. Here's how to use it:

```python
from vapi_client import VAPIClient

# Initialize the client
client = VAPIClient()

# Analyze an audio file
analysis = client.analyze_audio("path/to/your/audio/file.wav")

# Save the results
if analysis:
    client.save_analysis_results(analysis, "audio_analysis.json")
```

## Features

- Analyze audio files using the VAPI API
- Save analysis results to JSON files
- Error handling and file management

## Requirements

- Python 3.7+
- Required packages (see requirements.txt):
  - requests
  - python-dotenv
