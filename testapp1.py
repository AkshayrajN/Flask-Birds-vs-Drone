# from flask import Flask, render_template, request, jsonify, send_file
# from tensorflow import keras
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import os
# import uuid

# app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB, change as needed

# model = keras.models.load_model('best_modelthird.h5')
# Define your class names here
# class_names = ['2S1','BMP2','BRDM2','BTR60','BTR70','D7','SLICY','T62','T72','ZIL131','ZSU_23_4']

# @app.route('/')
# def home():
    # return render_template('upload1.html')

# @app.route('/process_image', methods=['POST'])
# def process_image():
    # if 'image' not in request.files:
        # return jsonify({'error': 'No file part'})

    # img = request.files['image']

    # if img.filename == '':
        # return jsonify({'error': 'No selected file'})

    #Generate a unique temporary file name
    # img_path = os.path.join('temp', str(uuid.uuid4()) + '.jpeg')
    # img.save(img_path)

    # try:
        # img = image.load_img(img_path, target_size=(64, 64))
        # img = image.img_to_array(img)
        # img = np.expand_dims(img, axis=0)

        # result = model.predict(img)

        #Find the class with the highest probability
        # predicted_class_index = np.argmax(result)
        # predicted_class = class_names[predicted_class_index]

       # Return the predicted class label, probability, and processed image
        # response = {
            # 'predicted_class': predicted_class,
            # 'probability': float(result[0][predicted_class_index]),
            # 'image_url': '/processed-image'
        # }

        # return jsonify(response)
    # except Exception as e:
        # return jsonify({'error': str(e)})
    # finally:
       # Clean up the temporary file
        # os.remove(img_path)

# @app.route('/get_processed_image')
# def get_processed_image():
    #You can process and generate the processed image here
   # For example, load and process the original image, save it, and then serve it

   # Load the original image
    # original_img = image.load_img(img_path, target_size=(64, 64))
    
    #Process the image as needed (e.g., perform image manipulation or classification)
    #For demonstration purposes, let's save and serve the same image as processed
    # processed_img_path = 'processed_image.jpeg'
    # original_img.save(processed_img_path)

    #Send the processed image as a file
    # return send_file(processed_img_path, as_attachment=True)

# if __name__ == "__main__":
   # Create a 'temp' directory for storing temporary files
    # os.makedirs('temp', exist_ok=True)
    
    # app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_from_directory
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB, change as needed

model = keras.models.load_model('best_modelthird.h5')

# Define your class names here
class_names = ['2S1', 'BMP2', 'BRDM2', 'BTR60', 'BTR70', 'D7', 'SLICY', 'T62', 'T72', 'ZIL131', 'ZSU_23_4']

@app.route('/')
def home():
    return render_template('upload1.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    img = request.files['image']

    if img.filename == '':
        return jsonify({'error': 'No selected file'})

    # Generate a unique temporary file name
    img_path = os.path.join('temp', str(uuid.uuid4()) + '.jpeg')
    img.save(img_path)

    try:
        img = image.load_img(img_path, target_size=(64, 64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        result = model.predict(img)

        # Find the class with the highest probability
        predicted_class_index = np.argmax(result)
        predicted_class = class_names[predicted_class_index]

        # Return the predicted class label, probability, and processed image URL
        response = {
            'predicted_class': predicted_class,
            'probability': float(result[0][predicted_class_index]),
            'image_url': '/get_processed_image/' + os.path.basename(img_path)
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        # Clean up the temporary file
        os.remove(img_path)

@app.route('/get_processed_image/<filename>')
def get_processed_image(filename):
    return send_from_directory('temp', filename)

if __name__ == "__main__":
    # Create a 'temp' directory for storing temporary files
    os.makedirs('temp', exist_ok=True)
    
    app.run(debug=True)
