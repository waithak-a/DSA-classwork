#creating a function that returns the power of a number
#It accepts Number, and exponent values as parameters
n = int(input("Enter a number: "))
exponent = int(input("Enter the exponent: "))

def findPower(number, exponent):
    #initializing a variable with 1(it stores the resultant power)
    resultPower =1
    #traversing in the range from 1 to given exponent+1
    for i in range(1, exponent+1):
        #Multiplying the result with the given number
        resultPower=resultPower*number
        #returning the resultant power
        return resultPower
  print ("The power of", n, "to the exponent", exponent, "is:", findPower(n, exponent))