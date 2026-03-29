from flask import Flask, request, jsonify
from flask_cors import CORS
import forgery_detector

app = Flask(__name__)
# Enable CORS for all domains so React can call this API
CORS(app)

@app.route('/api/detect-forgery', methods=['POST'])
def detect_forgery_endpoint():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
        
    file = request.files['image']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        try:
            # Read the file data into memory
            image_bytes = file.read()
            
            # Process the image utilizing OpenCV ORB logic
            processed_base64, num_forgeries = forgery_detector.detect_forgery(image_bytes)
            
            return jsonify({
                "status": "success",
                "processed_image": f"data:image/jpeg;base64,{processed_base64}",
                "forgery_count": num_forgeries,
                "is_forged": num_forgeries > 5  # Simple heuristic threshold
            }), 200
        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
