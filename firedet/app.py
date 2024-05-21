from flask import Flask, render_template, request, jsonify
from fire_detection import FireDetection

app = Flask(__name__)

# Path to your model
model_path = r'C:\Users\acer\Downloads\fireDETEECTOR\my_model.pt'
fire_detector = FireDetection(model_path=model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'result': False, 'message': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'result': False, 'message': 'No selected file'})
    
    if file:
        img_bytes = file.read()
        prediction = fire_detector.predict(img_bytes)
        # Assuming the model returns 1 for fire detected and 0 for no fire
        return jsonify({'result': prediction == 1})

if __name__ == '__main__':
    app.run(debug=True)
