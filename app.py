import json
from flask import Flask, redirect, render_template, request, jsonify, url_for
from chat import get_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.get("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.get("/Faq")  # Changed from "Faq" to "faq" for consistency
def Faq():
    return render_template("Faq.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

def save_feedback(data):
    with open('feedback_data.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')
        
@app.get("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'rating': request.form['rating'],
            'feedback': request.form['feedback']
        }
        save_feedback(feedback_data)
    except KeyError as e:
        return "Missing field: {}".format(str(e)), 400  # Return a 400 error if a required field is missing
    except Exception as e:
        return "An error occurred: {}".format(str(e)), 500  # General error handling

    return redirect(url_for('index_get'))
  # Redirect to the main page after feedback submission

if __name__ == "__main__":
    app.run(debug=True)  # Added this line to run the app in debug mode
