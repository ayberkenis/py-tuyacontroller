let chrome_tab = "";

setInterval(async function () {
    const tabs = await chrome.tabs.query({
        url: [
            "https://web.whatsapp.com/*",
        ],
    });

    checkForTitle(tabs[0]);
    chrome_tab = tabs[0].title;
}, 5000)


function checkForTitle(tab) {
    console.log(chrome_tab)
    console.log(tab.title)
    if (chrome_tab !== tab.title) {
        sendNotification()
    }
}

async function sendNotification() {
    const response = await fetch("http://localhost:8080/api/v1/whatsapp_notification/", {
    method: 'POST',
    headers: {'Content-Type':'application/json',
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'},
    body: `{
       "data": "success",
      }`,
    });
    response.json().then(data => {
      console.log(data);
    });
}