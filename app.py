from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from urllib.parse import quote
from datetime import datetime

app = Flask(__name__)
user_sessions = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From')

    response = MessagingResponse()
    msg = response.message()

    session = user_sessions.get(sender, {'step': 0})

    if incoming_msg.lower() == 'hi':
        session = {'step': 1}
        msg.body("👋 Welcome to HR Dost!
Please choose an option:

Apply for Visiting Card
(Type 1)")

    elif session['step'] == 1 and incoming_msg == '1':
        session['step'] = 2
        msg.body("Enter your full name (e.g., Rajnikant Tiwari)")

    elif session['step'] == 2:
        session['name'] = incoming_msg
        session['step'] = 3
        msg.body("Enter your employee number (e.g., BB1234)")

    elif session['step'] == 3:
        session['emp_no'] = incoming_msg
        session['step'] = 4
        msg.body(
            "✅ Your visiting card request is ready.

"
            "🎯 Final Step — Choose how to send your request:

"
            "A – Outlook Web (opens auto-filled email in browser)
"
            "B – Copy-paste email text into your Outlook app
"
            "C – Open default email app (Outlook must be default)

"
            "Please reply with A, B, or C to continue."
        )

    elif session['step'] == 4:
        choice = incoming_msg.upper()
        name = session.get('name', '')
        emp_no = session.get('emp_no', '')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if choice == 'A':
            body = f"I would like to apply for visiting card.\nName: {name}\nEmployee Number: {emp_no}"
            email_body = quote(body)
            outlook_link = (
                "https://outlook.office.com/mail/deeplink/compose?"
                "to=hnihr@bajajbroking.in"
                "&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
                "&subject=Request%20for%20Visiting%20Card"
                f"&body={email_body}"
            )
            msg.body(
                "📢 Make sure you are logged in to Outlook Web in your browser.
"
                "If already logged in, please click the link below to send your email:

"
                f"🔗 {outlook_link}"
            )

        elif choice == 'B':
            email_text = (
                "📋 Copy the text below and paste it in your Outlook app:

"
                "To: hnihr@bajajbroking.in
"
                "CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in
"
                "Subject: Request for Visiting Card

"
                "I would like to apply for visiting card.
"
                f"Name: {name}
"
                f"Employee Number: {emp_no}"
            )
            msg.body(email_text)

        elif choice == 'C':
            mail_body = f"I would like to apply for visiting card.
Name: {name}
Employee Number: {emp_no}"
            mailto_link = (
                "mailto:hnihr@bajajbroking.in"
                "?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
                "&subject=Request for Visiting Card"
                f"&body={quote(mail_body)}"
            )
            msg.body(
                "⚠️ If your default email app is NOT Outlook, please choose Option A or B instead.

"
                f"🔗 {mailto_link}"
            )
        else:
            msg.body("❌ Invalid choice. Please reply with A, B, or C.")

        session['step'] = 0

    user_sessions[sender] = session
    return str(response)
