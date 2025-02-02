import base64
import sys

def image_to_base64(image_path, output_file='encode.txt'):
    try:
        with open(image_path, "rb") as image_file:
            # Read and encode the image
            encoded_string = base64.b64encode(image_file.read())
            # Convert bytes to string for easier use
            base64_string = encoded_string.decode('utf-8')
            
            # Write to output file
            with open(output_file, 'w') as f:
                f.write(base64_string)
            
            print(f"Base64 string has been saved to {output_file}")
            return base64_string
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_image>")
    else:
        image_path = sys.argv[1]
        base64_string = image_to_base64(image_path)