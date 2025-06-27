class Queue:
    def __init__(self, len):
        self.len = len
        self.queue = [None] * len
        self.head = -1
        self.tail = -1

    def print(self):
        if self.head == -1:
            print('Queue is empty')
            return
        print('Queue items: ', end=' ')
        itr = self.head
        while True:
            print(self.queue[itr], end=' ')
            if itr == self.tail:
                break
            i = (i + 1) % self.len 
        print()

    def enqueue(self, item):
        if (self.tail + 1) % self.len == self.head:
            print('Queue is full')
            return
        elif self.head == -1:
            self.head = 0
            self.tail = 0
        else:
            self.tail = (self.tail + 1) % self.len
        self.queue[self.tail] = item

    def dequeue(self):
        if self.head == -1:
            print('Queue is empty')
            return
        elif self.head == self.tail:
            item = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return item
        else:
            item = self.queue[self.head]
            self.head = (self.head + 1) % self.len
            return item

    def get_instructions(self):
        print("""\033[1mHOW TO USE:\033[0m
              
              \033[1mprint\033[0m - print the current queue

              \033[1menqueue\033[0m - add item to queue

              \033[1mdequeue\033[0m - remove item from queue

              """
              )

if __name__ == '__main__':
    len = int(input("Enter size of queue: "))
    queue = Queue(len)

    while True:
        
        command = input("\n\033[1mEnter command:\033[0m ").strip().lower()

        match command:
            case "print":
                queue.print()
                
            case "enqueue":
                item = int(input("Enter item for add: "))
                queue.enqueue(item)
                queue.print()

            case "dequeue":
                item = queue.dequeue()
                if item is not None:
                    print(f"Removed item: {item}")
                queue.print()

            case "exit":
                print("Goodbye!")
                break
