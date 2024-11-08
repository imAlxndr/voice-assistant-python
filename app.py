from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk
import json
import queue
import words
from skills import *
import voice


q = queue.Queue() # Очереь из данных

model = vosk.Model('model_small') # Модель Vosk

device = sd.default.device # Микрофон и динамик по умолчанию

samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # Получаем частоту микрофона


def callback(indata, frames, time, status):
    q.put(bytes(indata)) # Добавляем в очередь семплы из потока


def recognize(data, vectorizer, clf):
    name = words.bot_name.intersection(data.split()) # Проверяем есть ли имя бота в data, если нет, то return
    if not name: # Если нет совпадений по имени, то ждем, пока появится имя бота
        return

    data.replace(list(name)[0], '') # удаляем имя бота из текста

    text_vector = vectorizer.transform([data]).toarray()[0] # получаем вектор полученного текста
    answer = clf.predict([text_vector])[0] # сравниваем с вариантами, получая наиболее подходящий ответ

    func_name = answer.split()[0] # получение имени функции из ответа из data_set

    voice.speaker(answer.replace(func_name, ''))  # озвучка ответа из модели data_set

    exec(func_name + '()') # запуск функции из skills


def main():
    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys())) # Получаем список ключей из словаря датасета
    
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values())) # Получаем список значений из словаря датасета

    del words.data_set # Удаляем из ОЗУ словарь датасета

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get() # Получаем поступившие данные
            if rec.AcceptWaveform(data): # Если наступила пауза (перестал говорить)
                data = json.loads(rec.Result())['text'] # Полученная фраза
                print(data)
                recognize(data, vectorizer, clf)


if __name__ == '__main__':
    main()

