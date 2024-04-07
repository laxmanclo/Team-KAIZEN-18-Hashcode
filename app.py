from flask import Flask, render_template, request, jsonify
import os
import base64
from openai import OpenAI
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Hashcode"
)
cursor = db.cursor()

# Initialize OpenAI API client
client = OpenAI(api_key='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')

prompt = "Give a brief summary of this, make sure you describe all the scenarios of the scenery and what is happening. 50 words is fine"

# Other existing routes...

@app.route('/search', methods=['GET'])
def search_images():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    cursor.execute("SELECT image_path, summary FROM images")
    results = cursor.fetchall()

    matching_image_paths = []
    for image_path, summary in results:
        if keyword.lower() in summary.lower():
            matching_image_paths.append(image_path)

    if not matching_image_paths:
        return jsonify({'message': 'No images found for the given keyword'}), 404

    return jsonify({'image_paths': matching_image_paths})

# Other existing routes and code...

if __name__ == '__main__':
    app.run(debug=True, port=5001)