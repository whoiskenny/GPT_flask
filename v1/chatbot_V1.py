import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

messages = []

def chatbot(prompt, tone="neutral"):
    usr_message = {"role": "user", "content": prompt}
    messages.append(usr_message)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    reply = response.choices[0].message.content

    assistant_msg = {"role": "assistant", "content": reply}
    messages.append(assistant_msg)

    return reply

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    assistant_reply = chatbot(user_input)
    return jsonify({"assistant_reply": assistant_reply})

if __name__ == '__main__':
    app.run(debug=True)
