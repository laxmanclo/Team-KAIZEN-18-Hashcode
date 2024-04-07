# # from flask import Flask, render_template, request, jsonify

# # app = Flask(__name__)

# # @app.route('/Recollectify')
# # def index():
# #     return render_template('index.html')

# # @app.route

# # @app.route('/signin.html')
# # def signin():
# #     return render_template('signin.html')

# # @app.route('/signup.html')
# # def signup():
# #     return render_template('signup.html')

# # @app.route('/home.html')
# # def home():
# #     return render_template('home.html')
    


# # @app.route('/process_data', methods=['POST'])
# # def process_data():
# #     # Here you would call your AI model and process the uploaded files
# #     # For demonstration purposes, let's just echo back the filenames
# #     uploaded_files = request.files.getlist('files')
# #     output = '\n'.join([file.filename for file in uploaded_files])
# #     return jsonify({'output': output})

# # import os
# # import base64
# # import pyrebase
# # from openai import OpenAI

# # # Firebase configuration
# # firebase_config = {
# #     "apiKey": "your-api-key",
# #     "authDomain": "your-auth-domain",
# #     "databaseURL": "https://hashcode-d61de-default-rtdb.firebaseio.com/",
# #     "projectId": "hashcode-d61de",
# #     "storageBucket": "gs://hashcode-d61de.appspot.com",
# #     "messagingSenderId": "your-messaging-sender-id",
# #     "appId": "your-app-id"
# # }

# # # Initialize Pyrebase
# # firebase = pyrebase.initialize_app(firebase_config)
# # db = firebase.database()

# # # Initialize OpenAI API client
# # client = OpenAI(api_key='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')

# # prompt = "Give a brief summary of this, make sure you describe all the scenarios of the scenery and what is happening. 50 words is fine"

# # # List of image file paths
# # # image_file_paths = ['C:\\Users\\laksh\\OneDrive\\Desktop\\LAKSHYA DOCUMENTS\\Hashcode\\Database\\lesgo.jpg', 'C:\\Users\\laksh\\OneDrive\\Desktop\\LAKSHYA DOCUMENTS\\Hashcode\\Database\\randomimage1.jpeg', 'C:\\Users\\laksh\\OneDrive\\Desktop\\LAKSHYA DOCUMENTS\\Hashcode\\Database\\randomimage2.jpeg']
# # image_file_paths = ['C:\\Users\\laksh\\OneDrive\\Desktop\\LAKSHYA DOCUMENTS\\Hashcode\\Database\\mt.jpeg']

# # for image_path in image_file_paths:
# #     print(f"Trying to open file: {image_path}")

# #     if os.path.isfile(image_path):
# #         with open(image_path, 'rb') as image_file:
# #             image_data = image_file.read()
# #             encoded_image = base64.b64encode(image_data).decode('utf-8')

# #         # Generate description using OpenAI's GPT-4 vision model
# #         stream = client.chat.completions.create(
# #             model="gpt-4-vision-preview",
# #             messages=[
# #                 {
# #                     "role": "user",
# #                     "content": [
# #                         {"type": "text", "text": prompt},
# #                         {"type": "image", "image": encoded_image},
# #                     ],
# #                 }
# #             ],
# #             max_tokens=200,
# #             stream=True,
# #         )

# #         description = ""
# #         for chunk in stream:
# #             if chunk.choices[0].delta.content is not None:
# #                 description += chunk.choices[0].delta.content

# #         # Print the generated description
# #         print(f"Description for {image_path}:")
# #         print(description)
# #         print("\n")

# #         try:
# #             # Upload image path and summary to Firebase Realtime Database
# #             db.child("images").push({
# #                 'image_path': image_path,
# #                 'summary': description
# #             })
# #             print(f"Uploaded data for {image_path} to Firebase.")
# #         except Exception as e:
# #             print(f"Error uploading data for {image_path} to Firebase: {e}")

# #     else:
# #         print(f"File not found: {image_path}")
# #         print("\n")





# # if __name__ == '__main__':
# #     app.run(debug=True)
























from flask import Flask, render_template, request, jsonify
import os
import base64
from openai import OpenAI
import mysql.connector
import requests
from flask_cors import CORS
from flask import Flask, send_from_directory





app = Flask(__name__)
app.static_folder = 'static'

@app.route('/test-image')
def test_image():
    return app.send_static_file('images/img1.jpeg')

