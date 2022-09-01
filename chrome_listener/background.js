let global_notif_count = 0;
// setInterval(async function () {
//     const tabs = await chrome.tabs.query({
//         url: [
//             "https://web.whatsapp.com/*",
//         ],
//     });
//
//     checkForTitle(tabs[0]);
//     chrome_tab = tabs[0].title;
// }, 5000)

chrome.tabs.onUpdated.addListener(function (
    tabId,
    changeInfo,
    tab
) {
if (tab.url === "https://web.whatsapp.com/") {
    if (tab.title.includes("(") && tab.title.includes(")")) {
        let current_notif_count = tab.title.match(/\d+/)[0]
        if (current_notif_count > global_notif_count) {
            global_notif_count = current_notif_count
            sendNotification()
            }
        }
    }
}
);

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