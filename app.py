# save each conversation, date- and time-stamped
#import files
from flask import Flask, render_template, request, jsonify
import openai
import os
from datetime import datetime

openai.api_key = OPENAI_API_KEY

prompt = "You are a witty, helpful assistant that will help clients with any questions they may have."

filename = "conversation_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

def save_to_file(text, response):
    with open(filename, "a") as file:
        file.write("\n" + "User: " + text + "\n")
        file.write("Bot: " + response + "\n")


def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message 


app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("index.html")   


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = generate_response(text)
    message = {"answer": response}
    save_to_file(text, response)
    return jsonify(message)

if __name__ == "__main__":    
    from gunicorn.app.wsgi.app import run
    run()


