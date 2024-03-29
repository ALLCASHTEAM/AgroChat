import cv2

# Загрузка каскада Хаара для обнаружения глаз
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Функция для обнаружения и возвращения координат глаз
def detect_eyes(frame):
    # Поиск глаз на кадре
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Список для хранения координат глаз
    eyes_coords = []

    # Добавляем координаты глаз в список
    for (ex, ey, ew, eh) in eyes:
        eyes_coords.append((ex + ew // 2, ey + eh // 2))

    return eyes_coords

# Загрузка видео
video_capture = cv2.VideoCapture('C:\\Users\\User\\Downloads\\VideoForTune.mp4')

while True:
    # Чтение кадра из видео
    ret, frame = video_capture.read()

    if not ret:
        break

    # Обнаружение глаз на кадре
    eyes_coords = detect_eyes(frame)

    # Отображение кругов вокруг обнаруженных глаз
    for (x, y) in eyes_coords:
        cv2.circle(frame, (x, y), 30, (0, 255, 0), 2)

    # Отображение обработанного кадра
    cv2.imshow('Video', frame)

    # Выход из цикла при нажатии на клавишу 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка ресурсов
video_capture.release()
cv2.destroyAllWindows()
