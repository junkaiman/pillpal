import requests
import json
import base64
import os

def test_pill_analysis(image_path, api_url='http://127.0.0.1:5001/analyze_pill'):
    try:
        # Ensure configs directory exists
        os.makedirs('./configs', exist_ok=True)
        
        # Convert image to base64
        with open(image_path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare the request
        headers = {'Content-Type': 'application/json'}
        payload = {'image': base64_string}
        
        # Send POST request
        print("Sending request to API...")
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Print response
        print('\nStatus Code:', response.status_code)
        
        if response.status_code == 200:
            result = response.json()  # This will be an array
            print(result)
            if result and len(result) > 0:
                pill_data = result[0]  # Get the first (and only) item
                
                # Print the formatted result
                print("\nPill Information:")
                print("Description:", pill_data.get('description', 'Not available'))
                
                print("\nInteractions:")
                interactions = pill_data.get('interactions', {})
                
                major = interactions.get('major interactions', {})
                if major:
                    print("\nMajor Interactions:")
                    for drug, desc in major.items():
                        print(f"- {drug}")
                
                moderate = interactions.get('moderate interactions', {})
                if moderate:
                    print("\nModerate Interactions:")
                    for drug, desc in moderate.items():
                        print(f"- {drug}")
                
                side_effects = pill_data.get('sideEffects', {})
                if side_effects:
                    print("\nSide Effects:")
                    for category, effects in side_effects.items():
                        print(f"\n{category}:")
                        for effect in effects:
                            print(f"- {effect}")
            else:
                print("No data returned from the API")
        else:
            print('Error1:', response.json())
        
    except Exception as e:
        print(f"Error2: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.content}")

if __name__ == "__main__":
    # Check if image exists
    image_path = "./pills/Alprazolam.png"
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        print("Please ensure your image exists and the path is correct")
        exit(1)
    
    test_pill_analysis(image_path)