@app.route('/search', methods=['GET'])
def search_images():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    cursor.execute("SELECT image_path, summary FROM images")
    results = cursor.fetchall()

    matching_images = []
    for image_path, summary in results:
        if keyword.lower() in summary.lower():
            matching_images.append({'image_path': image_path, 'summary': summary})

    if not matching_images:
        return jsonify({'message': 'No images found for the given keyword'}), 404

    return jsonify({'images': matching_images})

@app.route('/images/<path:filename>')
def serve_images(filename):
    image_dir = os.path.join(app.root_path, 'static', 'images')
    return send_from_directory(image_dir, filename)
CORS(app)


# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Hashcode"
)
cursor = db.cursor()

# Create a table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_path VARCHAR(255),
        summary TEXT
    )
""")

# Initialize OpenAI API client
client = OpenAI(api_key='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')

prompt = "Give a brief summary of this, make sure you describe all the scenarios of the scenery and what is happening. 50 words is fine"

# List of image file paths
image_file_paths = ['static\images\img1.jpeg', 'static\images\img2.jpg', 'static\images\img3.jpeg']

static_dir = os.path.join(app.root_path, 'static')


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/slideshow')
def sds():
    return render_template('slideshow.html', image_paths=requests.get("http://127.0.0.1:5001/search?keyword=cricket").json()["image_paths"])

@app.route('/process_data', methods=['POST'])
def process_data():
    # Here you would call your AI model and process the uploaded files
    # For demonstration purposes, let's just echo back the filenames
    uploaded_files = request.files.getlist('files')
    output = '\n'.join([file.filename for file in uploaded_files])
    return jsonify({'output': output})

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
            # Upload image path and summary to MySQL database
            sql = "INSERT INTO images (image_path, summary) VALUES (%s, %s)"
            values = (image_path, description)
            cursor.execute(sql, values)
            db.commit()
            print(f"Uploaded data for {image_path} to MySQL.")
        except mysql.connector.Error as e:
            print(f"Error uploading data for {image_path} to MySQL: {e}")

    else:
        print(f"File not found: {image_path}")
        print("\n")

if __name__ == '__main__':
    app.run(debug=True)



















# from flask import Flask, render_template, request, jsonify
# import os
# import base64
# from openai import OpenAI
# from werkzeug.utils import secure_filename
# import mysql.connector

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/uploads'

# client = OpenAI(api_key='your_openai_api_key')

# # MySQL configuration
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="Hashcode"
# )
# cursor = db.cursor()

# # Create a table if it doesn't exist
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS images (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         image_path VARCHAR(255),
#         summary TEXT
#     )
# """)

# @app.route('/')
# def index():
#     return render_template('upload.html')

# @app.route('/process_images', methods=['POST'])
# def process_images():
#     images = request.files.getlist('images[]')
#     image_paths = []
#     descriptions = []

#     for image in images:
#         filename = secure_filename(image.filename)
#         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         image.save(image_path)
#         image_paths.append(image_path)

#         with open(image_path, 'rb') as image_file:
#             image_data = image_file.read()
#             encoded_image = base64.b64encode(image_data).decode('utf-8')

#         prompt = "Describe the image in detail."

#         stream = client.chat.completions.create(
#             model="gpt-4-vision-preview",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {"type": "image", "image": encoded_image},
#                     ],
#                 }
#             ],
#             max_tokens=200,
#             stream=True,
#         )

#         description = ""
#         for chunk in stream:
#             if chunk.choices[0].delta.content is not None:
#                 description += chunk.choices[0].delta.content

#         descriptions.append(description)

#         # Insert image path and summary into the database
#         sql = "INSERT INTO images (image_path, summary) VALUES (%s, %s)"
#         values = (image_path, description)
#         cursor.execute(sql, values)
#         db.commit()

#     return jsonify({'image_paths': image_paths, 'descriptions': descriptions})

# @app.route('/search_images', methods=['POST'])
# def search_images():
#     keyword = request.form.get('keyword')

#     cursor.execute("SELECT image_path, summary FROM images WHERE summary LIKE %s", ('%' + keyword + '%',))
#     results = cursor.fetchall()

#     image_paths = [row[0] for row in results]
#     summaries = [row[1] for row in results]

#     return jsonify({'image_paths': image_paths, 'descriptions': summaries})

# if __name__ == '__main__':
#     app.run(debug=True)