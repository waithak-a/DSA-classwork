base=int(input("Enter base:"))
exp=int(input("Enter exponential value:"))
def power(base,exp):
    if(exp==1):
        return(base)
    if(exp!=1):
        return(base*power(base, exp-1))
    print("The power of", base, "to the exponent", exp, "is:", power(base, exp))
       
       