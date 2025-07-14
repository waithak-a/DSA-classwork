class is_Palindrome:
    def __init__(self):
        self.stack =[]    
    def pushChar(self,char):
        self.stack.append(char)    
    def popChar(self):
        if not self.stack:
             return None
        return self.stack.pop()
    
    def is_Palindrome(self,string):
        self.stack =[] # stack reset for each new string
        if not string:
            return True
        for c in string:
            self.pushChar(c)
        for char in string:
            if char !=self.popChar():
                return False
        return True
obj=is_Palindrome()

while True:
    l=input("Enter string (or type 'exit' to quit): ").strip()
    if l.lower() == "exit":
        break
    processed = l.replace(" ", "").lower()
    if obj.is_Palindrome(processed):
        print(f"{l} is a Palindrome")
    else:
        print(f"{l} is not a palindrome")
   