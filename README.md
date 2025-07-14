[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/b9hrDlfp)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19548894&assignment_repo_type=AssignmentRepo)
# ASSIGNMENTS-ICS-GROUP-D-2025
ASSIGNMENTS FOR ICS GROUP D

## IN YOUR IDE, CREATE A PYTHON FILE (implementation file) AND NAME IT  `circular_dll.py`
### GO THROUGH THIS FILE LINE BY LINE & THEN TYPE THE CODE PROVIDED IN YOUR IDE, AFTER WHICH YOU WILL PUSH THE CHANGES TO THIS REPOSITORY FOR MARKING
___


# Circular Doubly Linked List in Python

### We saw How to implement a singly linked list and to further our understanding, this markdown file will aid you to understand **Circular & Doubly Linked List (CDLL)** 
#### I've generously sprinkled comments all over the code, not because I like typing extra, but because future-you (and your sanity) will thank you during debugging, they are your scrolls of wisdom, to aid you understand every line of code as you **T Y P E !!**  the code in your IDE, because *Clarity is king and confusion is expensive.*
---

# TYPE THE CODE AS PROVIDED
___
### First we Define a Node class to represent each element in the circular doubly linked list

```python

class CircularListNode:
    def __init__(self, value):
        # Here we Store the actual data or value in this node
        self.value = value
        
        # 'next_node', is an attribute of type pointer that will point to the next node in the list
        # Initially, when the node is created, we don't know the next node, so we set it to None, or null
        self.next_node = None
        
        # Will also have 'previous_node', which is an attribute that  will point to the previous node in the list
        # Initially, we set to None since Llist uis empty at this point
        self.previous_node = None

````
### Define the Circular Doubly Linked List class to manage nodes and operations

```python
class CircularDoublyLinkedList:
    def __init__(self):
        #We need to tell the compiler about the first chainlink, or the first node of our LList whis is the head
        #Here in this code,  The 'start_node', attribute will be our head and it will keep track of the first node in the list (the head)
        # If the list is empty, 'start_node' will be None
        self.start_node = None
```
# OOP METHODS TO MANIPULATE OUR LINKED LIST
## i) _Insert at End_
_This method will Insert a new node with the given 'value' at the end of the circular doubly linked list._

```python
      def insert_at_end(self, value):
        # First,  Create a new node object with the given value
        new_node = CircularListNode(value)

        # Secondly, Check if our Llist is empty, where it is fulfilled by this condition: (start_node is None)
        if self.start_node is None:
            #We only enter this block if the LList is empty
            # Since the list is empty, this new node will be the only node in our list
            # Then, For a circular list, this node points to itself in both directions
            new_node.next_node = new_node  # The next node after new_node is itself
            new_node.previous_node = new_node  # The previous node before new_node is itself

            # We also need to Update the start_node pointer to this new node
            self.start_node = new_node

        else:
            # Her in the else clause, the list has contents,
            # So, The list is not empty, thus we need to add the new node at the end

            # 'last_node' is the node that currently comes before the start_node,
            #Remember to Keep in mind that this is a Circularly, Doubly Linked list.
            # We access it by following the 'previous_node' pointer of the start_node
            
# Now we have a special concept called chained attribute access or attribute chaining.
            
            # Here it is : 'self.start_node.previous_node' means:
            #   - 'self.start_node' gives us the first node in the list
            #   - '.previous_node' accesses the node that comes before the start_node
            
            #In context:
#You're navigating object references through chained attributes — essentially, following links (pointers) between objects.

#In data structures (like linked lists), this is also described as:
    # 1.Pointer traversal in object-oriented programming.

    #2. Link following in node-based structures.

# So, self.start_node.previous_node is an example of pointer traversal via attribute chaining in a linked structure.
            
            # This works because the list is circular, so the node before the first node is the last node
            last_node = self.start_node.previous_node

            # Now we link the new_node into the list:

            # First,  The current last_node's 'next_node' should point to the new_node
            last_node.next_node = new_node

            # Secondly, The new_node's 'previous_node' should point back to the last_node
            new_node.previous_node = last_node

            # Thirdly,  The new_node's 'next_node' should point to the start_node to maintain circularity
            new_node.next_node = self.start_node

            # lastly, The start_node's 'previous_node' should now point back to the new_node, which is the new last node
            self.start_node.previous_node = new_node
```

---

### _ii)_  _Inserting  at Beginning_
_Here we will Insert a new node with the given 'value' (passed as a parameter)at the beginning of the circular doubly linked list._
```python
    def insert_at_beginning(self, value):
    
        #To optimize our code, We are going reuse the insert_at_end method to add the node at the end first
        
        self.insert_at_end(value)

        # After adding the new node at the end, we move the start_node pointer backward to the new node
        # Here is the mark down;
        # - 'self.start_node' is currently the first node
        # - 'self.start_node.previous_node' is the node just added at the end
        # By setting start_node to start_node.previous_node, we simply make the new node the first node
        self.start_node = self.start_node.previous_node
