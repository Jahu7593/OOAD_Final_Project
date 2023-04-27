import os
# used a little help from Geeks for Geeks and Stack overflow to help form the obeserver patern into python.
#even used a little help from ChatGPT, to change some of our code from FNCD obserever from java into python then
#tweeked that code to work with our flappy bird game.

class Subject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        # print("Im registered")
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, scores):
        # print("I call notified")
        for observer in self.observers:
            # print("I should be notified here")
            observer.update(scores)

class Observer:
    def update(self, scores):
        pass

class FileWriter(Observer):
    def __init__(self):
        self.filename = "scores.txt"
        self.create_file()

    def create_file(self):
        with open(self.filename, "w") as file:
            file.write("High Scores\n\n")

    def update(self, scores):
        with open(self.filename, "a") as file:
            file.write("New High Score: " + str(scores)+"\n")
            file.write("\n")