const express = require("express");
const bodyParser = require("body-parser");
const { handleMessage } = require("./botFlow");
require("dotenv").config();

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));

app.post("/webhook", async (req, res) => {
  const incomingMsg = req.body.Body?.trim();
  const from = req.body.From;

  const reply = await handleMessage(from, incomingMsg);

  res.set("Content-Type", "text/xml");
  res.send(`<Response><Message>${reply}</Message></Response>`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Bot is running on port", PORT));
