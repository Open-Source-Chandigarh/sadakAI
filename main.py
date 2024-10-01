from flask import Flask, render_template, request
from httpx import stream
from litgpt import LLM
import torch



# Load the model
llm = LLM.load("microsoft/phi-1_5")


app = Flask(__name__)

# Simulated AI model function
def sadakAIout(input_text):
    # Process the input text
    proccesed_text = llm.generate(input_text)
    output_text = ""
    for text in proccesed_text:
        output_text += text
        if '.' in text:
            break
    # Ensure the output stops at the first period
    output_text = output_text.split('.')[0] + '.'
    return output_text

@app.route('/', methods=['GET', 'POST'])
def index():
    result_message = ""
    if request.method == 'POST':
        input_message = request.form['input_message']
        result_message = sadakAIout(input_message)
    return render_template('index.html', result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)