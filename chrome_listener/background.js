let global_notif_count = 0;

function getStoredKey(key) {
    return chrome.storage.sync.get(key).then(function (value) {
        return value[key];
    });
}

chrome.tabs.onUpdated.addListener(function (
        tabId,
        changeInfo,
        tab
    ) {

        if (tab.url === getStoredKey("site_url")) {
            console.log('yes it is the url')
            if (tab.title.includes("(") && tab.title.includes(")")) {
                let current_notif_count = tab.title.match(/\d+/)[0]
                if (current_notif_count < global_notif_count) {
                    // message has been read
                } else if (current_notif_count > global_notif_count) {
                    // new notification
                    global_notif_count = current_notif_count
                    sendNotification()
                }
                global_notif_count = current_notif_count

            }
        }
    }
);


async function sendNotification() {
    let body = {"action": "sendnotification", "color": "green"};
    body = JSON.stringify(body);
    const response = await fetch("http://localhost:8080/api/v1/bulb/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'
        },
        body: body,
    });
    try {
    response.json().then(data => {
        console.log(data);
    });
    }
    catch (error) {
        console.log("There has been an error while processing the request to the URL.", error);
    }

}