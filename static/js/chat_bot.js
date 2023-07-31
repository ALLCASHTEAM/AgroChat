var sendForm = document.querySelector('#chatform'),
    textInput = document.querySelector('.chatbox'),
    chatList = document.querySelector('.chatlist'),
    animationCounter = 1,
    animationBubbleDelay = 600;

function scrollToBottom() {
  chatList.scrollTop = chatList.scrollHeight;
}

sendForm.onkeydown = function(e){
  if(e.keyCode == 13){
    e.preventDefault();

    //No mix ups with upper and lowercases
    var input = textInput.value.toLowerCase();

    //Empty textarea fix
    if(input.length > 0) {
      createBubble(input);
    }
  }
};

sendForm.addEventListener('submit', function(e) {
  //so form doesnt submit page (no page refresh)
  e.preventDefault();

  //No mix ups with upper and lowercases
  var input = textInput.value.toLowerCase();

  //Empty textarea fix
  if(input.length > 0) {
    createBubble(input);
  }
});

var createBubble = function(input) {
  //create input bubble
  var chatBubble = document.createElement('li');
  chatBubble.classList.add('userInput');

  //adds input of textarea to chatbubble list item
  chatBubble.innerHTML = input;

  //adds chatBubble to chatlist
  chatList.appendChild(chatBubble);
  scrollToBottom();
  clearInput();
}

function clearInput() {
  // Clear the text from the input field after sending
  textInput.value = "";
  // Focus back on the input field
  textInput.focus();
}

//change to SCSS loop
function animateBotOutput() {
  chatList.lastElementChild.style.animationDelay= (animationCounter * animationBubbleDelay)+"ms";
  animationCounter++;
  chatList.lastElementChild.style.animationPlayState = "running";
}
  document.getElementById("chatform").addEventListener("submit", function (event) {
    event.preventDefault();
    const chatbox = document.getElementById("textInput");
    const message = chatbox.value.trim();
    chatbox.value = "";

    // Создаем элемент <li> для сообщения и добавляем его в <ul> для отображения в чате
    const chatList = document.getElementById("chatlist");
    const messageItem = document.createElement("li");
    messageItem.classList.add("userInput");
    messageItem.textContent = message;
    chatList.appendChild(messageItem);

    // Обработка загруженного изображения, если оно есть
    const fileInput = document.getElementById("upload");
    const file = fileInput.files[0];
    if (file) {
      // Показываем изображение, создавая элемент <img> и добавляя его в чат
      const imageItem = document.createElement("img");
      imageItem.classList.add("userInput");
      imageItem.src = URL.createObjectURL(file);
      chatList.appendChild(imageItem);
      //change label to filename and after send delete it from loader
    }

    // Прокручиваем чат вниз, чтобы видеть последние сообщения
    chatList.scrollTop = chatList.scrollHeight;
  });
