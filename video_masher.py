import cv2

# Загрузка каскада Хаара для обнаружения лиц и глаз
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Функция для обнаружения и возвращения координат лица и глаз
def detect_face_and_eyes(frame):
    # Поиск лиц на кадре
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Список для хранения координат лиц и глаз
    face_and_eyes_coords = []

    # Находим глаза на каждом обнаруженном лице
    for (x, y, w, h) in faces:
        # Добавляем координаты лица в список
        face_and_eyes_coords.append((x, y, x + w, y + h))

        # Определение области интереса для лица
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Поиск глаз на лице
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Добавляем координаты глаза в список
            face_and_eyes_coords.append((x + ex, y + ey, x + ex + ew, y + ey + eh))

    return face_and_eyes_coords

# Загрузка видео
video_capture = cv2.VideoCapture('C:\\Users\\User\\Downloads\\VideoForTune.mp4')

while True:
    # Чтение кадра из видео
    ret, frame = video_capture.read()

    if not ret:
        break

    # Обнаружение лиц и глаз на кадре
    face_and_eyes_coords = detect_face_and_eyes(frame)

    # Отображение прямоугольников вокруг обнаруженных лиц и глаз
    for (x1, y1, x2, y2) in face_and_eyes_coords:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Отображение обработанного кадра
    cv2.imshow('Video', frame)

    # Выход из цикла при нажатии на клавишу 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка ресурсов
video_capture.release()
cv2.destroyAllWindows()
