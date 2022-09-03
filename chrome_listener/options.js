let tab_list = []
let choose_site = document.getElementById('choose_site')
function get_tabs() {
    chrome.tabs.query({ }, function (tabs) {

        tabs.forEach(function(tab) {
        tab_list.push(tab)
        var opt = document.createElement('option');
        opt.value = tab.url;
        opt.innerHTML = tab.title;
        choose_site.appendChild(opt);
    });
});

}

function save_options() {
    let site_url = document.getElementById('choose_site').value;
    let method = document.getElementById('watch_for_type').value;
    chrome.storage.sync.set({
        site_url: site_url,
        method: method
    }, function () {
        var status = document.getElementById('status');
        status.textContent = "Options saved.";
        setTimeout(function () {
            status.textContent = '';
        }, 2500);
    });
}


function restore_options() {
    console.log('Restoring Options')
    get_tabs()
    chrome.storage.sync.get({
        site_url: 'https://web.whatsapp.com/',
        method: 'numeric'
    }, function (items) {
        document.getElementById('choose_site').value = items.site_url;
        document.getElementById('watch_for_type').value = items.method;

    });
}

async function checkServerStatus() {
    try {
        const response = await fetch("http://localhost:8080/api/v1/server_status/", {
            method: 'POST',
        });

        response.text().then(data => {
            setTimeout(function () {
            serverstatus.textContent = "Server is running and available.";
        }, 2500);
        });
    }
    catch (error) {
        let serverstatus = document.getElementById('serverstatus');
        setTimeout(function () {
            serverstatus.textContent = "Server is not running.";
        }, 2500);

        console.log("There has been an error while processing the request to the URL.", error);
    }
}



document.addEventListener("DOMContentLoaded", restore_options);

document.getElementById('save').addEventListener('click', save_options);
document.getElementById('check').addEventListener('click', checkServerStatus);