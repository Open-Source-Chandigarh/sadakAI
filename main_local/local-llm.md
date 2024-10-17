# Local LLM (knowledge based embedding)
This is an extension of sadakAI, a fully local LLM that works on knowledge based embeddings.
__Note:__ [ollama](https://ollama.com/)'s llama3.2 is used as the base model here, make sure you have ollama and the appropriate model installed, if another model is used please update [main_local.py](main_local.py).

## Installation
1. Clone the repository

``` bash
git clone -b local-llm https://github.com/Open-Source-Chandigarh/sadakAI.git
cd sadaakAI
```

2. Required dependencies can be found in [requirements.txt](requirements.txt), run the following code to install them on your machine/python envrionment (conda environment is recommended).

``` bash
pip install -r requirements.txt
```
## Usage

1. Execute the [main_local.py](main_local.py]) file.
``` bash
python3 main_local/main_local.py
```