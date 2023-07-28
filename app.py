from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "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"


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    title = data.get('title')
    message = f"I need a blog post about {title}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return jsonify({'content': response['choices'][0]['message']['content']}), 200

@app.route('/alter', methods=['POST'])
def alter():
    data = request.get_json()
    selected_text = data.get('selected_text')
    context = data.get('context')
    version = data.get('version')

    versions = {
        'shorter': 'shorter and concise',
        'longer': 'more detailed and longer',
        'casual': 'casual and conversational',
        'professional': 'more formal and professional'
    }
    
    instruction = versions[version]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Rewrite the following text: '<<<{selected_text.rstrip('.')}>>>' in a {instruction} way. Use the following context for understanding the meaning: '{context}'. Don't rewrite the entire context, just provide the rewritten text."
            }
        ],
        temperature=0.6,
        n=5  # generate 5 alternatives
    )
    alternatives = [choice['message']['content'].replace('<<<', '').replace('>>>', '') for choice in response['choices']]
    
    # Remove exact duplicates
    alternatives = list(set(alternatives))
    
    return jsonify({'content': alternatives}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

