var waitingForResponse = false;

document.getElementById('infoWrapper').addEventListener('click', function() {
    let obj = document.getElementById('dialogueInfoWrapper');
    if (obj.style.visibility == 'visible') {
        obj.style.visibility = 'hidden';
    } else {
        obj.style.visibility = 'visible';
    }
});

document.getElementById('backToSite').addEventListener('click', function() {
    window.location.href = 'https://betaren.ru/';
});

document.getElementById('about').addEventListener('click', function() {
    window.location.href = 'https://betaren.ru/about/';
});


// ONLOAD AND EVENT TRIGGERS

// handle onload actions
window.addEventListener("load", (e) => {
    // check if there's something in localStorage and load it into chat
    if (loadFromLocale("user").length > 0) {
        userStory = String(loadFromLocale("user")).split(";text:").slice(1);
        botStory = String(loadFromLocale("bot")).split(";text:").slice(1);

        for (let i = 0; i < userStory.length && i < botStory.length; i++) {
            userData = userStory[i];
            botData = botStory[i];
            //check if there is image
            if (userData.split("\\image:").length > 1) {
                imageName = userData.split("\\image:")[1];
                let imagePath = `/static/user_images/${imageName}`;
                makeUserBubble(null, imagePath);
            } else {
                makeUserBubble(userData);
            }
             makeBotBubble(botData);
        }
        scrollToBottom();
    }

});
const fileInput = document.querySelector('.send_img');
const chatList = document.querySelector('.chatlist');
document.getElementsByClassName("send_img")[0].addEventListener("input", (() => {
    document.getElementsByClassName("attach-button")[0].textContent = fileInput.files[0].name;
}));
// MISC

// scroll to bottom
function scrollToBottom() {
    var chatList = document.querySelector('#scroller');
    chatList.scrollTop = chatList.scrollHeight;
}

// INPUTS

// handle input shortcuts
const textInput = document.getElementById("textInput");

textInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        makeBubbles();
    }
    if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        this.value = this.value.substring(0, start) + "\n" + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 1;
    }
});

// handle image input
function loadImage() {
    if (document.getElementsByClassName("send_img")[0].files[0]) {
        var imageObj = document.getElementsByClassName("send_img")[0];
        document.getElementsByClassName("attach-button").textContent = imageObj.name;
        return imageObj.files[0]
    } else {
        return null
    }
}

// CHAT BUBBLES

// make user bubble

function editUserBubble(bubbleId, image){
    let m = document.getElementsByClassName("userInput id-" + bubbleId);
    m[0].querySelector("img").src = "static/user_images/" + image;
}

function makeUserBubble(text, image = null) {
    var chatBubble = document.createElement('li');
    var chatBubbleCounter = document.getElementsByClassName("userInput").length;
    chatBubble.classList.add('userInput', 'id-' + (chatBubbleCounter + 1));

    // Create a container for image and text
    var container = document.createElement('div');
    // Append the image if there is one
    if (image) {
        var imageDiv = document.createElement('img');
        imageDiv.src = "/static/user_images/" + image;
        // Set the image width to 100%
        imageDiv.style.width = '90%';
        container.appendChild(imageDiv);
    }

    // Append the text
    var textDiv = document.createElement('div');
    textDiv.textContent = text;
    container.appendChild(textDiv);

    chatBubble.appendChild(container);

    chatList.appendChild(chatBubble);

    scrollToBottom();

    return chatBubbleCounter + 1
}