```

### _iii)_ _Remove A given Value from the Linked List_

_Remove the first node found with the specified value._

```python
    def remove_by_value(self, value):
        # If the list is empty, then ofcourse, there is nothing to remove
        if self.start_node is None:
            print("The list is empty. Cannot remove any node.")
            return

        # If not, We start by searching from the start_node
        current_node = self.start_node

        # We will iterate through the LList until we come back to the start_node, since it's circularly linked list
        while True:
            if current_node.value == value:
                
                # We only enter this block if we find the node to remove

                #After finding the node to remove, there are a few cases we need to consider, 
                
                # the first case is that the list has only one node (which is current_node)
                if current_node.next_node == current_node:
                    # Since it's the only node, removing it makes the list empty
                    self.start_node = None

                else:
                    # The second case, is that The list has multiple nodes

                    # So, inorder to remove current_node, we need to announce our intentions to our neighbours, 
                    # by updating the links of these neighbours
                    
                    # Remember the pointer traversal via attribute chaining, in as that 'current_node.previous_node.next_node = current_node.next_node' which basically implies, 
                    #-The node before current_node should now point forward to the node after current_node
                    current_node.previous_node.next_node = current_node.next_node

                    # 'current_node.next_node.previous_node = current_node.previous_node' Implies that,
                    #   - The node after current_node should now point backward to the node before current_node
                    current_node.next_node.previous_node = current_node.previous_node

                    # If we are removing the start_node, move the start_node pointer forward
                    if current_node == self.start_node:
                        self.start_node = current_node.next_node

                # By this point, the Node is removed, and we can peacefully exit the method
                return

            # Move to the next node in the list
            current_node = current_node.next_node

            # If we by any chance have managed looped back to the start_node, the value was not found
            if current_node == self.start_node:
                print(f" Value {value} not found in the list.")
                break

```
### _iv)_ _Show List Forward wise_
_Display the values of the nodes in the list starting from the start_node and moving forward._

```python
       def show_list_forward(self):

        # We start by checking if the list is empty, and if so, print a message and exit the method using return
        if self.start_node is None:
            print("The list is empty.")
            return

        # Set a temporary attribute to aid us loop by assigning it to the start_node
        current_node = self.start_node

        # Then we Create an empty list to collect/ gather the string representations (which means we convert the sata part of the node to string) of node values
        values_list = []

        # Traverse through the LList until we come back to the start_node
        while True:
            # Add the current node's value to the list as a string
            values_list.append(str(current_node.value)) #Here str() is an inbuilt method that converts a given value to a string

            # Then we do our incrementation here by utilizing the pointers
            current_node = current_node.next_node
            
            #We then check a condition where we have completed a full circle, and if so, we MAKE A STOP
            if current_node == self.start_node:
                break
        
                ##We can Format output, but it's not a must, however We shall do it otherwise, because, why not?
                
        #Here's how to do it, We Join all the values in 'values_list' into a single string separated by ' -> '
        
        # Explanation of join inbuilt method:
        # - ' -> ' is a string separator
        # - '.join(values_list)' takes all elements in 'values_list' and concatenates them into one string,
        #   putting ' -> ' between each element
        # For example, if values_list = ['5', '10', '15'], the result will be '5 -> 10 -> 15'
        output_string = " -> ".join(values_list)

        # Print the resulting string to show the list contents
        print(output_string)
```
## _iv) _Showing List Backward_
_Here, we attempt to display the values of the nodes in the list starting from the last node and moving backward._
```python
       def show_list_backward(self):

        # If the list is empty, print a message and exit the method via (return)
        if self.start_node is None:
            print("The list is empty.")
            return

        # Here, the last node is the one before the start_node (because the list is circular)
        last_node = self.start_node.previous_node
# If you are wondering why not store a  self.last_node separately 
        # It's because it adds redundancy and risks de-synchronization, 
        # Instead,  we just access what we need through the links.
        
        # Now for the printing part, Start from the last node
        current_node = last_node

        # Create an empty list to collect the string representations of node values
        values_list = []

        # Traverse the list backward until we come back to the last_node
        while True:
            # Add the current node's value to the list as a string
            values_list.append(str(current_node.value))

            # Move to the previous node
            current_node = current_node.previous_node

            # Stop if we have completed a full circle
            if current_node == last_node:
                break

        # Join all the values in 'values_list' into a single string separated by ' <- '
        # - ' <- ' is our separator that now indicates backward direction
        # - '.join(values_list)' concatenates all elements in 'values_list' with ' <- ' between them
        # e.g  if values_list = ['30', '20', '10'], the result will be '30 <- 20 <- 10'
        
        output_string = " <- ".join(values_list)

        # Print the resulting string to show the list contents backward
        print(output_string)

```



### First we prepped the ingredients and cooked the meal in the class definition, now it’s time to taste it!  inside the (_main_) block

```python
if __name__ == "__main__":
    #Create a node by Instantiating that class via the creating of an object
    my_circular_list = CircularDoublyLinkedList()

    #Then insert values by calling the insertion method we created
    my_circular_list.insert_at_end("QUICK")
    my_circular_list.insert_at_end("BROWN")
    my_circular_list.insert_at_end("FOX")

    print("List after inserting at the end:")
    #Call the print forward method
    my_circular_list.show_list_forward() 

    my_circular_list.insert_at_beginning("THE")
    print("List after inserting at the beginning:")
    my_circular_list.show_list_forward()  

    print("List displayed backward:")
    my_circular_list.show_list_backward() 

    my_circular_list.remove_by_value("QUICK")
    print("List after removing QUICK:")
    my_circular_list.show_list_forward()

    my_circular_list.remove_by_value("QUICK")  # Not found
    my_circular_list.remove_by_value("SLOW")  # Not found

    my_circular_list.remove_by_value("BROWN")
    print("List after removing BROWN:")
    my_circular_list.show_list_forward() 

    # Attempting to empty the LList by removing the remining elements
    my_circular_list.remove_by_value("THE")
    my_circular_list.remove_by_value("FOX")
    print("List after removing all:")
    
    my_circular_list.show_list_forward()
```

## *NOTE BETTER*

* A **circular** doubly linked list ensures the last node links back to the first, and vice versa.


