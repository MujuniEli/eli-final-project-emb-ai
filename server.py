"""Emotion Detection Flask Server"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

def validate_response(response: dict) -> bool:
    """
    Check if the emotion analysis response from emotion_detector is valid.

    Args:
        response: A dictionary containing the emotion analysis results.

    Returns:
        True if the response is valid, False otherwise. A valid response
        is a non-empty dictionary where not all values are None and the
        'dominant_emotion' key has a non-None value.
    """
    if not response:
        return False
    if all(val is None for val in response.values()):
        return False
    if response.get('dominant_emotion') is None:
        return False
    return True

@app.route("/")
def render_index_page():
    """
    Render the index page of the Flask application.

    Returns:
        The rendered HTML template for the index page.
    """
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detection_route():
    """
    Handle requests to the /emotionDetector endpoint.

    Extracts text from the request arguments, performs emotion detection,
    and returns a formatted response or an error message.

    Returns:
        A tuple containing the response body (str) and an HTTP status code (int).
    """
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    # Handle empty input
    if not text_to_analyze:
        return "Invalid text! Please try again!", 400

    # Get emotion analysis
    response = emotion_detector(text_to_analyze)

    # Handle invalid responses (e.g., gibberish or API errors leading to None values)
    if not validate_response(response):
        return "Invalid text! Please try again!", 400

    # Format successful response
    # Using .get() with a default value for dictionary access to prevent KeyError
    # if emotion_detector returns an unexpected structure, although validate_response
    # should ideally catch this.
    anger = response.get('anger')
    disgust = response.get('disgust')
    fear = response.get('fear')
    joy = response.get('joy')
    sadness = response.get('sadness')
    dominant_emotion = response.get('dominant_emotion')

    result = (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return result, 200

if __name__ == "__main__":
    # The extra space at the end of the next line was the cause of C0305
    app.run(host="0.0.0.0", port=5090)