var waitingForResponse = false;

document.getElementById('infoWrapper').addEventListener('click', function(){
	let obj = document.getElementById('dialogueInfoWrapper');
	if (obj.style.visibility == 'visible'){
		obj.style.visibility = 'hidden';
	}else{
		obj.style.visibility = 'visible';
	}
});

document.getElementById('backToSite').addEventListener('click', function(){
  window.location.href = 'https://betaren.ru/';
});

document.getElementById('about').addEventListener('click', function(){
  window.location.href = 'https://betaren.ru/about/';
});


// ONLOAD AND EVENT TRIGGERS

  // handle onload actions
  window.addEventListener("load", (e) =>{

  // check if there's something in localStorage and load it into chat
    if (loadFromLocale("user").length > 0){
      userStory = String(loadFromLocale("user")).split(";text:").slice(1);
      botStory = String(loadFromLocale("bot")).split(";text:").slice(1);

      for (let i = 0; i < userStory.length && i < botStory.length; i++){
        userData = userStory[i];
        botData = botStory[i];

        //check if there is image
        if (userData.split("\\image").length == 2){
          userDataText = userData.split("\\")[0].split(":").slice(-1);
          userImageText = userData.split("\\")[1].split(":").slice(-1);
          makeUserBubble(userDataText, userImageText);
        }else{
          makeUserBubble(userData.split(":").slice(-1));
        }
        makeBotBubble(botData.split(":").slice(-1));
      }
      scrollToBottom();
    }

  });
  const fileInput = document.querySelector('.send_img');
  const chatList = document.querySelector('.chatlist');
  document.getElementsByClassName("send_img")[0].addEventListener("input", (()=>{
    console.log(document.getElementsByClassName("send_img")[0]);
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
    if (event.key === "Enter" && event.shiftKey){
      event.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;
      this.value = this.value.substring(0, start) + "\n" + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + 1;
    }
  });

  // handle image input
  //  function loadImage(){
  //    if (document.getElementsByClassName("send_img")[0].files[0]){
  //      var imageObj = document.getElementsByClassName("send_img")[0];
  //      document.getElementsByClassName("attach-button").textContent = imageObj.name;
  //      return imageObj.files[0]
  //    }
  //    else{
  //      return null
  //    }
  //  }

// CHAT BUBBLES

  // make user bubble
  function makeUserBubble(text, image=null){
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
      imageDiv.style.width = '300px';
      container.appendChild(imageDiv);
    }

    // Append the text
    var textDiv = document.createElement('div');
    textDiv.textContent = text;
    container.appendChild(textDiv);

    // Append the container to the chat bubble
    chatBubble.appendChild(container);

    // Append the chat bubble to the chat list (assuming you have a chatList defined)
    chatList.appendChild(chatBubble);

    scrollToBottom();

    return chatBubbleCounter + 1
  }

  // make bot bubble with unique class
    function makeBotBubble(text, image=null){
    if (text.length == 0){
      var botBubbleCounter = document.getElementsByClassName("bot__output").length-1;
      var chatBubble_bot = document.createElement('li');
      chatBubble_bot.classList.add('bot__output', 'animateBubble', "id-" + (botBubbleCounter + 1));
      chatBubble_bot.innerHTML = '<span class="loader loader_custom_zalupa" ></span>';
      chatList.appendChild(chatBubble_bot);
    } else {
     var botBubbleCounter = document.getElementsByClassName("bot__output").length;
    var chatBubble_bot = document.createElement('li');
    var container = document.createElement('div'); // Create a container for text
    var textDiv = document.createElement('div'); // Create a div for the text
    chatBubble_bot.classList.add('bot__output', 'animateBubble', "id-" + (botBubbleCounter + 1));
    textDiv.textContent = text;
    container.appendChild(textDiv); // Append the text div to the container
    chatBubble_bot.appendChild(container); // Append the container to the chat bubble
    chatList.appendChild(chatBubble_bot);
    }

    scrollToBottom();
    return botBubbleCounter + 1;
  }

  // edit user bubble
  function editUserBubble(id, {text, image}){

    if (text && !image){
      var userBubbleText = document.querySelectorAll(".id-" + id + ".userInput")[0];
      userBubbleText.children[0].children[0].textContent = text; // replace text
    }
    if (image){
      var userBubbleImage = document.querySelectorAll(".id-" + id + ".userInput")[0];
      userBubbleImage.children[0].children[0].src = "/static/user_images/" + image;
    }
  }

