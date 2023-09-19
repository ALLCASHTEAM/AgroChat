
document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('submitButton');

    button.addEventListener('click', function() {
        var dataFromLocalStorage = localStorage.getItem('myData');//myData поменять на ключ к local storage

        fetch('/request', {
            method: 'POST',
            body: JSON.stringify({ text: dataFromLocalStorage }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {

            console.log(data);

            var dialog = data.text;
        });
    });
});
