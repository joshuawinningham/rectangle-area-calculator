from flask import Flask, render_template, request
import os
import resend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
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
    area = None
    length = None
    width = None
    email_sent = False
    
    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        area = length * width
        
        email = request.form.get('email')
        if email:
            email_sent = send_email(email, length, width, area)
    
    return render_template('index.html', 
                         area=area, 
                         length=length, 
                         width=width, 
                         email_sent=email_sent)

if __name__ == '__main__':
    app.run(debug=True)