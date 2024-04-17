async function getRequest(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        cache: 'no-cache'
    })
    return response.json()
}
document.addEventListener('DOMContentLoaded', function () {
    let url = document.location
    let route = "/flaskwebgui-keep-server-alive"
    let interval_request = 3 * 1000 //sec
    function keep_alive_server() {
        getRequest(url + route)
            .then(data => console.log(data))
    }
    setInterval(keep_alive_server, interval_request)()
})


// Prevent F12 key
document.onkeydown = function (e) {
    if (e.key === "F12") {
        e.preventDefault();
    }
};

// Prevent right-click 
document.addEventListener("contextmenu", function (e) {
    e.preventDefault();
});