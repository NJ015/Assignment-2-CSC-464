from flask import Flask, request, jsonify, render_template
import pickle

# Load the saved model
with open("trigram_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# def predict_next_word(w1, w2):
#     key = (w1, w2)
#     if key in model:
#         return max(model[key], key=model[key].get)
#     return "No prediction available"

# def predict_next_word(w1, w2, top_n=5):
#     key = (w1, w2)
#     if key in model:
#         # Get the top N predictions and their probabilities
#         sorted_predictions = sorted(model[key].items(), key=lambda x: x[1], reverse=True)
#         return sorted_predictions[:top_n]
#     return []

def predict_next_word(w1, w2, top_n=5):
    key = (w1, w2)
    if key in model:
        sorted_predictions = sorted(model[key].items(), key=lambda x: x[1], reverse=True)
        return sorted_predictions[:top_n]  # Return top N predictions with probabilities
    return [("No prediction available", 1.0)]


# def predict_next_word(w1, w2, top_n=5):
#     key = (w1, w2)
#     if key in model:
#         sorted_predictions = sorted(model[key].items(), key=lambda x: x[1], reverse=True)
#         return [(word, prob) for word, prob in sorted_predictions[:top_n]]
#     return []


# def predict_multiple_words(w1, w2, num_words):
#     predictions = []
#     for _ in range(num_words):
#         next_word = predict_next_word(w1, w2)
#         predictions.append(next_word)
#         w1, w2 = w2, next_word  # Move the window forward
#     return predictions


# @app.route('/')
# def home():
#     return render_template('nextwordrecommender.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     w1 = request.form.get('w1', '').lower()
#     w2 = request.form.get('w2', '').lower()
    
#     if not w1 or not w2:
#         return render_template('nextwordrecommender.html', prediction="Please enter two words.")

#     prediction = predict_next_word(w1, w2)
#     return render_template('nextwordrecommender.html', prediction=f"Next word: {prediction}", w1=w1, w2=w2)

# def predict():
#     w1 = request.form.get('w1', '').lower()
#     w2 = request.form.get('w2', '').lower()
#     top_n = int(request.form.get('top_n', 5))  # Get how many predictions to show (default is 5)
    
#     if not w1 or not w2:
#         return render_template('nextwordrecommender.html', prediction="Please enter two words.")

#     predictions = predict_next_word(w1, w2, top_n)
#     return render_template('nextwordrecommender.html', predictions=predictions)

# def predict():
#     w1 = request.form.get('w1', '').lower()
#     w2 = request.form.get('w2', '').lower()
#     num_words = int(request.form.get('num_words', 1))  # How many words to predict
    
#     if not w1 or not w2:
#         return render_template('nextwordrecommender.html', prediction="Please enter two words.")

#     predictions = predict_multiple_words(w1, w2, num_words)
#     print(predictions)  # Add this line to debug
#     return render_template('nextwordrecommender.html', predictions=predictions)









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
    app.run(debug=True, port=5001)
