import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 180)	#скорость речи


def speaker(text):
	'''Озвучка текста'''
	engine.say(text)
	print(text)
	engine.runAndWait()