// make bot bubble with unique class
// make bot bubble with unique class
// make bot bubble with unique class
function makeBotBubble(text, image = null) {

    var botBubbleCounter = document.getElementsByClassName("bot__output").length;
    if (text.length == 0) {
        // Удаляем существующую кнопку регенерации, если она есть
        var existingRegenerateButton = document.querySelector('.regenerate');
        if (existingRegenerateButton) {
            existingRegenerateButton.remove();
        }

        var chatBubble_bot = document.createElement('li');
        chatBubble_bot.classList.add('animateBubble', "id-" + (botBubbleCounter + 1)); //28.02 если эта строка(157) есть, то лайк/дизлайк идёт поверх бабла, а если её нет, то бот отвечает на прошлое сообщение)

        var container = document.createElement('div'); // Create a container for text


        var textDiv = document.createElement('div'); // Create a div for the text
        textDiv.classList.add('bot__output', 'animateBubble', "id-" + (botBubbleCounter + 1));

        var mark_like = document.createElement('div');
        mark_like.classList.add('like', "id-" + (botBubbleCounter + 1));

        var mark_dislike = document.createElement('div');
        mark_dislike.classList.add('dislike', "id-" + (botBubbleCounter + 1));

        var regenerate = document.createElement('div'); //29.02
        regenerate.classList.add('regenerate', "id-" + (botBubbleCounter + 1)); //29.02

        textDiv.innerHTML = '<span class="loader loader_custom_zalupa" ></span>';
        container.appendChild(textDiv); // Append the text div to the containers
        container.appendChild(mark_dislike);
        container.appendChild(mark_like);
        container.appendChild(regenerate); //29.02
        chatBubble_bot.appendChild(container); // Append the container to the chat bubble
        chatList.appendChild(chatBubble_bot);

        chatList.appendChild(chatBubble_bot);
    } else {
        var chatBubble_bot = document.createElement('li');
        chatBubble_bot.classList.add('animateBubble', "id-" + (botBubbleCounter + 1)); //28.02 если эта строка(157) есть, то лайк/дизлайк идёт поверх бабла, а если её нет, то бот отвечает на прошлое сообщение)

        var container = document.createElement('div'); // Create a container for text
        //хуй тебе, а не класс, глупый контейнер

        var textDiv = document.createElement('div'); // Create a div for the text
        textDiv.classList.add('bot__output', 'animateBubble', "id-" + (botBubbleCounter + 1));

        var mark_like = document.createElement('div');
        mark_like.classList.add('like', "id-" + (botBubbleCounter + 1));

        var mark_dislike = document.createElement('div');
        mark_dislike.classList.add('dislike', "id-" + (botBubbleCounter + 1));

        var regenerate = document.createElement('div'); //29.02
        regenerate.classList.add('regenerate', "id-" + (botBubbleCounter + 1)); //29.02



        textDiv.textContent = text;
        container.appendChild(textDiv); // Append the text div to the containers
        container.appendChild(mark_dislike);
        container.appendChild(mark_like);
        container.appendChild(regenerate); //29.02 гриша умер от спида
        chatBubble_bot.appendChild(container); // Append the container to the chat bubble
        chatList.appendChild(chatBubble_bot);
    }

    scrollToBottom();
    return botBubbleCounter + 1;
}

// Функция регенерации запроса
// Гриша пидорас чтоб тебя сбил поезд
function regenerateLastResponse() {
    console.log("регенерируем");
    const lastBotBubble = document.querySelector('.bot__output').lastElementChild;
    if (lastBotMessage) {
        // Удаление существующего текста
        lastBotBubble.textContent = '';

        // Создание и добавление элемента анимации загрузки
        const loader = document.createElement('span');
        loader.className = 'loader loader_custom_zalupa';
        lastBotBubble.appendChild(loader);

        // Продолжение с вызовом функции, которая отправляет запрос на регенерацию
        const lastBotMessage = loadFromLocal('bot').slice(-1)[0];
        if (lastBotMessage) {
            sendRequestWithRegenerateFlag(lastBotMessage);
        } else {
            alert("Нет последнего сообщения для регенерации.");
            loader.remove();
        }
    }
}


async function sendRequestWithRegenerateFlag(lastMessage) {
    const url = '/request';
    lastTwouser = loadFromLocal('user').slice(-2);
    lastTwobot = loadFromLocal('bot').slice(-2);
    let dataToSend = {
        userMessages: lastTwouser,
        botMessages: lastTwobot,
        image: [],
        flags: ['regenerate']
    };
    console.log(dataToSend);
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
    });

    if (response.ok) {
        const resp = await response.json();
        console.log(resp);
        updateBotBubble(resp.text);
    } else {
        console.error('Request failed:', response.statusText);
    }
}


function updateBotBubble(text) {
    console.log(text);
    const lastBotBubble = document.querySelector('.bot__output').lastElementChild;
    console.log(lastBotBubble.textContent);
    if (lastBotBubble) {
        lastBotBubble.textContent = text;
        const loader = lastBotBubble.querySelector('.loader');
        if (loader) {
            loader.remove(); // Удаление анимации загрузки
        }
    }
}


// LOCAL STORAGE
// save string into local storage
function saveToLocal(type, text, image = null) {
    previous = localStorage.getItem(type);
    if (image) {
        localStorage.setItem(type, previous + ";" + "text:" + text + "\\image:" + image);
    } else {
        localStorage.setItem(type, previous + ";" + "text:" + text);
    }
}

// load from local storage
function loadFromLocal(type) {
    let storedItems = localStorage.getItem(type);

    if (!storedItems) {
        return []; // Возвращает пустой массив, если данных нет
    }
    return storedItems.split(";").map(item => {
        // Предполагаем, что каждый элемент может быть простым текстом или JSON-строкой
        try {
            return JSON.parse(item); // Пытаемся разобрать каждый элемент как JSON
        } catch (e) {
            return item; // Возвращаем как есть, если это простой текст
        }
    });
}

