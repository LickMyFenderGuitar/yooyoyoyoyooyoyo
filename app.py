from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__, static_folder='public', static_url_path='/')

api_key = "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"
os.environ["GROQ_API_KEY"] = api_key

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Ensure the request has the correct content type
        if request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        user_message = request.json.get('message')

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Call Groq API to generate a response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="deepseek-r1-distill-qwen-32b",
            stream=False,
        )
        
        # Extract Groq's response
        chat_response = chat_completion.choices[0].message.content
        return jsonify({'response': chat_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    app.run(debug=True)
