import openai
import base64
import os
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def encode_image_to_base64(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def chat_with_gpt(prompt, image_path=None, model="gpt-4o-mini", max_tokens=4096):
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    if image_path:
        base64_image = encode_image_to_base64(image_path)
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    text_prompt = "Reply in the following format in json: is_pill: True/False, color: yellow/white/..., shape: circle/rectangle/..."
    local_image_path = "./test.jpeg"  # Provide the correct local image path
    try:
        result = chat_with_gpt(text_prompt, image_path=local_image_path)
        print("ChatGPT Response:", result)
    except Exception as e:
        print("Error:", str(e))