//Grisha's ultra fix after Vlad's destroying everything
function loadFromLocale(type) {
    return localStorage.getItem(type);
}

// REQUESTS

// send request to server and get response
function makeBubbles() {
    const disallowedChars = /[{}[\]<>\\|\/#~*]/;

    var text = document.querySelector('.chatbox').value;
    // if text is smaller than 2 symbols and there is no image throw alert
    if (text.trim() <= 2 && !loadImage()) {
        alert("Слишком короткое сообщение или не выбрано изображение!");
        return
    } else if (disallowedChars.test(text)) {
        alert("В сообщении используются запрещенные символы!");
        return
    } else if (text.trim().length > 1000) {
        alert("Слишком длинное сообщение");
        return
    } else if (loadImage() && (text.trim().length > 0)) {
        alert("Пожалуйста выберите или картинку или текст");
        document.getElementsByClassName("send_img")[0].value = "";
        document.getElementsByClassName("chatbox")[0].value = "";
        document.querySelector('.send_img').value = "";
        document.querySelector('.attach-button').textContent = "Выберите изображение";

        return
    }

    var url = '/request';

    // get server response
    // ебаные промисы сука как же я их рот ебал
    // витоге код с запросам к серверу перенесен в промис, чтобы они друг за другом ебланились

    var promise = new Promise(async (resolve, reject) => {
        try {
            if (loadImage()) {
                var userBubbleId = makeUserBubble(text, 1);
                var imageHash = await getImageHash(loadImage());
                saveToLocal("user", text, imageHash);

                var result = await sendRequest(url, text, imageHash);
                resolve(result);
                editUserBubble(userBubbleId.toString(), imageHash);

            } else {
                var userBubbleId = makeUserBubble(text);
                saveToLocal("user", text);
                var result = await sendRequest(url, text);
                resolve(result);
            }
        } catch (error) {
            reject(error);
        }
    });

    promise.then((resp) => {
        // fill the bot bubble and scroll to bottom
        document.querySelectorAll(".id-" + botBubbleId + ".bot__output")[0].innerHTML = resp["text"];
        scrollToBottom();
        saveToLocal("bot", resp["text"], resp["image"]);

    }).catch((error) => {
        console.error('Async function failed with error:', error);
    });

    // scroll to bottom after everything

    scrollToBottom();

    // remove text from textbox
    document.querySelector('.chatbox').value = "";
    document.getElementsByClassName("send_img")[0].value = "";
    document.querySelector('.send_img').value = "";
    document.querySelector('.attach-button').textContent = "Выберите изображение";

     var botBubbleId = makeBotBubble("");
}

// function that sends request to server
async function sendRequest(url, textData, imageData) {
    // Retrieve all user messages from local storage
    let allUserMessages = loadFromLocal('user'); // Assuming this returns an array of all user messages
    let allBotMessages = loadFromLocal('bot'); // Assuming this returns an array of all bot messages

    // Select the last three messages of each
    let lastThreeUserMessages = allUserMessages.slice(-2);
    let lastThreeBotMessages = allBotMessages.slice(-2);

    // Package these last three messages in a format suitable for your server endpoint
    let dataToSend = {
        userMessages: lastThreeUserMessages,
        botMessages: lastThreeBotMessages,
        image: [imageData],
        flags: []
    };
    // Example: Sending data to the server using fetch API
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            dataToSend),
    });
    if (response.ok) {
        const resp = await response.json();
        return resp;
    } else {
        console.error('Request failed with status:', response.status);
    }
}

// function that gets hash of an image
async function getImageHash(image) {
    const form = new FormData();
    form.append('image', image);
    var response = await fetch("/get_image_hash", {
        method: "POST",
        body: form,
    });
    if (response.ok) {
        var resp = await response.json();
        return resp["imageName"]
    } else {
        console.error('Request failed with status:', response.status);
    }
}

// Выбираем кнопку  (переключение темы)
const btn = document.querySelector(".dark-theme");

//круг для анимки 24.02
const circle = document.getElementById('circle');

// Выбираем таблицу стилей
const theme = document.querySelector("#theme-link");
// Отслеживаем щелчок по кнопке
btn.addEventListener("click", function() {

    // Если текущий адрес содержит "light-theme.css"
    if (theme.getAttribute("href") == "static/css/light-styles.css") {
        // …то переключаемся на "dark-theme.css"
        theme.href = "static/css/dark-styles.css";
        saveThemeToLocalStorage("dark");
        // В противном случае…
    } else {
        // …переключаемся на "light-theme.css"
        theme.href = "static/css/light-styles.css";
        saveThemeToLocalStorage("light");

    }
});

