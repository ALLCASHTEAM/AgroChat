

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

document.getElementById('privacy-policy').addEventListener('click', function(){
  window.location.href = 'https://betaren.ru/';
});

document.getElementById('about').addEventListener('click', function(){
  window.location.href = 'https://betaren.ru/about/';
});





// ONLOAD AND EVENT TRIGGERS

  // handle onload actions
  window.addEventListener("load", (e) =>{

  // check if there's something in localStorage and load it into chat
  	try{
	    if (loadFromLocal("user").length > 0){
	      userStory = loadFromLocal("user").split(";").slice(1);
	      botStory = loadFromLocal("bot").split(";").slice(1);

	      for (let i = 0; i < userStory.length && i < botStory.length; i++){
	        userData = userStory[i];
	        botData = botStory[i];

	        // check if there is an image
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
	    }}
	 catch{

	 }

  });
  let fileInput = document.querySelector('.send_img');
  let chatList = document.querySelector('.chatlist');
  console.log("старт"+fileInput);
      console.log("старт"+chatList);
  document.getElementsByClassName("send_img")[0].addEventListener("input", (()=>{
    console.log(document.getElementsByClassName("send_img")[0]);
    document.getElementsByClassName("attach-button")[0].textContent = fileInput.files[0].name;
  }));
// MISC
  // loader
  var loader = '<svg version="1.1" id="L4" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"viewBox="0 0 100 100" enable-background="new 0 0 0 0" xml:space="preserve"> <circle fill="#fff" stroke="none" cx="6" cy="50" r="6"> <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.1"/> </circle> <circle fill="#fff" stroke="none" cx="26" cy="50" r="6"> <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.2"/> </circle> <circle fill="#fff" stroke="none" cx="46" cy="50" r="6"> <animate attributeName="opacity"dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.3"/></circle></svg>';
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
  function loadImage(){
  	try{
	    if (document.getElementsByClassName("send_img")[0].files[0]){
	      var imageObj = document.getElementsByClassName("send_img")[0];
	      document.getElementsByClassName("attach-button").textContent = imageObj.name;
	      return imageObj.files[0]
	    }
	    else{
      		return null
    	}
	}catch{
		return null
	}

  }

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

    return chatBubbleCounter + 1
  }

  function replaceBotAnimwithBubble(responce_text){

    // Находим существующий элемент li с классом "test-output"
    var existingLi = document.querySelector('.test-output');

    // Создаем новый элемент li
    var botBubbleCounter = document.getElementsByClassName("bot__output").length + 1; // Увеличиваем счетчик на 1
    var chatBubble_bot = document.createElement('li');
    chatBubble_bot.classList.add('bot__output', 'bot__output--standard', 'animateBubble', 'id-' + botBubbleCounter);

    // Вам нужно добавить текст в ваш элемент, вместо text
    chatBubble_bot.innerHTML = responce_text;

    // Заменяем существующий элемент на новый элемент
    existingLi.parentNode.replaceChild(chatBubble_bot, existingLi);
    //saveStateToLocalStorage();
    saveHtmlToLocalStorage();

  }
// Save the current HTML code to local storage
function saveHtmlToLocalStorage() {
    var htmlCode = document.documentElement.outerHTML;
    localStorage.setItem('savedHtmlCode', htmlCode);
}

// Restore the HTML code from local storage
function restoreHtmlFromLocalStorage() {
    var savedHtmlCode = localStorage.getItem('savedHtmlCode');
    if (savedHtmlCode) {
      console.log(fileInput);
      console.log(chatList);
        document.open();
        document.write(savedHtmlCode);
        document.close();
        console.log(fileInput);
      console.log(chatList);
    }
}

// Save the HTML code when the page is unloaded (e.g., before a refresh or navigation)
window.addEventListener('beforeunload', saveHtmlToLocalStorage);

