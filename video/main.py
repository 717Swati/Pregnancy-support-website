import cv2
import time
from flask import Flask, render_template, Response

app = Flask(__name__)

# Define the codec for video writing
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Function to record and store video for 20 seconds


def record_and_store():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    # Get the default frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Generate a unique filename with timestamp
    current_time = time.strftime("%Y%m%d_%H%M%S")
    filename = f"output_{current_time}.avi"

    # Create a VideoWriter object to save the video
    out = cv2.VideoWriter(filename, fourcc, fps, (640, 480))

    # Record for 20 seconds
    recording_duration = 20  # in seconds
    start_time = cv2.getTickCount() / cv2.getTickFrequency()
    while True:
        ret, frame = cap.read()
        if ret:
            # Write the frame to the output video
            out.write(frame)

            # Encode the frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Yield the encoded frame
            yield jpeg.tobytes()

            # Check if 20 seconds have elapsed
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if current_time - start_time >= recording_duration:
                break

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    for frame in record_and_store():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, port=5003)
