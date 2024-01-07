from flask import Flask, render_template, request, jsonify
import os
import json
from openai import OpenAI  # Make sure this matches your actual setup for OpenAI



my_api_key = os.environ.get('OPENAI_API_KEY')




# Initialize OpenAI client
client = OpenAI(api_key=my_api_key)

app = Flask(__name__)

assistant_id = 'asst_n2SszS8qe4pvaPrEwmAzkLmE'



def get_assistant_response(message):
    try:
        # Create a new thread
        thread = client.beta.threads.create()
        thread_id = thread.id

        # Send the message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        # Run the assistant on the thread and get the response
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for the assistant's response
        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run.status == 'completed':
                break

        # Retrieve all messages from the thread
        messages_response = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        # Extract the assistant's response
        for msg in messages_response.data:
            if msg.role == 'assistant':
                return " ".join(content.text.value for content in msg.content if hasattr(content, 'text'))

    except Exception as e:
        print(f"Error in getting assistant response: {e}")
        return "Sorry, an error occurred."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        user_prompt = data.get('prompt')
        addVesper = data.get('addVesper')


        

        if not user_prompt:
            raise ValueError("No prompt provided or prompt is empty.")


        
       
        if addVesper:
            # Logic when addVesper is True
            refined_prompt = get_assistant_response(user_prompt)
            response = client.images.generate(
                model="dall-e-3",
                prompt="Please create " + user_prompt + " based on these guidelines: " + refined_prompt,
                size="1024x1024",
                quality="hd",
                n=1
            )
        else:
            # Logic when addVesper is False
            # Adjust the parameters as needed
            response = client.images.generate(
                model="dall-e-3",
                prompt=user_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

        # Correct format to extract the image URL
        image_url = response.data[0].url

        return jsonify({'imageUrl': image_url})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
