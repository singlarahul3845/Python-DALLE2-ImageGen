from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = "Enter your OpenAI_API_Key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']

    # Enhance the prompt using OpenAI's ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fabulous prompt writer that will write prompt for generating fantastic images"}, 
            {"role": "user", "content": f"Write prompt for image generation:\n{prompt}"}
        ]
    )

    # Extract the enhanced prompt from the response
    enhanced_prompt = response.choices[0].message['content']

    # Generate image using DALL·E 2 model
    image_response = openai.Image.create(
        model="dall-e-2",
        prompt=enhanced_prompt,
        n=1,
        size="512x512",
        quality="hd",
    )

    # Extract the image URL from the response
    image_url = image_response['data'][0]['url']

    return render_template('result.html', enhanced_prompt=enhanced_prompt, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
