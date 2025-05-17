# Bonfire

Bonfire is a modular Python toolkit for generating and augmenting payloads for text, audio, and image data. It is designed to help researchers, red teamers, and developers automate the creation of adversarial or evasive prompts for AI security testing and adversarial training. The goal of Bonfire is to provide a tool that is effective and flexible, while remaining simple to use and understand.

## Background
Bonfire's methodology is influenced by:
- [Arcanum Pi Taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy)
- [spikee](https://github.com/ReversecLabs/spikee)

## Extending Bonfire
- Add new augmentation methods by adding methods to the relevant Evasion class in `utils/`, subclassing or creating your own class.
- Add new templates or intents as `.jsonl` files in the `data/` directory.

- **Intents** are base prompts that define the "what" (e.g., leaking a system prompt, testing for bias, attacking users, etc.).

- **Templates** are strategies or techniques (e.g., logical bypasses, role play) that enhance the base prompt. Bonfire combines your base intent with the templates/strategies you specify, generating all combinations and applying augmentations.

To add a new technique, simply create a new file in the templates directory with prompts in the specified format. You may specify as many base prompts as you like, but note that this can create a large number of payloads, which may take extended amounts of time to process especially for audio and image generation.

## Features
- **Modular & Extensible:** Easily extendable classes for text, audio, and vision evasion. Add new augmentation methods or strategies with minimal code changes.
- **Text, Audio, and Vision Augmentation:** Modular classes to apply a variety of evasive and adversarial transformations. See the files under `utils/` to see the currently implemented augmentations.
- **JSONL-based Workflow:** All data and templates are handled in newline-delimited JSON (JSONL) format. This enables easy line-by-line processing outside of Bonfire using standard Unix tools or other programming languages. Each payload, template, or result is a single JSON object on its own line, making it easy to filter, transform, or analyze large datasets efficiently.
- **Custom Test Automation:** Seamlessly integrate your own Python scripts to automate sending generated payloads to your target system or perform custom evaluation. By using the `test` command, you can specify a Python script (located in the `bonfire/functions/` directory) that defines a `run_test(payloads)` function. Bonfire will generate the payloads and automatically pass them to your script for processing, enabling flexible integration with external systems, APIs, or custom validation logic.

## Dependencies
- Python 3.11+
- [openai-edge-tts](https://github.com/travisvn/openai-edge-tts) (optional, required for audio generation)
  - Set your API key in the `.env` file with the `OPENAI_EDGE_TTS_API_KEY` variable. 
- See `requirements.txt` for other Python dependencies.

## Installation
Bonfire requires Python 3.11 or newer.

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd bonfire
   ```
2. (Recommended) Create a virtual environment using your preferred tool:
   - **venv** (built-in):
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **virtualenv**:
     ```bash
     virtualenv .venv
     source .venv/bin/activate
     ```
   - **pyenv**:
     ```bash
     pyenv install 3.11.0  # if not already installed
     pyenv virtualenv 3.11.0 bonfire-env
     pyenv activate bonfire-env
     ```
3. Copy the example environment file and fill in any required values (such as API keys):
   ```bash
   cp .env.example .env
   # Then edit .env and set the values as needed
   ```
4. Install dependencies with pip:
   ```bash
   pip install -r requirements.txt
   # or, if using pyproject.toml with pip >=23.1:
   pip install .
   ```

## Usage
Bonfire is primarily used via its CLI, supporting both `generate` and `test` commands. You can generate augmented payloads for text, audio, or image data using provided templates and methods, or run a custom test script on the generated payloads.

### CLI Example
```bash
pyhton3 bonfire.py --help
```

### Command Overview
Bonfire supports two main commands:
- `generate`: Generate augmented payloads.
- `test`: Generate payloads and run a custom Python test script on them.

---

### Arguments for Both `generate` and `test`
All arguments are positional and required unless otherwise noted.

| Argument      | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `data_type`  | str    | Yes      | Type of data to augment. Must be one of: `text`, `audio`, or `image`. |
| `format`     | str    | Optional | Format for audio or image data. For audio: `wav` or `mp3`. For image: `jpeg`, `png`, or `gif`. Leave blank for default (`mp3` for audio, `png` for image). |
| `methods`    | str    | Yes      | Augmentation methods to use. Comma-separated list (e.g., `logical_bypass,role_play`) or `all` for every available method. |
| `output_dir` | str    | Yes      | Directory path to save generated payloads. Will be created if it does not exist. |

---

### `generate` Command
Generate augmented payloads and save them to disk.

**Examples:**
```bash
pyhton3 bonfire.py generate text  all ./output
python3 bonfire.py generate image png logic_bypass ./output
python3 bonfire.py generate audio mp3 basic ./output
```

---

### `test` Command
The `test` command requires **all the same arguments as `generate`**, in the same order, **plus** an additional required `test_file` argument at the end. This ensures you specify the data type, format, methods, and output directory for payload generation, and then provide the test script to execute.

| Argument      | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `data_type`  | str    | Yes      | Type of data to augment. Must be one of: `text`, `audio`, or `image`. |
| `format`     | str    | Optional | Format for audio or image data. For audio: `wav` or `mp3`. For image: `jpeg`, `png`, or `gif`. Leave blank for default (`mp3` for audio, `png` for image). |
| `methods`    | str    | Yes      | Augmentation methods to use. Comma-separated list (e.g., `logical_bypass,role_play`) or `all` for every available method. |
| `output_dir` | str    | Yes      | Directory path to save generated payloads. Will be created if it does not exist. |
| `test_file`  | str    | Yes      | Name of the Python file (with or without `.py` extension) in `bonfire/functions/` to run as the test. |

**Examples:**
```bash
pyhton3 bonfire.py test text basic,logic_bypass ./output example
```
This will:
- Generate payloads as in `generate`.
- Import `bonfire/functions/example.py` and call its `run_test(payloads)` function.

---

### Argument Details
- **data_type**: Specify the type of data to augment (`text`, `audio`, or `image`). Determines which augmentation methods and templates are used.
- **format**: (Optional) Specify the output format for audio or image payloads. Ignored for text. If omitted, defaults to `mp3` for audio, `png` for image.
- **methods**: Comma-separated list of augmentation methods to use, or `all` for every available method. Available methods are listed in the CLI help and depend on your templates directory.
- **output_dir**: Directory where generated payloads will be saved. Will be created if it does not exist.
- **test_file** (test only): Name of the Python script in `bonfire/functions/` to run. Can be specified with or without the `.py` extension. Must define a `run_test(payloads)` function.

---

### Example Test Script
Place a file like this in `bonfire/functions/example.py`:
```python
from typing import List, Dict

def run_test(payloads: List[Dict[str, str]]):
    print(payloads)
```

---


## TODO
- Results analysis and report generation: Allow for specification of an OpenAI compatible or Ollama endpoint to determine if the model responded in an unsafe way. Generate an HTML report for the results that is filterable. I have these in othe rmodules and just need to implement here
- Multi-turn functionality: Allow for a list of prompts in the `prompt` value to facilite multi-turn testing
- Perhaps add more granukar control of the augmentations applied

## Authors
- skribblez

---
For more details, see the code in the `bonfire/utils/` directory and the CLI help output.
