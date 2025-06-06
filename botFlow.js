const userState = {};

async function handleMessage(from, message) {
  if (message.toLowerCase() === "hi") {
    userState[from] = { step: 0 };
  }

  if (!userState[from]) {
    userState[from] = { step: 0 };
  }

  const state = userState[from];

  switch (state.step) {
    case 0:
      userState[from].step++;
      return "👋 Welcome to HR Dost!\n\nPlease choose an option:\n1. Apply for Visiting Card";

    case 1:
      if (message === "1") {
        userState[from].step++;
        return "Please enter your full name:";
      } else {
        return "Invalid option. Please reply with 1 to apply for Visiting Card.";
      }

    case 2:
      userState[from].name = message;
      userState[from].step++;
      return "Please enter your employee number:";

    case 3:
      userState[from].empNo = message;
      userState[from].step++;

      const name = userState[from].name;
      const empNo = userState[from].empNo;

      return `Thank you ${name} (${empNo}). Your request is ready.\n\nClick below to send email:\nhttps://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&subject=Request%20for%20Visiting%20Card`;
  }

  return "Something went wrong. Please type \"Hi\" to restart.";
}

module.exports = { handleMessage };
