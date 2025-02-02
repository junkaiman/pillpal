import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def drug_interaction_prompt(drug_name):
    return f"{drug_name}: Provide a short summary for an elderly patient, no jargon, one sentence, less than 15 words."

def chat_with_gpt(prompt, model="gpt-4o-mini", max_tokens=4096):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def gpt_summarize(json_file, save_dir):
    with open(json_file, "r") as f:
        pill_data = json.load(f)

    # Format drug data for summarization
    drug_summary_prompt = f"Please provide a concise summary of the drug details in under 60 words, focusing on key information without following a readme format, less than 3 paragraphs: {json.dumps(pill_data, indent=2)}"
    drug_summary = chat_with_gpt(drug_summary_prompt)

    # Initialize dictionary to store responses
    processed_data = {
        "imgUrl": pill_data.get("imgUrl", {}),
        "description": drug_summary,
        #"interactions": {"major interactions": {}, "moderate interactions": {}},
        "interactions": {"major interactions": {}},
        "sideEffects": pill_data.get("sideEffects", {})
    }

    # Process interactions
    # for interaction_type in ["major interactions", "moderate interactions"]:
    for interaction_type in ["major interactions"]:
        for drug in pill_data.get("interactions", {}).get(interaction_type, []):
            interaction_summary = chat_with_gpt(drug_interaction_prompt(drug))
            processed_data["interactions"][interaction_type][drug] = interaction_summary

    save_path = os.path.join(save_dir,"processed_pill_info.json")
    with open(save_path, "w") as f:
        json.dump(processed_data, f, indent=4)

    return save_path


if __name__ == "__main__":
    input_json_path = "pill_info.json"
    gpt_summarize(input_json_path, "./")
