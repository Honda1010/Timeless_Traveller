from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'moustafalaa30@gmail.com'
app.config['MAIL_PASSWORD'] = 'zjojyrangfledltl'

mail = Mail(app)

@app.route('/send_email')
def send_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=["youssifmo0310@gmail.com"],  # Replace with your recipient
            body="This is a test email sent from Flask-Mail."
        )
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
