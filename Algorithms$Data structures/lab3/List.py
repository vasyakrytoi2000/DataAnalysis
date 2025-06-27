import time
from functools import wraps
import tracemalloc
import sys
from pympler import asizeof
def gtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Time '{func.__name__}': {end - start:.6f} sec")
        return result
    return wrapper

def umemory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory use '{func.__name__}': {peak / 1024:.2f} KB")
        tracemalloc.stop()
        return result
    return wrapper

class TextEditor:
    def __init__(self):
        self.text = []  

    def print(self):
        if not self.text:
            print("The text is empty.")
        else:
            print(' '.join(self.text))

    @gtime
    @umemory
    def get_length(self):
        return len(self.text)

    @gtime
    @umemory
    def insert_at_beginning(self, word):
        self.text.insert(0, word)

    @gtime
    @umemory
    def insert_at_end(self, word):
        self.text.append(word)

    @gtime
    @umemory
    def insert_at(self, index, word):
        if index < 0 or index > len(self.text):
            print("Invalid index!")
        else:
            self.text.insert(index, word)

    @gtime
    @umemory
    def remove_at(self, index):
        if index < 0 or index >= len(self.text):
            print("Invalid index!")
        else:
            self.text.pop(index)

    @gtime
    @umemory
    def remove_by(self, value):
        if value in self.text:
            self.text.remove(value)
        else:
            print("Word not found!")

    def sys_memory(self):
        print(f"Memory size: {asizeof.asizeof(self.text)} bytes")


    @gtime
    @umemory
    def task(self):
        if not self.text:
            print("The text is empty.")
            return

        first_word = self.text[0]
        filtered_text = [first_word[:-1]] 

        for word in self.text[1:]:  
            if word != first_word and word.startswith('ab'):
                filtered_text.append(word[:-1])  

        self.text = [word + '.' for word in filtered_text]  


    def get_instructions(self):
        print("""\033[1mHOW TO USE:\033[0m
              \033[1mprint\033[0m - print the current text

              \033[1mget length\033[0m - get the current length of the text 

              \033[1madd begg\033[0m - add some text in begining

              \033[1madd end\033[0m - add some text in end

              \033[1madd in\033[0m - add some text in place you want
                       <index>, <some text>
                       <index> meaning example: <0> i <1> like <2> data <3> structures <4> and <5> algorithms <6>
              
              \033[1mremove at\033[0m - remove some word by index
                          <index>, <some word>
                          <index> meaning example: i like data structures and algorithms  
                                                  <0> <1>  <2>     <3>    <4>    <5>
              
              \033[1mremove by\033[0m - remove the word which you will enter, 
                                        \033[3mbut if you have few similar words it will remove the first in the text\033[0m
              """
              )

if __name__ == '__main__':
    editor = TextEditor()

    user_input = input("Enter your text: ").strip().split()
    editor.text = user_input

    editor.task()
    editor.print()

while True:
    command = input("\nEnter command: ").strip().lower()
    try:
        match command:
            case "print":
                editor.print()
                editor.sys_memory()
            case "get length":
                print(f"Length: {editor.get_length()}")
            case "add begg":
                word = input("Enter text to add at beginning: ")
                editor.insert_at_beginning(word)
                editor.print()
                editor.sys_memory()
            case "add end":
                word = input("Enter text to add at end: ")
                editor.insert_at_end(word)
                editor.print()
                editor.sys_memory()
            case "add in":               
                index = int(input("Enter index: "))
                word = input("Enter text to insert: ")
                editor.insert_at(index, word)            
                editor.print()
                editor.sys_memory()
            case "remove at":
                index = int(input("Enter index to remove: "))
                editor.remove_at(index)
                editor.print()
                editor.sys_memory()
            case "remove by":
                word = input("Enter word to remove: ")
                editor.remove_by(word)
                editor.print()
                editor.sys_memory()
            case "help":
                editor.get_instructions()
            case "exit":
                print("Goodbye!")
                break
            case _:
                print("Unknown command. Type 'help' to see the list of commands.")
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")