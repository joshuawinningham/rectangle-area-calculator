from flask import Flask, render_template, request, redirect, url_for, session
import os
import resend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session
resend.api_key = os.environ.get('RESEND_API_KEY')

def send_email(to_email, length, width, area):
    try:
        params = {
            "from": "Rectangle Calculator <calculator@resend.dev>",
            "to": [to_email],
            "subject": "Your Rectangle Area Calculation Result",
            "html": f'''
                <h2>Rectangle Area Calculation Result</h2>
                <p>With length {length} and width {width}</p>
                <p>The area of the rectangle is: {area} square units</p>
            '''
        }
        
        r = resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def calculate_area():
    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        area = length * width
        
        email = request.form.get('email')
        email_sent = False
        if email:
            email_sent = send_email(email, length, width, area)
        
        # Store results in session
        session['results'] = {
            'area': area,
            'length': length,
            'width': width,
            'email_sent': email_sent
        }
        
        # Redirect to results page
        return redirect(url_for('show_results'))
    
    # For GET requests, show empty form
    return render_template('index.html', 
                         area=None, 
                         length=None, 
                         width=None, 
                         email_sent=False)

@app.route('/results')
def show_results():
    results = session.pop('results', None)  # Remove results from session after showing
    if results is None:
        return redirect(url_for('calculate_area'))
    
    return render_template('index.html',
                         area=results['area'],
                         length=results['length'],
                         width=results['width'],
                         email_sent=results['email_sent'])

@app.after_request
def add_header(response):
    # Prevent caching of all responses
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)