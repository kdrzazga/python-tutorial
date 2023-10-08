from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form.get('name')
    gender = request.form.get('gender')

    # Do something with the data (e.g., print it)
    print(f'Name: {name}, Gender: {gender}')

    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
