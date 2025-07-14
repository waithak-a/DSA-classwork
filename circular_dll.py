class CircularListNode:
    def __init__(self, value):
        self.value = value #here we store the actual data or value inthis node
        
        self.next_node = None # 'next_node, is an attribute of type pointer that will point to the next node in the list
                              #when the node is created, we don't know the next node so its set to none
                          
        self.previous_node = None #This attribute that will point to the previous node in the list 
                                #the list is empty as its set to none

class CircularDoublyLinkedList:###manages nodes and operations
    def __init__(self): #the 'start_node' attribute will be the head and it will keep track of the first node in the list
            self.start_node =None #start_node is none because the list is empty

    def insert_at_end(self, value):
        new_node = CircularListNode(value) #creates a new node object with a given value
        if self.start_node is None: #checks if the lists are empty, where its is fulfilled by this condition:(start_node is none)
            new_node.next_node = new_node #for a circular list, the next node of the new node points to itself
            new_node.previous_node = new_node #the previous node before new_node is itself
                
            self.start_node = new_node #Update of the start_node pointer to this new node
        else:
            last_node = self.start_node.previous_node #the list is circular, so the node before the first node is the last node
                
                # the current last_node's 'next_node' should point the new node
            last_node.next_node = new_node 
                #the new_node's 'previous_node' should point back to the last node
                
            new_node.previous_node = last_node 
                #the new_node's 'next_node' should point to the start_node to maintain circularity
                
            new_node.next_node = self.start_node 
                #th start_node's 'previous_node' should now point back to the new_node, which is the new last node
            self.start_node.previous_node = new_node
                
                #Inserting at the beginning
                #A new node wtih the given 'value' (passed as a parameter)at the beginning of the circular doubly linked list
                
    def insert_at_beginning(self,value):
                    #for optimization, reuse of the insert_at_end method will take place to add the node at the end first
                    
            self.insert_at_end(value)
                    
                    #by setting start_node to start_node.previous_node, we simply make the new node the first node
            self.start_node = self.start_node.previous_node
                    
                    ###_ _remove a given value from the linked list
         
    def remove_by_value(self, value):#if the list is empty, then there is nothing to remove
        if self.start_node is None:
            print("The list is empty. cannot remove any node.") 
            return #Otherwise, we start searching from the start node
                   
        current_node = self.start_node
                   
        while True:
             if current_node.value == value:
                #we only enter this block if we find the node to remove
                #cases to consider: 1st-> when the node has only one node (which is current_node)
                  if current_node.next_node == current_node:
                     self.start_node = None
              
                  else:
                    #2nd -> when there are multiple nodes but first the intentions of the neighbours need to be announced by updating the links of these neighbours
                      current_node.previous_node.next_node = current_node.next_node #implies that the node after current_node should now point backward to the node before current_node
                      current_node.next_node.previous_node = current_node.previous_node
                                  
                      if current_node == self.start_node:#If we are removing the start_node, move the start_node pointer forward
                          self.start_node = current_node.next_node
                          return
            #moving to the next node in the list
             current_node = current_node.next_node
            
             if current_node == self.start_node: #if we by any chance have managed looped back to the start_node, the value was not found 
                print(f"Value {value} not found in the list.")
                break
            
            #Dispalys the values of the nodes in the list starting from the start_node and moving forward
            
    def show_list_forward(self):# start by checking if the list is empty, and if so, print a message and exit the method using return
        if self.start_node is None:
            print("The list is empty.")
            return
         
         #temporary attribute to aid in loop by assigning it to the start_node
        current_node = self.start_node
         #creation of an empty list to collect/ gather the string representations(which means we convert the data part of the node to string ) of node values
        values_list = []
         
        while True: #traverse through the list until we come back to the start_node
             values_list.append(str(current_node.value))#add the current  node's value to the list as a string
             current_node = current_node.next_node #incrementation here by  utilizing the pointers
            
             if current_node == self.start_node:# checking a condition where we have completed a full circle, and if so, we MAKE A STOP
                 break
        output_string = " -> " .join(values_list) + "->(head)"
        print(output_string) #resulting string to show the list contents
             
             #showing the list backwards
    def show_list_backward(self):
        if self.start_node is None:
            print("The list is empty.")
            return
            
        last_node = self.start_node.previous_node#last_node is the one before the start node
            
        current_node = last_node #start from the last node
        values_list = [] # Create an empty list to collect the string representations of node values
        while True:
            values_list.append(str(current_node.value))#add the current node's value to the list as a string
                
            current_node = current_node.previous_node#mov eto the previous node
                #stop if the program has completed a full circle
            if current_node == last_node: 
                    break
        output_string = " <- ".join(values_list) +"<-(tail)"
        #joins all the values in 'values_list' and tail into a singular string
                
        print(output_string)
                
                #test
if __name__ == "__main__":
    #Create a node by instantiating that class via the creation of an object
    my_circular_list = CircularDoublyLinkedList()
    #insert value by calling the insertion metod created
    my_circular_list.insert_at_end(10)
    my_circular_list.insert_at_end(20)
    my_circular_list.insert_at_end(30)
    
    print("List after inserting at the end:")
    my_circular_list.show_list_forward()
    
    my_circular_list.insert_at_beginning(5)
    print("List after inserting at the beginning:")
    my_circular_list.show_list_forward()
    
    print("List displayed backward:")
    my_circular_list.show_list_backward()
    
    my_circular_list.remove_by_value(10)
    print("List after removing 10:")
    my_circular_list.show_list_forward()
    
    my_circular_list.remove_by_value(10)#Not found
    my_circular_list.remove_by_value(40)#Not found
    
    my_circular_list.remove_by_value(20)
    print("List after removing 20:")
    my_circular_list.show_list_forward()
    
    #Attempting to empty the list by removing the remaining elements
    my_circular_list.remove_by_value(5)
    my_circular_list.remove_by_value(30)
    print("List after removing all:")
    
    my_circular_list.show_list_forward()
    # most of the comments are because of learning purposes :)
            
                                  
                                  
                                  
            