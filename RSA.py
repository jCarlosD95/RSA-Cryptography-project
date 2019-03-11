#-----RSA.py-----
#Juan Diaz
#jcd14

class RSA(object):

    def __init__(self):
        self._list = []
        self._e = 0
        self._d = 0
        self._N = 0        

    def inputFunc(self):
        i = int(input("Enter the number of messages: "))
        
        print ("Enter the messages:")
        for _ in range(0,i):
            self._list.append(int(input()))
    

    def printFunc(n):
        return "message is " + str(n)

    #Assumes minVal > 1
    def primeGen(minVal):

        #Any known prime gaps this algorithm can handle are < 500
        #Also, this version of the sieve skips even numbers.
        x = (minVal + 501)//2

        sieve = []
        
        for _ in range (0,x):
            sieve.append(True)

        #Practically speaking, this isn't a list of [0,1,2...]. It's a list of [3,5,7...].
        #ans represents the "actual" sieve index value. Sieve[0]=[3], sieve[1]=[5], etc
        for i in range(0,x):
            ans = i*2+3
            
            if sieve[i] == False:
                continue

            if ans > minVal:
                return ans
            else:
                for j in range (i+ans,x,ans):
                    sieve[j] = False


    def keyGen(self):
        
        minVal = int(input("Enter the minimum value for the prime numbers: "))
        p = RSA.primeGen(minVal)
        q = RSA.primeGen(p)

        self._N = p*q
        tot = RSA.totient(p,q)

        #print("Delete line later: " + str(tot))

        rng = tot//5
        
        for _ in range(rng,100000,-1):
            tester = RSA.gcd(_,tot)[0]
            if tester == 1:
                self._e = _
                break
        
        
        self._d = int(RSA.exEuc(tot,self._e))
        #So that self._d's value will be visible in the debugger:
        d = self._d  

        print("N is " + str(self._N))
        print("e is " + str(self._e))

   

    def encrypt(self, num):
        #print(self._d)
        return int(pow(num, self._e, self._N))

    def decrypt(self, num):
        #print(self._d)
        return pow(num, self._d, self._N)


    def e_decorator(func):
        def rapper(name):
            return "The encrypted " + func(name)
        return rapper
        
        
    def d_decorator(func):
        def rapper(name):
            return "The decrypted " + func(name)
        return rapper
                   

    def messages(self):
        self.inputFunc()
        self.keyGen()
        
        crypt = []

        enc = RSA.e_decorator(RSA.printFunc)
        for _ in self._list:
            x = self.encrypt(_)
            crypt.append(x)
            print (enc(x))

        dec = RSA.d_decorator(RSA.printFunc)
        for _ in crypt:
            x = self.decrypt(_)
            print(dec(x))


    def lcm(x, y):
        return x*y/RSA.gcd(x,y)[0]
        
            
    def gcd(x, y):

        #first, ensure that x >= y
        if x < y:
            _ = x
            x = y
            y = _

        #list used to calculate modular inverse in exEuc(lN,e)
        xgcd = [y,x]
        #Euclidean algorithm
        while True:
            r = x % y

            #used to ensure consistency in the returns;
            #r is always GCD & y is always the last y
            if r == 0:
                r = y
            else:
                xgcd.insert(0,r)
                
            if y%r == 0:
                return xgcd
            else:
                x = y
                y = r

    def totient(x,y):
        return (x-1)*(y-1)

    #my implementation of the extended Euclidean Algorithm
    def exEuc(lN,e):
        xgcd = RSA.gcd(lN,e)
        
        #crashes if lN and e are somehow not coprime
        assert xgcd[0] == 1

        #get rid of "1" from the list
        xgcd.pop(0)

        #Running on the principal that ax + by = gcd(a,b).
        #Also, a > b
        b = xgcd.pop(0)
        a = xgcd.pop(0)
        x = 1
        y = int((a-1)/b)

        if xgcd:

            #switch each iteration between changing b,x and a,y
            switch = True
            while xgcd:
                if switch == True:
                    b = xgcd.pop(0)
                    x = int((b*abs(y) + 1)/a)
                else:
                    a = xgcd.pop(0)
                    y = int((1 - a*x)/b)
                switch = not switch
        else:
            #if it hasn't gone through the xgcd while loop, y must be made negative
            y -= 2*y

        #in the end, it's either 1=e(x)-lN(y) or 1=lN(x)-e(y)
        #ignore the variable attached to lN because lN(x) % lN == 0
        #so the equation simplifies to d=ey 

        
        if lN == a:
            while y < 0:
                y += lN
            return abs(y)
        else:
            return x
            
            

#while input("type \"done\" if you're done or press \"enter\" to continue: ") != "done\n":
test = RSA()
test.messages()

