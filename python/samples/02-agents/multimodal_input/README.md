# Multimodal Input Examples

This folder contains examples demonstrating how to send multimodal content (images, audio, PDF files) to AI agents using the Agent Framework.

## Examples

### OpenAI clients

- **File**: `openai_chat_multimodal.py`
- **Description**: Shows image and PDF input with `OpenAIChatClient`, and audio input with `OpenAIChatCompletionClient`
- **Supported formats**: PNG/JPEG images, WAV/MP3 audio, PDF documents

### Foundry image sample

- **File**: `azure_chat_multimodal.py`
- **Description**: Shows image input with `FoundryChatClient`
- **Supported formats**: PNG/JPEG images

### Foundry image and PDF sample

- **File**: `azure_responses_multimodal.py`
- **Description**: Shows image and PDF input with `FoundryChatClient`
- **Supported formats**: PNG/JPEG images, PDF documents

## Environment Variables

Set the following environment variables before running the examples:

**For OpenAI:**
- `OPENAI_API_KEY`: Your OpenAI API key

**For both Foundry samples (`azure_chat_multimodal.py` and `azure_responses_multimodal.py`):**

- `FOUNDRY_PROJECT_ENDPOINT`: Your Microsoft Foundry project endpoint, such as `https://your-account.services.ai.azure.com/api/projects/your-project`
- `FOUNDRY_MODEL`: The model deployment name in your Foundry project

**Note:** You can also provide configuration directly in code instead of using environment variables:
```python
# Example: Pass the Foundry project endpoint directly
client = FoundryChatClient(
    credential=AzureCliCredential(),
    project_endpoint="https://your-account.services.ai.azure.com/api/projects/your-project",
    model="your-deployment-name",
)
```

## Authentication

Both Foundry samples use `AzureCliCredential` for authentication. Run `az login` in your terminal before running them, or pass another supported Azure credential through the `credential` parameter.

## Running the Examples

```bash
# Run OpenAI example
python openai_chat_multimodal.py

# Run Foundry image example (requires az login)
python azure_chat_multimodal.py

# Run Foundry image and PDF example (requires az login)
python azure_responses_multimodal.py
```

## Using Your Own Files

The examples include small embedded test files for demonstration. To use your own files:

### Method 1: Data URIs (recommended)

```python
import base64

# Load and encode your file
with open("path/to/your/image.jpg", "rb") as f:
    image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    image_uri = f"data:image/jpeg;base64,{image_base64}"

# Use in DataContent
Content.from_uri(
    uri=image_uri,
    media_type="image/jpeg"
)
```

### Method 2: Raw bytes

```python
# Load raw bytes
with open("path/to/your/image.jpg", "rb") as f:
    image_bytes = f.read()

# Use in DataContent
Content.from_data(
    data=image_bytes,
    media_type="image/jpeg"
)
```

## Supported File Types

| Type      | Formats              | Notes                          |
| --------- | -------------------- | ------------------------------ |
| Images    | PNG, JPEG, GIF, WebP | Most common image formats      |
| Audio     | WAV, MP3             | For transcription and analysis |
| Documents | PDF                  | Text extraction and analysis   |

## Clients Used by the Samples

- **OpenAI example**: Uses `OpenAIChatClient` for images and PDFs, and `OpenAIChatCompletionClient` for audio.
- **Foundry image example**: Uses `FoundryChatClient` for images.
- **Foundry image and PDF example**: Uses `FoundryChatClient` for images and PDFs.

Choose the sample and deployed model that match your input type.
