# sadakAI
### your one stop solution for learning guidance.
<br>

# Settup Guide

<br>

## Contributing

We appreciate your interest in contributing to **sadakAI**. Here's how you can get started:


0. **Find Issues or Create your Own** We appreciate you solving existing issues in the repository in the issues tab or to create new

1. **Fork the Repository:** Click the "Fork" button at the top of this repository to create a copy in your GitHub account.


2. **Clone Your Fork:** Clone your fork to your local machine with `git clone`.

    git clone https://github.com/<your_github_username>/sadakAI.git

3. **Change the working directory:**  cd sadakAI

4. **Add an upstream link to the main branch in your cloned repo:**

    git remote add upstream https://github.com/<your_github_username>/sadakAI.git

5. **Keep your cloned repo up to date by pulling from upstream (this will also avoid any merge conflicts while committing new changes):**

    git pull upstream main

6. **Create a New Branch:** Make a new branch for your work with a descriptive name.

    git checkout -b <branch-name>

7. **Make Changes:** Implement your desired feature or fix a bug.

8. **Track and stage your changes:**

    git status

9. **Add all the required changes:**

    git add .

10. **Commit all the changes (Write commit message as "Small Message"):**

    git commit -m "<your-commit-message>"

11. **Push the changes for review:**

    git push origin <branch-name>

12. **Open a Pull Request:** Create a pull request from your fork to this repository. Provide a concise title and description.

We'll review your contribution and collaborate to merge it into the project. Please adhere to our code of conduct and guidelines.

If you have questions or need assistance, feel free to open an issue.

## Installation

1. Required dependencies can be found in [requirements.txt](requirements.txt), run the following code to install them on your machine/python envrionment (conda environment is recommended).

``` bash
pip install -r requirements.txt
```
<br>

__Note:__ This is a work in progress project, due to it not being hosted on the web yet you have to download and finetune the LLM model on your machine. Before running the model, open [settup.ipynb](settup.ipynb) in jupyter lab/ your prefered text editor and execute all the code blocks inorder to download and finetune the LLM model.

3. Execute the [main.py](main.py]) file.
``` bash
python3 main.py
```
