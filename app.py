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
        msg.body("👋 Welcome to HR Dost!\nPlease choose an option:\n\nApply for Visiting Card\n(Type 1)")

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
            "✅ Your visiting card request is ready.\n\n"
            "🎯 Final Step — Choose how to send your request:\n\n"
            "A – Outlook Web (opens auto-filled email in browser)\n"
            "B – Copy-paste email text into your Outlook app\n"
            "C – Open default email app (Outlook must be default)\n\n"
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
                "📢 Make sure you are logged in to Outlook Web in your browser.\n"
                "If already logged in, please click the link below to send your email:\n\n"
                f"🔗 {outlook_link}"
            )

        elif choice == 'B':
            msg.body(
                "📋 Copy the text below and paste it in your Outlook app:\n\n"
                "To: hnihr@bajajbroking.in\n"
                "CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in\n"
                "Subject: Request for Visiting Card\n\n"
                "I would like to apply for visiting card.\n"
                f"Name: {name}\n"
                f"Employee Number: {emp_no}"
            )

        elif choice == 'C':
            mailto_link = (
                f"mailto:hnihr@bajajbroking.in?cc=employeesupport@bajajbroking.in,"
                f"rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
                "&subject=Request for Visiting Card"
                f"&body={quote('I would like to apply for visiting card.\nName: ' + name + '\nEmployee Number: ' + emp_no)}"
            )
            msg.body(
                "⚠️ If your default email app is NOT Outlook, please choose Option A or B instead.\n\n"
                f"🔗 {mailto_link}"
            )
        else:
            msg.body("❌ Invalid choice. Please reply with A, B, or C.")

        session['step'] = 0

    user_sessions[sender] = session
    return str(response)
