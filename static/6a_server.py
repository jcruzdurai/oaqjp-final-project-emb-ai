from flask import Flask, render_template, request, jsonify
import requests
import json

# Initialize the Flask app
app = Flask(__name__)

# Define the Watson NLP Emotion Predict API URL and Headers (replace with actual credentials if required)
URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    "Content-Type": "application/json"
}

# Define the route with the specified Flask decorator
@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector():
    if request.method == 'POST':
        # Retrieve the user's text input from the form
        user_text = request.form.get('statement', '')

        # Prepare the payload for Watson NLP API
        payload = {
            "raw_document": {
                "text": user_text
            }
        }

        # Send POST request to the Watson NLP API
        response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))

        if response.status_code == 200:
            # Parse the response JSON
            response_dict = json.loads(response.text)

            # Extract emotion data from the API response
            if 'emotionPredictions' in response_dict:
                emotion_data = response_dict['emotionPredictions'][0]['emotion']
                
                # Find the dominant emotion
                dominant_emotion = max(emotion_data, key=emotion_data.get)
                
                # Create a dictionary to store the scores and dominant emotion
                emotion_scores = {**emotion_data, "dominant_emotion": dominant_emotion}

                # Format the output as per the requirements
                result = f"Let's say that you want to evaluate the statement: {user_text}. " \
                         f"The statement is processed as follows: Emotion detected is {dominant_emotion}."
                
                return jsonify({'result': result, 'emotion_scores': emotion_scores})
            else:
                return jsonify({'error': "Could not retrieve emotions from response"}), 500
        else:
            return jsonify({'error': f"Error: Received status code {response.status_code}"}), 500

    # Render the index.html file for GET requests
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)