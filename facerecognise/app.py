from flask import Flask, render_template, request, jsonify
import cv2
import pymongo
import base64
import numpy as np
import os
import face_recognition

app = Flask(__name__)

# Adjust these variables as needed
DATABASE_NAME = "your_database"
IMAGES_FOLDER = "images"
TOLERANCE = 0.6


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        image_data = request.form['image']

        # Convert base64 image data to numpy array
        nparr = np.frombuffer(base64.b64decode(
            image_data.split(',')[1]), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Save image to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[DATABASE_NAME]
        users_collection = db["users"]
        _, jpeg_image = cv2.imencode('.jpg', img)
        jpeg_image_bytes = jpeg_image.tobytes()

        user_data = {
            "username": username,
            "image": jpeg_image_bytes
        }
        users_collection.insert_one(user_data)

        # Save image to local folder
        folder_path = os.path.join(os.getcwd(), IMAGES_FOLDER)
        os.makedirs(folder_path, exist_ok=True)
        image_path = os.path.join(folder_path, f"{username}.jpg")
        cv2.imwrite(image_path, img)

        return jsonify({"message": "User registered successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        # Retrieve username and image data from the request
        username = request.form['username']
        image_data = request.form['image']

        # Convert base64 image data to numpy array
        nparr = np.frombuffer(base64.b64decode(
            image_data.split(',')[1]), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Load the registered user's image from MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[DATABASE_NAME]
        users_collection = db["users"]
        user_data = users_collection.find_one({"username": username})

        if user_data:
            # Retrieve the image data from the user data
            registered_image = cv2.imdecode(np.frombuffer(
                user_data["image"], np.uint8), cv2.IMREAD_COLOR)

            # Encode the images to face encoding vectors
            registered_encoding = face_recognition.face_encodings(registered_image)[
                0]
            captured_encoding = face_recognition.face_encodings(img)[0]

            # Compare the face encodings to determine if they match
            match = face_recognition.compare_faces(
                [registered_encoding], captured_encoding, tolerance=TOLERANCE)

            # Add this line to see the result of face recognition
            print("Match:", match)

            if match[0]:
                # If the images match, return a success message
                return jsonify({"message": "User verified."})
            else:
                # If the images do not match, return an error message
                return jsonify({"message": "Face not recognized."})
        else:
            # If the username is not found in the database, return an error message
            return jsonify({"message": "User not found."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
