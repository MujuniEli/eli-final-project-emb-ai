function RunSentimentAnalysis() {
    let textToAnalyze = document.getElementById("textToAnalyze").value;
    let responseDiv = document.getElementById("system_response");

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                responseDiv.innerHTML = this.responseText;
                responseDiv.style.color = "black";
            } else {
                responseDiv.innerHTML = "Error: " + this.responseText;
            }
        }
    };
    
    let encodedText = encodeURIComponent(textToAnalyze);
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodedText, true);
    xhttp.send();
}