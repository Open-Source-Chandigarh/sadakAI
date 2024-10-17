# sadakAI
### Personalized Roadmaps for Your Software Development Journey
sadakAI is an AI model designed to help users with their software development career roadmaps can analyze individual skills, experiences, and career goals to provide personalized recommendations. It suggests learning paths and skill development milestones, helping users navigate their career progression effectively. This model leverages data from various sources to ensure the advice is up-to-date and relevant.


## Contributions
1. Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
2. Follow the [issues](https://github.com/Open-Source-Chandigarh/sadakAI/issues) to look for potential contributions.
3. The [local-llm](https://github.com/Open-Source-Chandigarh/sadakAI/tree/local-llm) branch is currently in development, head over there to look for potential issues to work on.


## Settup Guide
__Note:__ This is a work in progress project, the project's current working is not intended.


## Installation
1. Clone the repository

``` bash
git clone https://github.com/Open-Source-Chandigarh/sadakAI.git
cd sadaakAI
```

2. Required dependencies can be found in [requirements.txt](requirements.txt), run the following code to install them on your machine/python envrionment (conda environment is recommended).

``` bash
pip install -r requirements.txt
```
<br>

__Note:__ This is a work in progress project, due to it not being hosted on the web yet you have to download and finetune the LLM model on your machine. Before running the model, open [settup.ipynb](settup.ipynb) in jupyter lab/ your preferred text editor and execute all the code blocks inorder to download and finetune the LLM model.

3. Execute the [main.py](main.py]) file.
``` bash
python3 main.py
```

