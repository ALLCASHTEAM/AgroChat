document.querySelector('.question-mark-btn').addEventListener('click', function() {
    var menuContent = document.querySelector('.menu-content');
    if (menuContent.style.display === 'block') {
        menuContent.style.display = 'none';
    } else {
        menuContent.style.display = 'block';
    }
});

// Закрывать меню, если пользователь кликнул вне него
window.addEventListener('click', function(event) {
    var menuContent = document.querySelector('.menu-content');
    if (event.target !== menuContent && event.target !== document.querySelector('.question-mark-btn')) {
        menuContent.style.display = 'none';
    }
});

// Выбираем кнопку  (переключение темы)
const btn = document.querySelector(".dark-theme");
// Выбираем таблицу стилей
const theme = document.querySelector("#theme-link");
// Отслеживаем щелчок по кнопке
btn.addEventListener("click", function() {
  // Если текущий адрес содержит "light-theme.css"
  if (theme.getAttribute("href") == "light-zhopa.css") {
    // …то переключаемся на "dark-theme.css"
    theme.href = "dark-zhopa.css";
    // В противном случае… 
  } else {
    // …переключаемся на "light-theme.css"
    theme.href = "light-zhopa.css";
  }
});