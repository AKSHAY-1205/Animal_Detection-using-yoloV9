from flask import Flask, request, render_template, redirect, url_for
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="k1dHndoqYWx0dAqxwWcJ"
)

# List of farm animals
farm_animals = [
    'Cow', 'Pig', 'Sheep', 'Goat', 'Chicken', 'Duck', 'Turkey', 
    'Horse', 'Donkey', 'Rabbit', 'Llama', 'Alpaca', 'Goose', 
    'Guinea Fowl', 'Quail', 'Bee', 'Buffalo', 'Ox', 'Emu', 
    'Ostrich', 'Camel', 'Yak', 'Deer'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Perform inference
            result = CLIENT.infer(file_path, model_id="farm-animals-j7dxg/1")
            predictions = result.get('predictions', [])
            
            if predictions:
                animal_class = predictions[0].get('class')
                if animal_class.capitalize() in farm_animals:
                    message = f"{animal_class} - No harm is done to the field."
                else:
                    message = f"Alert: {animal_class} is not a farm animal!"
            else:
                message = "No animal detected."
            
            return render_template('index.html', image=file.filename, result=message)
    
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
