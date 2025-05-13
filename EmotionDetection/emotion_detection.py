import requests
import json

def emotion_detector(text_to_analyze: str) -> dict:
    # Handle empty input immediately
    if not text_to_analyze.strip():
        return None

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=myobj, headers=header, timeout=5)
        if response.status_code != 200:
            return None

        data = json.loads(response.text)
        emotions = data['emotionPredictions'][0]['emotion']
        
        # Check for gibberish (all scores below threshold)
        if all(score < 0.05 for score in emotions.values()):
            return None

        dominant = max(emotions.items(), key=lambda x: x[1])[0]
        
        return {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': dominant
        }

    except (requests.exceptions.RequestException, 
            json.JSONDecodeError, 
            KeyError, 
            IndexError):
        return None