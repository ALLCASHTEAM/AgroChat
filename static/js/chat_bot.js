

// ONLOAD AND EVENT TRIGGERS

  // handle onload actions
  window.addEventListener("load", (e) =>{

  // check if there's something in localStorage and load it into chat
    if (loadFromLocal("user").length > 0){
      userStory = loadFromLocal("user").split(";").slice(1);
      botStory = loadFromLocal("bot").split(";").slice(1);

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
    var chatList = document.querySelector('.chatlist');
    chatList.scrollTop = chatList.scrollHeight;
  }

// INPUTS

  // handle input shortcuts
  const textInput = document.getElementById("textInput");

  textInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      makeBubbles();

      scrollToBottom();
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
    if (document.getElementsByClassName("send_img")[0].files[0]){
      var imageObj = document.getElementsByClassName("send_img")[0];
      document.getElementsByClassName("attach-button").textContent = imageObj.name;
      return imageObj.files[0]
    }
    else{
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

  // make bot bubble with unique class
  function makeBotBubble(text, image=null){
    var botBubbleCounter = document.getElementsByClassName("bot__output").length;
    var chatBubble_bot = document.createElement('li');
    chatBubble_bot.classList.add('bot__output', 'bot__output--standard', 'animateBubble', "id-" + (botBubbleCounter + 1));
    chatBubble_bot.innerHTML = text;
    chatList.appendChild(chatBubble_bot);
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
      console.log(type);
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

    // if text is smaller than 2 symbols and there is no image throw alert
    if (text.trim() <= 2 && !loadImage()){
      alert("Текст должен содержать больше 2 символов");
      return
    }
    if (loadImage() && text.trim() > 0){
      alert("Пожалуйста, либо отправьте текст, либо картинку");
      document.getElementsByClassName("send_img")[0].value = "";
      document.getElementsByClassName("chatbox")[0].value = "";
      return
    }

    var url = '/request';

    // create chatBubble for user, scroll and save to localStorage

    if (loadImage()){
      var userBubbleId = makeUserBubble(text, 1);
      scrollToBottom();
      var waitForImage = new Promise (async (resolve, reject) => {
        try{
          imageHash = await getImageHash(loadImage());
          editUserBubble(id=userBubbleId, {image: imageHash["imageName"]});
          saveToLocal("user", text, imageHash["imageName"]);
          document.getElementsByClassName("send_img")[0].value = "";
          document.getElementsByClassName("attach-button")[0].textContent = "Прикрепить изображение";
          document.getElementById('submitButton').disabled = true;

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
    document.getElementById('submitButton').disabled = true;


    var botBubbleId = makeBotBubble("");
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
      document.querySelectorAll(".id-" + botBubbleId + ".bot__output")[0].innerHTML = resp["text"];
      scrollToBottom();
      document.getElementById('submitButton').disabled = false;
      saveToLocal("bot", resp["text"], resp["image"]);

    }).catch((error) => {
      console.error('Async function failed with error:', error);
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
