var sendForm = document.querySelector('#chatform');
    textInput = document.querySelector('.chatbox');
    chatList = document.querySelector('.chatlist');
    fileInput = document.getElementById("upload");
    animationCounter = 1;
    animationBubbleDelay = 600;
    attachButton = document.querySelector('.attach-button');

function scrollToBottom() {
  chatList.scrollTop = chatList.scrollHeight;
}

sendForm.onkeydown = function(e) {
  if (e.keyCode == 13) {
    e.preventDefault();

    // No mix ups with upper and lowercases
    var input = textInput.value.toLowerCase();

    // Empty textarea fix
    if (input.length > 0) {
      createBubble(input);
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
    alert("You can't send both text and an image. Please choose only one.");
    // Удаляем файл из поля для выбора
    fileInput.value = "";
    // Возвращаем поле для ввода к доступному состоянию
    textInput.disabled = false;
    attachButton.textContent = 'Attach Image';
    return;
  } else if (input.length > 0) {
    // Обрабатываем текстовое сообщение
    createBubble(input);
  } else if (file) {
    // Обрабатываем изображение
    processImage(file);
  } else {
    alert("Please enter a message or choose an image.");
  }
});

var createBubble = function(input) {
  // Create input bubble
  var chatBubble = document.createElement('li');
  chatBubble.classList.add('userInput');

  // Add input of textarea to chatbubble list item
  chatBubble.innerHTML = input;

  // Add chatBubble to chatlist
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

// Change to SCSS loop
function animateBotOutput() {
  chatList.lastElementChild.style.animationDelay = (animationCounter * animationBubbleDelay) + "ms";
  animationCounter++;
  chatList.lastElementChild.style.animationPlayState = "running";
}

function processImage(file) {
  // Показываем изображение, создавая элемент <img> и добавляя его в чат
  const imageItem = document.createElement("img");
  imageItem.classList.add("userInput");
  imageItem.src = URL.createObjectURL(file);
  chatList.appendChild(imageItem);
  fileInput.value = "";
  // Сбрасываем текст на кнопке прикрепления
  attachButton.textContent = 'Attach Image';

  // Возвращаем поле для ввода к кликабельному состоянию после небольшой задержки
  setTimeout(function() {
    textInput.disabled = false;
  }, 100);
}

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    attachButton.textContent = file.name;
    // Делаем поле для ввода некликабельным
    textInput.disabled = true;
  } else {
    attachButton.textContent = 'Attach Image';
    // Возвращаем поле для ввода к кликабельному состоянию
    textInput.disabled = false;
  }
});