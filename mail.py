import smtplib
from email.message import EmailMessage
# sender's email and password
EMAIL_ADDRESS = "stock.recommendation.sp@gmail.com"
EMAIL_PASSWORD = "Spro@2021"


def send_email(to_email, token):
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.add_alternative("""\
    <html>
      <head></head>
      <body>
        <p>You requested for password reset from Arc Invoicing application</p>
                    <h5>Please click this <a href="https://arcinvoice.com/reset/"""+token+"""">link</a> to reset your password</h5>
                    <p>Link not clickable?, copy and paste the following url in your address bar.</p>
                    <p>https://arcinvoice.com/reset/"""+token+"""</p>
                    <P>If this was a mistake, just ignore this email and nothing will happen.</P>
      </body>
    </html>
    """, subtype='html')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        # print("email sent")

if __name__ == '__main__':
    send_email("hvtailor16@gmail.com", "my_token")