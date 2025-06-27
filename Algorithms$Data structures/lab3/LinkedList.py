import time
from functools import wraps
import tracemalloc
from pympler import asizeof

class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.head = None

    def print(self):
        if self.head is None:
            print("Linked list is empty")
            return
        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data) + ' ' if itr.next else str(itr.data)
            itr = itr.next
        print(llstr)

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count += 1
            itr = itr.next
        return count

    def insert_at_begining(self, data):
        node = Node(data, self.head)
        if self.head:
            self.head.prev = node
        self.head = node

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data)
            return
        itr = self.head
        while itr.next:
            itr = itr.next
        node = Node(data, None, itr)
        itr.next = node

    def insert_at(self, index, data):
        if index < 0 or index > self.get_length():
            raise Exception("Invalid Index")
        if index == 0:
            self.insert_at_begining(data)
            return
        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                node = Node(data, itr.next, itr)
                if itr.next:
                    itr.next.prev = node
                itr.next = node
                break
            itr = itr.next
            count += 1

    def remove_at(self, index):
        if index < 0 or index >= self.get_length():
            raise Exception("Invalid Index")
        if index == 0:
            if self.head.next:
                self.head.next.prev = None
            self.head = self.head.next
            return
        count = 0
        itr = self.head
        while itr:
            if count == index - 1 and itr.next:
                to_remove = itr.next
                itr.next = to_remove.next
                if to_remove.next:
                    to_remove.next.prev = itr
                break
            itr = itr.next
            count += 1

    def remove_by_value(self, value):
        if self.head is None:
            return
        if self.head.data == value:
            if self.head.next:
                self.head.next.prev = None
            self.head = self.head.next
            return
        itr = self.head
        while itr:
            if itr.data == value:
                if itr.prev:
                    itr.prev.next = itr.next
                if itr.next:
                    itr.next.prev = itr.prev
                return
            itr = itr.next

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def task(self):
        if self.head is None:
            return

        first_word = self.head.data
        result = []

        itr = self.head
        while itr:
            word = itr.data
            if itr == self.head or (word != first_word and word.lower().startswith("ab")):
                modified = word[:-1] if len(word) > 1 else ''
                modified += '.'
                result.append(modified)
            itr = itr.next

        self.insert_values(result)

    def measure_and_run(self, func, *args, **kwargs):
        import time, tracemalloc
        tracemalloc.start()
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Time '{func.__name__}': {end - start:.6f} sec")
        print(f"Memory use '{func.__name__}': {peak / 1024:.2f} KB")
        return result
    
    def mem_size(self):
        print(f"LinkedList memory size: {asizeof.asizeof(self)} bytes")

        
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
    ll = LinkedList()
    user_input = input("Enter your text: ").strip().split()
    ll.measure_and_run(ll.insert_values, user_input)
    ll.measure_and_run(ll.task)
    ll.print()



while True:
    command = input("\n\033[1mEnter command:\033[0m ").strip().lower()

    try:
        match command:
            case "print":
                ll.print()
                ll.mem_size()

            case "get length":
                print(f"Length: {ll.measure_and_run(ll.get_length())}")

            case "add begg":
                text = input("Enter text to add at beginning: ")
                ll.measure_and_run(ll.insert_at_begining, text)
                ll.print()

            case "add end":
                text = input("Enter text to add at end: ")
                ll.measure_and_run(ll.insert_at_end, text)
                ll.print()

            case "add in":
                index = int(input("Enter index: "))
                text = input("Enter text to insert: ")
                ll.measure_and_run(ll.insert_at, index, text)
                ll.print()

            case "remove at":
                index = int(input("Enter index to remove: "))
                ll.measure_and_run(ll.remove_at, index)
                ll.print()

            case "remove by":
                value = input("Enter word to remove: ")
                ll.measure_and_run(ll.remove_by_value, value)
                ll.print()

            case "help":
                ll.get_instructions()

            case "exit":
                print("Goodbye!")
                break

            case _:
                print("\033[31mUnknown command. Type 'help' to see the list of commands.\033[0m")
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")

