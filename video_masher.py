import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips


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
def fisheye(frame, center_x, center_y, radius, strength=0.001):
    height, width = frame.shape[:2]

    # Create a grid of coordinates
    X, Y = np.meshgrid(np.arange(width), np.arange(height))

    # Calculate distances from center
    distance_from_center = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)

    # Apply distortion only within the circular area
    within_circle = distance_from_center <= radius

    # Normalize coordinates to range [-1, 1] within circular area
    X_normalized = ((X[within_circle] - center_x) / radius)
    Y_normalized = ((Y[within_circle] - center_y) / radius)

    # Calculate radial distance from center within circular area
    r = np.sqrt(X_normalized ** 2 + Y_normalized ** 2)

    # Apply modified fisheye distortion equation
    r = np.clip(r, 0, 1)  # Clip the radial distance to [0, 1]
    r = r * (1 + (strength + 1) * r ** 2)

    # Map distorted coordinates back to frame coordinates within circular area
    X_distorted = (center_x + X_normalized * r * radius).astype(np.int32)
    Y_distorted = (center_y + Y_normalized * r * radius).astype(np.int32)

    # Copy original frame to keep the parts outside the circular area unchanged
    distorted_frame = np.copy(frame)

    # Update distorted circular area in the frame
    distorted_frame[within_circle] = frame[Y_distorted, X_distorted]

    return distorted_frame
# Загрузка видео
filename = 'IMG_3409.mp4'
video_capture = cv2.VideoCapture(filename)
out = cv2.VideoWriter(f'mute{filename}', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))
video_clip = VideoFileClip(filename)
#аудиодорожку воруем
audio_clip = video_clip.audio


while True:
    # Чтение кадра из видео
    ret, frame = video_capture.read()

    if not ret:
        break

    # Обнаружение глаз на кадре
    eyes_coords = detect_eyes(frame)
    print(eyes_coords)
    # Отображение кругов вокруг обнаруженных глаз
    #for (x, y) in eyes_coords:
        #cv2.circle(frame, (x, y), 30, (0, 255, 0), 2)
    try:
        for i in range(len(eyes_coords)):
            frame = fisheye(frame, eyes_coords[i][0], eyes_coords[i][1], 30, strength=0.8)
    except Exception:
        pass
    # Отображение обработанного кадра

    cv2.imshow('Video', frame)
    out.write(frame)


    # Выход из цикла при нажатии на клавишу 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка ресурсов
video_capture.release()
cv2.destroyAllWindows()
out.release()

# к которому дорожку делаем
video_clip2 = VideoFileClip(f"mute{filename}")

# Добавляем аудиодорожку к другому видео
video_clip_with_audio = video_clip2.set_audio(audio_clip)

# Сохраняем новое видео с аудиодорожкой
video_clip_with_audio.write_videofile(f"sound_{filename}", codec='libx264')
video_clip.reader.close()
audio_clip.reader.close_proc()
video_clip2.reader.close()