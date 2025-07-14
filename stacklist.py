
stack1 = [] # Create an empty list to represent the stack

stack1.append(10) 
stack1.append(20) 
stack1.append(30) 
print("Stack after pushes:", stack1) # Expected: [10, 20, 30]
    
# Peek at the top element (last element in list)
top_element = stack1[-1] # Access last element without removing it
print("Top element is:", top_element) # Expected: 30
if len(stack1) == 0:
    print("Stack is empty")
else:
    print("Stack is not empty") # Expected here

class SimpleStack:
    def __init__(self):
            
        self.items = []#Initialize an empty list to hold stack elements 
    def is_empty(self):
        #Initialize an empty list to hold stack elements     
        return len(self.items) == 0#add item to the top of the stack 
    def push(self, item):
        self.items.append(item)
 # remove an item from the top and return it
     
    def pop(self): # if stack is empty return an error to avoid an invalid operation    
     if self.is_empty():
         raise Exception("Cannot pop an empty stack")
     return self.items.pop()
    
     
    def peek(self):#Raise an error is stack is Empty
     if self.is_empty():
         raise Exception("STACK IS EMPTY")

     return self.items[-1]

 #SIZE: Return the number of all the items in the stack
    def size(self):
     return len(self.items)
    
    def printstack(self):# Print all items in the stack from bottom to top
     print("Stack from bottom to top:", self.items)
     return
    
     
if __name__ == "__main__":
 #instantiate the class stack by creating an object for it.    
    stack1 = SimpleStack()

 #Then, push some elements
    stack1.push(1000)
    stack1.push(2000)
    stack1.push(3000)
    
     #print the elements
    stack1.printstack()
    
     # Peek top element
    print("Top element:", stack1.peek()) # Expected: 3000
    
     
    print("Popped:", stack1.pop()) # Expected: 3000
    stack1.printstack() # Expected: [100, 200]
    
    
    print("Is stack empty?", stack1.is_empty()) # Expected: False
    
     # Pop all to empty
    stack1.pop()
    stack1.pop()
    print("Is stack empty after popping all?", stack1.is_empty()) 