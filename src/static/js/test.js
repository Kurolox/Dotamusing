var xhr = new XMLHttpRequest();

xhr.open('GET', "https://api.opendota.com/api/matches/3750796866", true);
xhr.send();

xhr.onreadystatechange = processRequest;

function processRequest(e){
    if (xhr.readyState == 4 && xhr.status == 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
    }
}