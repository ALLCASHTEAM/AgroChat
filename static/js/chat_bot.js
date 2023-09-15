var sendForm = document.querySelector('#chatform');
    textInput = document.querySelector('.chatbox');
    chatList = document.querySelector('.chatlist');
    fileInput = document.getElementById("upload");
    animationCounter = 1;
    animationBubbleDelay = 600;
    botAnimationDelay = 600;
    attachButton = document.querySelector('.attach-button');

function loadChatHistoryFromStorage() {
  const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
  const existingMessages = new Set(); // Создаем множество для хранения уникальных сообщений

  chatHistory.forEach(function (messageObject) {
    if (!existingMessages.has(messageObject.message)) { // Проверяем, не было ли уже такого сообщения
      existingMessages.add(messageObject.message); // Добавляем сообщение в множество
      if (messageObject.type === 'user') {
        createBubble(messageObject.message, false); // Пользовательское сообщение без анимации
      } else if (messageObject.type === 'bot') {
        createBubble_bot(messageObject.message, false); // Сообщение бота без анимации
      }
    }
  });
}
window.addEventListener('load', function () {
  loadChatHistoryFromStorage();
});
function addToChatHistory(message, type) {

  // Получаем текущую историю сообщений (если она есть)
  const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

  const messageExists = chatHistory.some(item => item.type === type && item.message === message);

  if (!messageExists) {
    // Если сообщения нет в истории, добавляем его
    chatHistory.push({ type: type, message: message });

    // Сохраняем обновленную историю в LocalStorage
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }
 }

function scrollToBottom() {
  chatList.scrollTop = chatList.scrollHeight;
}



sendForm.onkeydown = function(e) {
  if (e.keyCode === 13) {
    e.preventDefault();

    // No mix ups with upper and lowercases
    var input = textInput.value.toLowerCase();

    // Empty textarea fix
    if (input.length > 0) {
      get_user_text();
      createBubble(input);
      send_bot_answer();
    }
  }
};

sendForm.addEventListener('submit', function(e) {
  // So form doesn't submit page (no page refresh)
  e.preventDefault();

  // No mix ups with upper and lowercases
  var input = textInput.value.toLowerCase();

  // Обработка загруженного изображения, если оно есть
  const file = fileInput.files[0];
  if (input.length > 0 && file) {
    alert("Вы не можете прикрепить изображение вместе с текстом.");
    // Удаляем файл из поля для выбора
    fileInput.value = "";
    // Возвращаем поле для ввода к доступному состоянию
    textInput.disabled = false;
    attachButton.textContent = 'Прикрепить изображение';
  } else if (input.length > 0) {
    // Обрабатываем текстовое сообщение
    createBubble(input);
  } else if (file) {
    // Обрабатываем изображение
    processImage(file);
  } else {
    alert("Пожалуйста выберети изображение или напишите текст.");
  }
});

var createBubble = function(input) {
  // Create input bubble
  var chatBubble = document.createElement('li');
  chatBubble.classList.add('userInput');

  // Add input of textarea to chatbubble list item
  chatBubble.innerHTML = input;
  chatBubble.addEventListener('animationend', function() {
    chatBubble.classList.remove('animateBubble'); // Удаляем класс анимации
  });

  // Add chatBubble to chatlist
  chatList.appendChild(chatBubble);

  scrollToBottom();
  clearInput();
  addToChatHistory(input, 'user');

  createBubble_bot(input);
  animateBotOutput();
  get_bot_text();
};

var createBubble_bot = function(input) {
  // Create input bubble
  var chatBubble_bot = document.createElement('li');
  chatBubble_bot.classList.add('bot__output', 'bot__output--standard', 'animateBubble');

  // Add input of textarea to chatbubble list item
  chatBubble_bot.innerHTML = window.GlobalVar;


  // Add chatBubble to chatlist
  chatList.appendChild(chatBubble_bot);

  addToChatHistory(input, 'bot');

  scrollToBottom();
  clearInput();
};

function clearInput() {
  // Clear the text from the input field after sending
  textInput.value = "";
  // Focus back on the input field
  textInput.focus();
}

// Change to SCSS loop
function animateBotOutput() {
  chatList.lastElementChild.style.animationDelay = (animationBubbleDelay) + "ms";
  chatList.lastElementChild.style.animationPlayState = "running";
}

function saveImageToLocalStorage(imageData) {
  const imageHistory = JSON.parse(localStorage.getItem('imageHistory')) || [];
  imageHistory.push(imageData);
  localStorage.setItem('imageHistory', JSON.stringify(imageHistory));
}

function processImage(file) {
  // Показываем изображение, создавая элемент <img> и добавляя его в чат
  const imageItem = document.createElement("img");
  imageItem.classList.add("userInput");
  imageItem.src = URL.createObjectURL(file);
  chatList.appendChild(imageItem);
  fileInput.value = "";
  // Сбрасываем текст на кнопке прикрепления
  attachButton.textContent = 'Прикрепить изображение';

  saveImageToLocalStorage(imageItem.src);

  // Возвращаем поле для ввода к кликабельному состоянию после небольшой задержки
  setTimeout(function() {
    textInput.disabled = false;
  }, 100);

}

function loadImageHistoryFromStorage() {
  const imageHistory = JSON.parse(localStorage.getItem('imageHistory')) || [];

  imageHistory.forEach(function (imageSrc) {
    const imageItem = document.createElement("img");
    imageItem.classList.add("userInput");
    imageItem.src = imageSrc;
    chatList.appendChild(imageItem);
  });
}

// Вызовите функцию загрузки истории изображений при загрузке страницы
window.addEventListener('load', function () {
  loadImageHistoryFromStorage();
});

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    attachButton.textContent = file.name;
    // Делаем поле для ввода некликабельным
    textInput.disabled = true;
  } else {
    attachButton.textContent = 'Прикрепить изображение';
    // Возвращаем поле для ввода к кликабельному состоянию
    textInput.disabled = false;
  }
});

  function get_user_text() {
  $.ajax({
    type: "POST",
    url: "{{url_for('get_user_text')}}",
    data: {"user_text":textInput.value.toLowerCase()}

  })
}

  function get_bot_text() {
  $.ajax({
    type: "POST",
    url: "{{url_for('get_bot_text')}}",
    data: {"bot_text": $(".bot__output").last().text()}

  })
}

function send_bot_answer() {
    $.ajax({
      type: "GET",
      url: "{{url_for('send_bot_answer')}}",
      success: function(response) {
        console.log(response);
        window.GlobalVar = response;
      },
      error: function (error){
        console.log("Error sending... :(")
      }
    })
}


