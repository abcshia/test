#Project Euler
#3
def isprime(n):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False
    for i in range(3,int(n**0.5)+1,2):   # only odd numbers
        if n%i==0:
            return False    
    return True
    
def main():
    x = 600851475143
    i = 2
    while (1):
        if ((x%i)==0):
            quo = x/i
            if isprime(quo):
                print("the answer is",quo)
                break
        i=i+1

#4
# palindrome: find the largest palindrome made from the
# product of two 3-digit numbers

#def palin():
    #M = 102341
    #A = str(M)
    #print(A[0])
    #print(A[1])
    #print(A[:])
    #print(A[len(A)-1])

    #if A[0]==A[len(A)-1]:
     #   print("PALINDROME")
# This function returns TRUE if number is a palindrome
# determining if somthing (N the number,H = str(N)) is palindrome:
# this problem requires that len(str(N))%2==0
# after that, check that

def palinOrNot(N):
    x = 0
    H = str(N)
    if len(str(N))%2==0:
        for i in range(int(len(str(N)))-1, int((len(str(N))/2))-1, -1):
            
            if H[x]==H[i]:
                x = x+1
                
            else:
                print("NOT PALIN")
                return False 
                
        return True
    else:
        print("NOT EVEN")
        return False

def palinLarge():
    for n in range(999,100-1,-1):
        for m in range(999,100-1,-1):
                A = n*m
                if palinOrNot(A):
                    print("n,m",(n,m))
                    print(A)
                    break

                

print (palinOrNot(9001))