const saveThemeToLocalStorage = (themeValue) => {
    localStorage.setItem("theme", themeValue);
};
document.addEventListener("DOMContentLoaded", function() {
    const savedTheme = localStorage.getItem("theme");

    // Проверяем, есть ли сохраненное значение темы в localStorage
    if (savedTheme === "dark") {
        theme.href = "static/css/dark-styles.css";
    } else {
        theme.href = "static/css/light-styles.css";

    }
});
var sendBtn = document.getElementById('sendBtn');
sendBtn.addEventListener("click", function() {
    makeBubbles();
});
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modal");
    var acceptBtn = document.getElementById("acceptBtn");

    // Проверяем, принял ли пользователь политику конфиденциальности
    var privacyAccepted = localStorage.getItem("privacyAccepted");

    // Если пользователь не принял политику, показываем модальное окно
    if (privacyAccepted !== "true") {
        modal.style.display = "block";
    } else {
        modal.style.display = "none";
    }

    // Обработчик для кнопки "Принять"
    acceptBtn.addEventListener("click", function() {
        // Сохраняем информацию о принятии политики в localStorage
        localStorage.setItem("privacyAccepted", "true");
        // Скрываем модальное окно
        modal.style.display = "none";
    });
});

// Объект для отслеживания состояния кнопок
var buttonState = JSON.parse(localStorage.getItem('LSD_marks')) || {};

function handleClick(event) {
    var target = event.target;
    // Проверяем, был ли клик на элементе с классом like или dislike
    if (target.classList.contains('like') || target.classList.contains('dislike')) {
        // Получаем id элемента
        var id = target.closest('.animateBubble').classList[1].split('-')[1];
        // Получаем название элемента (like или dislike)
        var name = target.classList.contains('like') ? 'like' : 'dislike';
        // Выводим id и название в консоль

        // Получаем путь к активному изображению
        var activeImagePath = name === 'like' ? 'static/resources/like_on.svg' : 'static/resources/disslike_on.svg';

        // Проверяем текущее состояние кнопки
        if (!buttonState[id]) {
            // Если кнопка еще не нажата, устанавливаем активное изображение
            target.style.backgroundImage = 'url(' + activeImagePath + ')';
            // Обновляем состояние кнопки
            buttonState[id] = name;
        } else {
            // Если кнопка уже была нажата
            if (buttonState[id] === name) {
                // Если текущее состояние совпадает с предыдущим, меняем на изображение по умолчанию
                var defaultImagePath = name === 'like' ? 'static/resources/like_off.svg' : 'static/resources/disslike_off.svg';
                target.style.backgroundImage = 'url(' + defaultImagePath + ')';
                // Сбрасываем состояние кнопки
                delete buttonState[id];
            } else {
                // Если текущее состояние отличается от предыдущего, меняем на активное изображение
                target.style.backgroundImage = 'url(' + activeImagePath + ')';
                // Обновляем состояние кнопки
                buttonState[id] = name;
                // Если противоположная кнопка активирована, отключаем ее
                var oppositeButton = name === 'like' ? '.dislike' : '.like';
                var oppositeTarget = target.closest('.animateBubble').querySelector(oppositeButton);
                oppositeTarget.style.backgroundImage = 'url(' + (name === 'like' ? 'static/resources/disslike_off.svg' : 'static/resources/like_off.svg') + ')';
                // Обновляем состояние противоположной кнопки
                buttonState[id] = name;
            }
        }

        // Сохраняем buttonState в localStorage
        localStorage.setItem('LSD_marks', JSON.stringify(buttonState));
    }
    if(target.classList.contains('regenerate')){
        regenerateLastResponse();
    }
}

// Восстановление состояния кнопок при загрузке страницы
window.addEventListener('load', function() {
    for (var id in buttonState) {
        var name = buttonState[id];
        var target = document.querySelector('.id-' + id + ' .' + name);
        if (target) {
            var activeImagePath = name === 'like' ? 'static/resources/like_on.svg' : 'static/resources/disslike_on.svg';
            target.style.backgroundImage = 'url(' + activeImagePath + ')';
        }
    }
});

// Добавляем обработчик клика на список, используя делегирование событий
document.body.addEventListener('click', handleClick);


//удаление чата 01.03
document.addEventListener('DOMContentLoaded', function() {
    // Находим элемент "Очистить чат"
    var clearChatButton = document.getElementById('clearChatButton');

    // Добавляем обработчик события клика на кнопку "Очистить чат"
    clearChatButton.addEventListener('click', function() {
        // Удаляем данные из локального хранилища
        localStorage.removeItem('user');
        localStorage.removeItem('bot');
        localStorage.removeItem('LSD_marks');

        // Обновляем страницу
        location.reload();
    });
});

document.getElementById('upload').onchange = function() {
    var fileName = this.files[0].name; // Получить имя файла
    document.querySelector('.attach-button').textContent = fileName; // Изменить текст на label
};

