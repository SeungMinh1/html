#-*- coding: utf-8 -*-
"""
파일명 : dht11.py
작성자 : 
작성일자 : 2022-11-30
수정사항 : *
제공기능 : 라즈베리파이의 GPIO를 이용한 dht11 온습도센서 값 출력
"""

import RPi.GPIO as GPIO
import time

DHT11_PIN = 36
DEBUG_PIN = 38

class DHT11 :
    def __init__(self) :
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(DHT11_PIN, GPIO.OUT)
        GPIO.setup(DEBUG_PIN, GPIO.OUT)

    def read(self):
        GPIO.setup(DHT11_PIN, GPIO.OUT)
        GPIO.output(DHT11_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(DHT11_PIN, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(DHT11_PIN, GPIO.HIGH)

        count = 0
        while count < 35:
            count += 1
        GPIO.setup(DHT11_PIN, GPIO.IN)
        while GPIO.input(DHT11_PIN) == GPIO.LOW:
            break
        while GPIO.input(DHT11_PIN) == GPIO.HIGH:
            break
        while GPIO.input(DHT11_PIN) == GPIO.LOW:
            break

        data = [0, 0, 0, 0, 0] # 5 x 8 = 40bit data 
        count = 0 # bit count
        while count <= 40: 
            i = 0
            while GPIO.input(DHT11_PIN) == GPIO.LOW:
                i += 1
            while GPIO.input(DHT11_PIN) == GPIO.HIGH:
                i += 1
            if (count > 0):
                GPIO.output(DEBUG_PIN, 1)
                GPIO.output(DEBUG_PIN, 0)
                data[int ((count - 1) / 8)] <<= 1
            if i > 37: # if duration is more than 76us
                data[int ((count - 1) / 8)] |= 1 
            count += 1

        #print(data)
        if ((data[0] + data[1] + data[2] + data[3]) % 256 == data[4]):
            relative_humidity = (data[0] + data[1]) * 0.1
            temp = data[2]
            if (data[3] & 0x80):
                temp = -1 - temp
            temp += (data[3] &0x0F) * 0.1 
            return relative_humidity, temp
        else:
            #print("checksum error")
            return None

if __name__ == "__main__":
    dht11 = DHT11()
    while True:
        result = dht11.read()
        if result == None :
            print("checksum error")
        else :
            print("rel_hum = {:5.1f}%, temp = {:5.1f} deg".format(result[0], result[1])) #습도, 온도 출력
        time.sleep(1) # sleep 1 sec