// Restore the HTML code when the page is loaded
document.addEventListener('DOMContentLoaded', restoreHtmlFromLocalStorage);

  // make bot bubble with unique class
  function makeBotBubble(text, image=null){
    //var botBubbleCounter = document.getElementsByClassName("bot__output").length;
    var botBubbleCounter = document.getElementsByClassName("test-output").length;
    //var chatBubble_bot = document.createElement('li');
    //chatBubble_bot.classList.add('test-output','bot__output', 'bot__output--standard', 'animateBubble', "id-" + (botBubbleCounter + 1));
    //chatBubble_bot.innerHTML = text;
    //chatList.appendChild(chatBubble_bot);

    var li = document.createElement('li');
    li.classList.add("test-output", "id-"+(botBubbleCounter + 1));

    // Создаем три элемента div с классом "dot" и стилем "--delay"
    var dot1 = document.createElement('div');
    dot1.className = 'dot';
    dot1.style.setProperty('--delay', '200ms');

    var dot2 = document.createElement('div');
    dot2.className = 'dot';
    dot2.style.setProperty('--delay', '300ms');

    var dot3 = document.createElement('div');
    dot3.className = 'dot';
    dot3.style.setProperty('--delay', '400ms');

    // Добавляем элементы div в элемент li
    li.appendChild(dot1);
    li.appendChild(dot2);
    li.appendChild(dot3);

    chatList.appendChild(li);

    return botBubbleCounter + 1
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
    return localStorage.getItem(type)
  }

// REQUESTS

  // send request to server and get response
  function makeBubbles()
  {
    var text = document.querySelector('.chatbox').value;
  	waitingForResponse = true;

    // if text is smaller than 2 symbols and there is no image throw alert
    if (text.trim() <= 2 && !loadImage()){
      alert("Слишком короткое сообщение");
      return
    }
    if (loadImage() && text.trim() > 0){
      alert("текст и картинка не могут быть отправленны одновременно");
      document.getElementsByClassName("send_img")[0].value = "";
      document.getElementsByClassName("chatbox")[0].value = "";
      return
    }

    var url = '/request';

    // create chatBubble for user, scroll and save to localStorage

    if (loadImage()){
      var userBubbleId = makeUserBubble(text, 1);
      var waitForImage = new Promise (async (resolve, reject) => {
        try{
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

    //var botBubbleId = makeBotBubble("") + 1;
    var botBubbleId = makeBotBubble("") + 1;
    var botBubbleID = document.getElementsByClassName("userInput").length + 1;
    console.log(botBubbleID);
    scrollToBottom();

    // get server response
    var promise = new Promise(async (resolve, reject) => {
        try {
          result = await sendRequest(url, text, loadImage());
          resolve(result);
        } catch (error) {
          reject(error);
        }
    });

    promise.then((resp) => {
      // fill the bot bubble and scroll to bottom
      replaceBotAnimwithBubble("");
      document.querySelectorAll(".id-" + botBubbleID + ".bot__output")[0].innerHTML = resp["text"];
      scrollToBottom();
      saveToLocal("bot", resp["text"], resp["image"]);
      waitingForResponse = false;

    }).catch((error) => {
      console.error('Async function failed with error:', error);
      waitingForResponse = false;

    });
  }

  // function that sends request to server
  async function sendRequest(url, textData, imageData){
        // create array with all the data
        const formData = new FormData();
        if (imageData){
          formData.append('image', imageData);
        }
        formData.append('text', textData);
        const response = await fetch(url, {
        method: 'POST',
        body: formData,});
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


const sendButton = document.getElementById('sendBtn');
sendButton.addEventListener('click', function() {
    if (waitingForResponse) {
        return 0
    } else {
        makeBubbles();
    }});

textInput.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    if (waitingForResponse) {
      return 0
    } else {
      makeBubbles();
    }
  }
  if (event.key === "Enter" && event.shiftKey){
    event.preventDefault();
    const start = this.selectionStart;
    const end = this.selectionEnd;
    this.value = this.value.substring(0, start) + "\n" + this.value.substring(end);
    this.selectionStart = this.selectionEnd = start + 1;
  }
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