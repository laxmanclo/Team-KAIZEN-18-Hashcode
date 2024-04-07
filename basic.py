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

def search_images_by_keyword(keyword):
    try:
        image_ref = db.child("images").order_by_child("summary").equal_to(keyword)
        images = image_ref.get().val()
        if images:
            matched_images = []
            for image_id, image_data in images.items():
                matched_images.append((image_data['image_path'], image_data['summary']))

            # Sort the list of matched images based on the summary
            matched_images.sort(key=lambda x: x[1])

            for image_path, summary in matched_images:
                print(f"Image Path: {image_path}")
                print(f"Summary: {summary}")
                print()
        else:
            print(f"No images found with the keyword '{keyword}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Prompt user for keyword
search_keyword = input("Enter a keyword to search for images: ")
print(f"Searching for images with keyword: {search_keyword}") # Debugging line

# Call the search function with the user's input
search_images_by_keyword(search_keyword)