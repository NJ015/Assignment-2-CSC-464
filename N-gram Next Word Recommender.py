from flask import Flask, request, jsonify, render_template
import pickle

# Load the saved n-gram model
with open("ngram_model.pkl", "rb") as f:
    ngram_models = pickle.load(f)

app = Flask(__name__)

# Define the prediction function for n-gram models
def predict_next_word(w1, w2, top_n=5):
    key = (w1, w2)  # Using the last two words for prediction
    predictions = []

    for n, model in ngram_models.items():
        if key in model:
            sorted_predictions = sorted(model[key].items(), key=lambda x: x[1], reverse=True)
            predictions.extend(sorted_predictions[:top_n])

    if predictions:
        return predictions[:top_n]  # Return top N predictions
    return [("No prediction available", 1.0)]

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    alternatives = []

    if request.method == "POST":
        text = request.form["text"].strip().split()
        if len(text) < 2:
            return render_template("nextwordrecommender.html", error="Please enter at least two words.")

        predictions = predict_next_word(text[-2], text[-1])
        prediction = predictions[0][0]  # Top prediction
        alternatives = predictions[1:]  # Other predictions

    return render_template("nextwordrecommender.html", prediction=prediction, alternatives=alternatives)

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form["text"].strip().split()
    num_words = int(request.form["num_words"])

    if len(text) < 2:
        return jsonify({"error": "Enter at least two words"}), 400

    generated = text[:]  # Start with user input
    for _ in range(num_words):
        predictions = predict_next_word(generated[-2], generated[-1])  # Use last two words
        next_word = predictions[0][0]  # Top prediction

        if next_word == "No prediction available":
            break  # Stop if no valid prediction
        generated.append(next_word)

    return jsonify({"generated_text": " ".join(generated)})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
