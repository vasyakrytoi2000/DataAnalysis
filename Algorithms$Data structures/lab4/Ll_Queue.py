class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None  

    def print(self):
        if self.head is None:
            print("Queue is empty")
            return
        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data) + ' ' if itr.next else str(itr.data)
            itr = itr.next
        print(llstr)

    def enqueue(self, data):
        node = Node(data)
        if self.tail is None:  
            self.head = self.tail = node
            return
        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def dequeue(self):
        if self.head is None:
            print("Queue is empty")
            return
        item = self.head.data
        self.head = self.head.next
        if self.head:  
            self.head.prev = None
        else:  
            self.tail = None
        return item



if __name__ == '__main__':
    
    ll= LinkedList()

    while True:
        
        command = input("\n\033[1mEnter command:\033[0m ").strip().lower()

        match command:
            case "print":
                ll.print()
                
            case "enqueue":
                item = int(input("Enter item for add: "))
                ll.enqueue(item)
                ll.print()

            case "dequeue":
                item = ll.dequeue()
                if item is not None:
                    print(f"Removed item: {item}")
                ll.print()

            case "exit":
                print("Goodbye!")
                break