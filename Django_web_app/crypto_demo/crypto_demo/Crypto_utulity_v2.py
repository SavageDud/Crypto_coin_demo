import random
import json
import prime_numbers as prime_nums

def LoadPrimes():
    return 

#euclid algo to find the greatest common divider
def euclid_gcd(m , n):
    
    if n == 0:
        return m
    
    else:
        r = m % n
        return euclid_gcd(n , r)



def create_private_key():
    return 

#turns a str into a key_pair
def str_to_key():
    return 

# turns a key pair into a str
def key_to_str():
    return


# generates a public key
def derive_public_key():
    
    return 

def generate_prime_num():
    data = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097]
    return data[random.randrange(10 , len(data) - 1)]

def create_large_prime_num():
    """
    rand_file_index = 0
    file = open("prime_numbers/prime_numbers" + str(rand_file_index) + ".json" , "r")
    data = json.load(file)
    """
    return generate_prime_num()
    
#extended euclidean algo
def exteuclid(a, b):
     
    r1 = a
    r2 = b
    s1 = int(1)
    s2 = int(0)
    t1 = int(0)
    t2 = int(1)
    print("running exteuclid algorithm")
    while r2 > 0:
        
       q = r1//r2
       r = r1-q * r2
       r1 = r2
       r2 = r
       s = s1-q * s2
       s1 = s2
       s2 = s
       t = t1-q * t2
       t1 = t2
       t2 = t
        
    if t1 < 0:
        t1 = t1 % a
        
    return (r1, t1)




#generates public & private keys
def generate_public_private_key_pair():
    rand_prime_1 = create_large_prime_num()
    rand_prime_2 = create_large_prime_num()
    

    prime_product = rand_prime_1 * rand_prime_2
    
    #Eulers totient function
    #a coprime of a num has the greatest common diviser of 1 
    #ex : 8 & 9
    
  

    num_coprime_integers_of_product = (rand_prime_1 - 1) * (rand_prime_2 - 1)
    
   
    keys = []
    print("step 1")
    for x in range(19 , num_coprime_integers_of_product):
        if euclid_gcd( prime_product , x) == 1:
            keys.append(x)
            if(len(keys) > 10):
              break
    for key in keys:      
      
      r , d = exteuclid( num_coprime_integers_of_product , key )
    
    
      d = int(d)
      if(r == 1):
        public_key = [key , prime_product]
        private_key = [d , prime_product]
        return (public_key , private_key)
    
 
def Encrypte(message , private_key):
    return(message**private_key[0]) % private_key[1]

def Decrypte(message , public_key):
    return (message ** public_key[0]) % public_key[1] 


#given a key it creates a string of the key to display it
def Turn_key_to_str(key):
    return "<key>" + str(key[0]) + ":" + str(key[1]) + ":"


def Turn_str_to_str(str_):
    key = []
    message = ""
    for x in str_[5:]:
       if(x == ":"):
           key.append( int(message))
           message = ""
       else:
          
           message += x
    return key
           
message = 101
public , private = generate_public_private_key_pair()

str_ = Turn_key_to_str(private)
print(str_)
print(Turn_str_to_str(str_))



