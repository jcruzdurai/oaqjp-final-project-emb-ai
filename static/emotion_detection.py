import requests
import json

# Watson NLP Emotion Predict API URL
URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

# Headers for the request
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    "Content-Type": "application/json"
}

def emotion_detector(text):
    """
    Input text to analyze for emotions and return a dictionary containing scores of anger, disgust, fear, joy, sadness, and the dominant emotion.
    """
    emotionInput = {
        "raw_document": {
            "text": text
        }
    }
        
    # POST to Emotion Predict API
    response = requests.post(URL, headers=HEADERS, data=json.dumps(emotionInput))
        
    # Check for a successful response
    if response.status_code == 200:
            
        # Convert response text to a dictionary using json.loads()
        response_dict = json.loads(response.text)

        # Check the structure to access the right part of the response
        if 'emotionPredictions' in response_dict:
            emotions = response_dict['emotionPredictions']  # Correct this part based on response structure
        else:
            print("Error: Unable to find 'emotion_predictions' in the response")
            return None

        emotion_data = response_dict['emotionPredictions'][0]['emotion']

        # Accessing each emotion
        anger = emotion_data['anger']
        disgust = emotion_data['disgust']
        fear = emotion_data['fear']
        joy = emotion_data['joy']
        sadness = emotion_data['sadness']

        # Create a dictionary of the emotions
        emotion_scores = {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness
        }

        print("emotion_scores : ", emotion_scores)
        # Find the dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Add the dominant emotion to the result
        emotion_scores["dominant_emotion"] = dominant_emotion

        return emotion_scores
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

def main():
    text_input = input("Enter an Input to analyze for emotions: ")

    # Call the emotion detector
    emotion_data = emotion_detector(text_input)

    # Output the detected emotions if successful
    if emotion_data:
        print("Emotion analysis result:")
        print(json.dumps(emotion_data, indent=2))
    else:
        print("No emotions found.")

if __name__ == "__main__":
    main()

