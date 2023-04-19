import os

class Subject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        print("Im registered")
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, scores):
        print("I call notified")
        for observer in self.observers:
            print("I should be notified here")
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
            file.write("End-of-Game Scores\n\n")

    def update(self, scores):
        with open(self.filename, "a") as file:
            file.write("New Score: " + str(scores)+"\n")
            file.write("\n")