import os
import base64
import pyrebase
from dotenv import load_dotenv
from openai import OpenAI

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

OpenAI_APIKEY = os.environ.get("API_KEY")
print(OpenAI_APIKEY)

# Firebase configuration
firebase_config = {
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain",
    "databaseURL": "https://hashcode-d61de-default-rtdb.firebaseio.com/",
    "projectId": "hashcode-d61de",
    "storageBucket": "gs://hashcode-d61de.appspot.com",
    "messagingSenderId": "your-messaging-sender-id",
    "appId": "your-app-id"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Initialize OpenAI API client
client = OpenAI(api_key=OpenAI_APIKEY)

prompt = "Give a brief summary of this, make sure you describe all the scenarios of the scenery and what is happening. 50 words is fine"

# List of image file paths
image_file_paths = ['C:\\Users\\laxma\\OneDrive\\Desktop\\Database\\2323232.jpg', 'C:\\Users\\laxma\\OneDrive\\Desktop\\Database\\random.jpg', 'C:\\Users\\laxma\\OneDrive\\Desktop\\Database\\pyreisthegoat.jpeg']

for image_path in image_file_paths:
    print(f"Trying to open file: {image_path}")

    if os.path.isfile(image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Generate description using OpenAI's GPT-4 vision model
        stream = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "image": encoded_image},
                    ],
                }
            ],
            max_tokens=200,
            stream=True,
        )

        description = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                description += chunk.choices[0].delta.content

        # Print the generated description
        print(f"Description for {image_path}:")
        print(description)
        print("\n")
        
            
        

        try:
            # Upload image path and summary to Firebase Realtime Database
            db.child("images").push({
                'image_path': image_path,
                'summary': description
            })
            print(f"Uploaded data for {image_path} to Firebase.")
        except Exception as e:
            print(f"Error uploading data for {image_path} to Firebase: {e}")

    else:
        print(f"File not found: {image_path}")
        print("\n")
