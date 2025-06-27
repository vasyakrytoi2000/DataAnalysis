class BinarySearchTreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def add_child(self, data):
        if data < self.data:
            if self.left:
                self.left.add_child(data)
            else:
                self.left = BinarySearchTreeNode(data)
        else:
            if self.right:
                self.right.add_child(data)
            else:
                self.right = BinarySearchTreeNode(data)


    def search(self, val):
        if self.data == val:
            return self.data

        if val < self.data:
            if self.left:
                return self.left.search(val)
            else:
                return False

        if val > self.data:
            if self.right:
                return self.right.search(val)
            else:
                return False

    def find_max(self):
        if self.right is None:
            return self.data
        return self.right.find_max()
    
    def print_tree(self, level=0, prefix="Root: "):
        print("    " * level + prefix + str(self.data))
        if self.left:
            self.left.print_tree(level + 1, prefix="L--- ")
        if self.right:
            self.right.print_tree(level + 1, prefix="R--- ")
    
def build_tree(elements):
    print("Building tree with these elements:",elements)
    root = BinarySearchTreeNode(elements[0])

    for i in range(1,len(elements)):
        root.add_child(elements[i])

    return root



if __name__ == '__main__':
    try:
        user_input = list(map(int, input("\033[1mEnter integer numbers separated by a space:\033[0m ").strip().split()))
        tree = build_tree(user_input)
        print("\n\033[1mYour Tree:\033[0m")
        tree.print_tree()
    except Exception as e:
        print(f"\033[31mInvalid input: {e}\033[0m")
        exit()

    while True:
        command = input("\n\033[1mEnter command:\033[0m ").strip().lower()
        try:
            match command:
                case "print":
                    print("\n\033[1mCurrent Tree:\033[0m")
                    tree.print_tree()

                case "max":
                    print(f"\033[1mMax element:\033[0m {tree.find_max()}")

                case "search":
                    val = int(input("\033[1mEnter value to search:\033[0m "))
                    result = tree.search(val)
                    if result == False:
                        print('\033[1melement does not exist\033[0m')
                    else:
                        print(f"\033[1mYour element exist:\033[0m {result}")

                case "add":
                    value = int(input("\033[1mEnter value to add:\033[0m "))
                    tree.add_child(value)
                    print(f"Element {value} added.")
                    tree.print_tree()

                case "help":
                    print("""Available commands:
\033[1m- print\033[0m       : Display the tree
\033[1m- max\033[0m    : Show the maximum element
\033[1m- search\033[0m      : Search element
\033[1m- add\033[0m         : Add new element
\033[1m- help\033[0m        : Show this help
\033[1m- exit\033[0m        : Exit 
""")

                case "exit":
                    print("Goodbye!")
                    break

                case _:
                    print("\033[31mUnknown command. Type 'help' to see available commands.\033[0m")
        except Exception as e:
            print(f"\033[31mError: {e}\033[0m")