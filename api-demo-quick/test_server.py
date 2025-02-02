from flask import Flask, request, jsonify
import openai
import base64
import os
from dotenv import load_dotenv
import csv
import json
import tempfile

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_csv_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if 'color' in row:
                mapping[row['color']] = row['value']
            elif 'shape' in row:
                mapping[row['shape']] = row['value']
    return mapping

def create_prompt_guide(color_mapping, shape_mapping):
    color_guide = "\n".join([f"{value}: {color}" for color, value in color_mapping.items()])
    shape_guide = "\n".join([f"{value}: {shape}" for shape, value in shape_mapping.items()])
    return f"""Analyze the pill image and provide the imprint, color number, and shape number.
    I will format your response into a URL to search on drugs.com.
    Use ONLY these numeric values:
    Colors:
    {color_guide}
    Shapes:
    {shape_guide}
    Return ONLY a JSON with three fields:
    {{
        "imprint": "text on pill",
        "color": "number from color list",
        "shape": "number from shape list"
    }}"""

def save_base64_image(base64_string):
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        image_data = base64.b64decode(base64_string)
        temp_file.write(image_data)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        raise Exception(f"Error saving image: {str(e)}")

def chat_with_gpt(prompt, image_path=None, model="gpt-4o-mini", max_tokens=4096):
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    
    if image_path:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        response_format={ "type": "json_object" }
    )
    
    try:
        response_json = json.loads(response.choices[0].message.content)
        url = f"https://www.drugs.com/imprints.php?imprint={response_json['imprint']}&color={response_json['color']}&shape={response_json['shape']}"
        return url
    except json.JSONDecodeError:
        return "Error: Could not parse GPT response as JSON"
    except KeyError:
        return "Error: Missing required fields in GPT response"

@app.route('/analyze_pill', methods=['POST'])
def analyze_pill():
    try:
        # Check if the request contains the image
        if 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400

        # Get the base64 image from the request
        base64_image = request.json['image']
        
        # Save the base64 image to a temporary file
        temp_image_path = save_base64_image(base64_image)
        
        # Load mappings from CSV files
        color_mapping = load_csv_mapping('color_type.txt')
        shape_mapping = load_csv_mapping('shape_type.txt')
        
        # Create prompt with valid values
        prompt = create_prompt_guide(color_mapping, shape_mapping)
        
        # Process the image and get the URL
        result = chat_with_gpt(prompt, image_path=temp_image_path)
        
        # Clean up the temporary file
        os.unlink(temp_image_path)
        
        return jsonify({'url': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)