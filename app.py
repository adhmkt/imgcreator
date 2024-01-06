from flask import Flask, render_template, request, jsonify
import json
from openai import OpenAI  # Make sure this matches your actual setup for OpenAI

# Load API key from config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    my_api_key = config['openai_api_key']

# Initialize OpenAI client
client = OpenAI(api_key=my_api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            raise ValueError("No prompt provided or prompt is empty.")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Correct format to extract the image URL
        image_url = response.data[0].url

        return jsonify({'imageUrl': image_url})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
