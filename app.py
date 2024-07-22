from flask import Flask, request, redirect, send_from_directory, render_template_string
from base64 import b64decode
import face_recognition
import os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    face_match = False
    image = request.form.get('current_image')
    
    if image is None:
        return render_template_string("<script>alert('Missing image. Please provide the required fields.')</script>")
    
    try:
        header, encoded = image.split(",", 1)
        data = b64decode(encoded)
        
        with open("image.jpeg", "wb") as f:
            f.write(data)

        got_image = face_recognition.load_image_file("image.jpeg")
        got_image_facialfeatures = face_recognition.face_encodings(got_image)
        
        if not got_image_facialfeatures:
            return render_template_string("<script>alert('No face detected in the image.')</script>")
        
        got_image_facialfeatures = got_image_facialfeatures[0]

        # Directory of images to compare against
        student_images_dir = "students/"
        for file_name in os.listdir(student_images_dir):
            if file_name.endswith(".jpeg"):
                existing_image_path = os.path.join(student_images_dir, file_name)
                existing_image = face_recognition.load_image_file(existing_image_path)
                existing_image_facialfeatures = face_recognition.face_encodings(existing_image)

                if not existing_image_facialfeatures:
                    continue
                
                existing_image_facialfeatures = existing_image_facialfeatures[0]

                results = face_recognition.compare_faces([existing_image_facialfeatures], got_image_facialfeatures)

                if results[0]:
                    face_match = True
                    break
    except Exception as e:
        return render_template_string(f"<script>alert('Error processing the image: {str(e)}')</script>")

    if face_match:
        # Redirect to Streamlit app on successful login
        return redirect("https://6614-171-48-101-135.ngrok-free.app/")  # Change the URL to your Streamlit app's URL for website and ngrok url for mobile app
    else:
        return render_template_string("<script>alert('Face not recognized')</script>")

@app.route('/')
def index():
    print("defult route")
    return send_from_directory('static', 'index.html')

@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('static/css', filename)

#if __name__ == '__main__':
#    port = 5000
#    print(f"Starting server on port {port}...")
#    app.run(debug=True, port=port)



# to use ngrok: run the code to start the server. go to ngrok terminal and type ngrok http 5000 
# the port number(5000) changes according to your server's port number.  