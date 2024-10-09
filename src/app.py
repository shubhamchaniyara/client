# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import ViltProcessor, ViltForQuestionAnswering
# from PIL import Image
# import requests, wikipedia
# import torch
# import pyttsx3

# app = Flask(__name__)
# CORS(app)

# # Load model and processor
# processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
# model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

# # Text-to-Speech function
# def narrate_text(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     image_url = data.get('image_url')
#     question = data.get('question')

#     # Load image
#     image = Image.open(requests.get(image_url, stream=True).raw)

#     # Process image and question
#     encoding = processor(image, question, return_tensors="pt")
#     outputs = model(**encoding)
#     logits = outputs.logits
#     idx = logits.argmax(-1).item()
#     answer = model.config.id2label[idx]

#     # Fetch Wikipedia information
#     try:
#         summary = wikipedia.summary(answer + " (animal)", sentences=3)
#     except wikipedia.exceptions.DisambiguationError as e:
#         summary = f"Disambiguation error: {e.options}"

#     # Narrate the answer
#     # narrate_text(f"The answer is {answer}. {summary}")

#     return jsonify({
#         'answer': answer,
#         'info': summary
#     })

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import requests, wikipedia
import torch
import pyttsx3
import os

app = Flask(__name__)
CORS(app)

# Load model and processor
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

# Text-to-Speech function
def narrate_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/predict', methods=['POST'])
def predict():
    question = request.form.get('question')
    image_url = request.form.get('image_url')
    image_file = request.files.get('image')

    # Load image from URL or file
    if image_url:
        image = Image.open(requests.get(image_url, stream=True).raw)
    elif image_file:
        image = Image.open(image_file)
    else:
        return jsonify({'error': 'No image provided'}), 400

    # Process image and question
    encoding = processor(image, question, return_tensors="pt")
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    answer = model.config.id2label[idx]

    # Fetch Wikipedia information
    try:
        summary = wikipedia.summary(answer + " (animal)", sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        summary = f"Disambiguation error: {e.options}"

    # Narrate the answer
    # narrate_text(f"The answer is {answer}. {summary}")

    return jsonify({
        'answer': answer,
        'info': summary
    })

if __name__ == '__main__':
    app.run(debug=True)

