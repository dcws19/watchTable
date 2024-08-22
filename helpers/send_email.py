import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(html_file_path, subject, to_email):
    from_email = "morrisroe.jack@gmail.com"

    # Read the HTML file
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "morrisroe.jack@gmail.com"
    smtp_password = "rgva tsmn shtx ugev "

    # Create the email
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the HTML content as the email body
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Example code (will not run if imported by another script)
if __name__ == "__main__":
    html = "/Users/JMM/Documents/GitHub/watchTable/emails/week1_report.html"
    sub = "Week 1 Watch Tables"
    email = "intalamu@yahoo.com"

    send_email(html_file_path=html, subject=sub, to_email=email)
