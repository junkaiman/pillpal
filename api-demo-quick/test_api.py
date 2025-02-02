import requests
import json

def send_image_to_api(base64_file='encode.txt', url='http://localhost:5001/analyze_pill'):
    try:
        # Read the base64 string from file
        with open(base64_file, 'r') as f:
            base64_string = f.read().strip()
        
        # Prepare the request
        headers = {'Content-Type': 'application/json'}
        payload = {'image': base64_string}
        
        # Send POST request
        response = requests.post(url, headers=headers, json=payload)
        
        # Print response
        print('Status Code:', response.status_code)
        print('Response:', response.json())
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_image_to_api()