// LOCAL STORAGE

  // save string into local storage
  function saveToLocal(type, text, image=null){
    previous = localStorage.getItem(type);
    if (image){
      localStorage.setItem(type, previous + ";" + "text:" + text + "\\image:" + image);
    }else{
      localStorage.setItem(type, previous + ";" + "text:" + text);
    }
  }

  // load from local storage
  function loadFromLocal(type){
    let storedItems = localStorage.getItem(type);
    if (!storedItems) {
        return []; // Возвращает пустой массив, если данных нет
    }
    return storedItems.split(";").map(item => {
        // Предполагаем, что каждый элемент может быть простым текстом или JSON-строкой
        try {
            return JSON.parse(item); // Пытаемся разобрать каждый элемент как JSON
        } catch(e) {
            return item; // Возвращаем как есть, если это простой текст
        }
    });
  }

  //Grisha's ultra fix after Vlad's destroying everything
  function loadFromLocale(type){
    return localStorage.getItem(type);
    }

// REQUESTS

  // send request to server and get response
  function makeBubbles()
  {
    var text = document.querySelector('.chatbox').value;
    console.log(text.length);
    // if text is smaller than 2 symbols and there is no image throw alert
    // if (text.trim() <= 2 && !loadImage()) !!!
    const disallowedChars = /[{}[\]<>\\|\/#~*]/;
    if(disallowedChars.test(text)) {
      alert("В сообщении используются запрещенные символы!");
    return 
    }
    if (text.trim().length <= 2){
      alert("Слишком короткое сообщение!");
      return
    }
    if (text.trim().length > 1000) {
      alert("Слишком длинное сообщение");
    return  
    }

    // if loadImage() && !!!!!!
    //  if (text.trim().length > 0){
    //    alert("сука тока либо текст либо картинка");
    //    document.getElementsByClassName("send_img")[0].value = "";
    //    document.getElementsByClassName("chatbox")[0].value = "";
    //    return
    //  }

    var url = '/request';

    // create chatBubble for user, scroll and save to localStorage
    // if (loadImage()) !!!
    if (false){
      var userBubbleId = makeUserBubble(text, 1);
      var waitForImage = new Promise (async (resolve, reject) => {
        try{
        //imageHash = await getImageHash(loadImage());
          imageHash = await getImageHash(loadImage());
          editUserBubble(id=userBubbleId, {image: imageHash["imageName"]});
          saveToLocal("user", text, imageHash["imageName"]);
        }catch(error){
          console.log(error);
        }
      })

    }else{
      var userBubbleId = makeUserBubble(text);
      saveToLocal("user", text);
    }
    scrollToBottom();

    // remove text from textbox
    document.querySelector('.chatbox').value = "";

    var botBubbleId = makeBotBubble("");

    // get server response
    var promise = new Promise(async (resolve, reject) => {
        try {
          //result = await sendRequest(url, text, loadImage());!!!
          result = await sendRequest(url, text);
          resolve(result);
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
  }

  // function that sends request to server
  async function sendRequest(url, textData, imageData){
    // Retrieve all user messages from local storage
    let allUserMessages = loadFromLocal('user'); // Assuming this returns an array of all user messages
    let allBotMessages = loadFromLocal('bot'); // Assuming this returns an array of all bot messages

    // Select the last three messages of each
    let lastThreeUserMessages = allUserMessages.slice(-2);
    let lastThreeBotMessages = allBotMessages.slice(-1);

    // Package these last three messages in a format suitable for your server endpoint
    let dataToSend = {
        userMessages: lastThreeUserMessages,
        botMessages: lastThreeBotMessages
    };

    // Example: Sending data to the server using fetch API
    const response = await fetch(url,{
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
  async function getImageHash(image){
    const form = new FormData();
    form.append('image', image);
    var response = await fetch("/get_image_hash", {
      method: "POST",
      body: form,
    });
    if (response.ok){
      var resp = await response.json();
      return resp
    }else{
      console.error('Request failed with status:', response.status);
    }
  }

    // Выбираем кнопку  (переключение темы)
const btn = document.querySelector(".dark-theme");

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
        console.log("NOT TRUE");
    }else{
        modal.style.display = "none";
    }

    // Обработчик для кнопки "Принять"
    acceptBtn.addEventListener("click", function() {
        // Сохраняем информацию о принятии политики в localStorage
        localStorage.setItem("privacyAccepted", "true");
        console.log("Privacy accepted");
        // Скрываем модальное окно
        modal.style.display = "none";
    });
});

