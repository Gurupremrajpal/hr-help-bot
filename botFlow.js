const userState = {};

async function handleMessage(from, message) {
  // Reset if user types "Hi"
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
      return `👋 Welcome to HR Dost!\n\nPlease choose an option:\n1. Apply for Visiting Card`;

    case 1:
      if (message === "1") {
        userState[from].step++;
        return `Please enter your full name:`;
      } else {
        return `Invalid option. Please reply with 1 to apply for Visiting Card.`;
      }

    case 2:
      userState[from].name = message;
      userState[from].step++;
      return `Please enter your employee number:`;

    case 3:
          case 3:
      userState[from].empNo = message;
      userState[from].step++;

      const name = userState[from].name;
      const empNo = userState[from].empNo;

      const optionA = `🟢 Option A:\nOutlook Web:\nhttps://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20${encodeURIComponent(name)}%0AEmployee%20Number:%20${encodeURIComponent(empNo)}`;

      const optionB = `🟡 Option B:\nCopy and paste in Outlook App:\nTo: hnihr@bajajbroking.in\nCC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in\nSubject: Request for Visiting Card\nBody: I would like to apply for visiting card.\nName: ${name}\nEmployee Number: ${empNo}`;

      const optionC = `🔵 Option C:\nDefault Mail App:\nmailto:hnihr@bajajbroking.in?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20${encodeURIComponent(name)}%0AEmployee%20Number:%20${encodeURIComponent(empNo)}`;

      return `🎯 Final Step — Choose how to send your request:\n\n${optionA}\n\n${optionB}\n\n${optionC}`;

  }

  return `Something went wrong. Please type "Hi" to restart.`;
}

module.exports = { handleMessage };
