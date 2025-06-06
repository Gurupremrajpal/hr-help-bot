require('dotenv').config();
const express = require('express');
const { MessagingResponse } = require('twilio').twiml;
const { handleMessage } = require('./botFlow');
const twilio = require('twilio');

const app = express();
app.use(express.urlencoded({ extended: false }));

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

app.post('/webhook', async (req, res) => {
  const from = req.body.From;
  const message = req.body.Body;

  try {
    const reply = await handleMessage(from, message);
    await client.messages.create({
      from: 'whatsapp:' + process.env.TWILIO_WHATSAPP_NUMBER,
      to: from,
      body: reply,
    });

    res.sendStatus(200);
  } catch (error) {
    console.error("Error:", error);
    res.sendStatus(500);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`HR Dost Bot running on port ${PORT}`);
});
