from flask import Flask, render_template
from time import sleep
import RPi.GPIO as GPIO
import accelerometer
import threading
import random

app = Flask(__name__, static_url_path="")

THRESHOLD_CUTREMUR = 10

alarm_time = 0

@app.route("/")
def render_index():
	return app.send_static_file("index.html")

@app.route("/getvalue")
def get_value():
	global alarm_time
	val = accelerometer.get_value()
	if val > THRESHOLD_CUTREMUR:
		alarm_time = 16
		print("Alarm")
	return str(val)


def alarm_thread_main():
	global alarm_time
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)
	while True:
		if alarm_time > 0:
			alarm_time -= 1
			if (alarm_time % 2) == 0:
				GPIO.output(8, GPIO.LOW)
			else:
				GPIO.output(8, GPIO.HIGH)
		else:
			GPIO.output(8, GPIO.HIGH)
		sleep(0.1)


if __name__ == "__main__":
	threading.Thread(target=alarm_thread_main).start()
	app.run(host="0.0.0.0", port=6969)