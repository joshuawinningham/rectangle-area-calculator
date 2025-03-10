from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_area():
    area = None
    length = None
    width = None
    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        area = length * width
    return render_template('index.html', area=area, length=length, width=width)

if __name__ == '__main__':
    app.run(debug=True)