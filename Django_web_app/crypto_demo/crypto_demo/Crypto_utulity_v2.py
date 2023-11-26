import random
import json
import hashlib
import datetime



def NULL_ADDRESS():
    return ("0" * 64)




#euclid algo to find the greatest common divider
def euclid_gcd(m , n):
    
    if n == 0:
        return m
    
    else:
        r = m % n
        return euclid_gcd(n , r)









# given a string return a sha256 hash of that string
def HashString(str_):
    return hashlib.sha256(str_.encode("utf-8")).hexdigest()







#given a key, return a string of the Sha256 hash of that key
def HashKeyPair(key_pair):
    return hashlib.sha256((str(key_pair[0])+ "<>" + str(key_pair[1])).encode("utf-8")).hexdigest()











# given a private_key , derive_the public_key
def derive_public_key(private_key):
    message = 101
    encryped = Modular_exponentiation_with_key(message, private_key)  
    n = private_key[1]
    a = 0
    MAX_TRIES = 100
    for i in range(0 , MAX_TRIES):
        if(Modular_exponentiation_with_key(encryped,[i , n]) == message):
            return [i , n]
    return 




# Note I was encountering problems loading the primes numbers so I made a list
def generate_prime_num():
    data = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097]
    return data[random.randrange(10 , len(data) - 1)]







def create_large_prime_num():
    
    return generate_prime_num()





    
#extended euclidean algo
def exteuclid(a, b):
     
    r1 = a
    r2 = b
    s1 = int(1)
    s2 = int(0)
    t1 = int(0)
    t2 = int(1)
    
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
    
    print("generating keys")
    
    
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
    







# given a integer and a list of integers , encrypt/decrypt the integer with the list of 2 integers
def Modular_exponentiation_with_key(message , key):
    return(message ** key[0]) % key[1]



#given a public and private key returns true if they are coresponding else returns false
def AreCorrespondingKeys(public_key , private_key):
    Message = 643
    return(Message == Modular_exponentiation_with_key(Modular_exponentiation_with_key(Message , private_key), public_key))


#given these inputes create a array of those input, formated with the <Block> model in mind
def Format_data_for_processing(From_address , previouse_hash , amount , to_address , signature , public_key , index):
    return [previouse_hash , From_address , to_address , amount , signature , index]








#given a key it creates a string of the key to display it
def Turn_key_to_str(key):
    return "[key]" + str(key[0]) + "]" + str(key[1]) + "]"









#given a string of a formated key
#return the key in the form of a array with integers
def Turn_str_to_key(str_):
    key = []
    message = ""
    for x in str_[5:]:
       if(x == "]"):
           key.append( int(message))
           message = ""
       else:
          
           message += x
    return key





#given a string of a hexidecimal number 
#return the equivalent integer
def Convert_Hexadecimal_to_num(str_):
    base = 16
    symboles = {'0' : 0 , '1' : 1 , '2' : 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 , '7' : 7 , '8' : 8 , '9' : 9 , 'A' : 10 , 'B' : 11 , 'C': 12 , 'D' : 13, 'E' : 14 , 'F': 15}
    len_ = len(str_)
    num = 0
    for c in range(0 , len_):
        num += (base ** (len_- c - 1)) * symboles[str_[c]]
        
    return num







#Given a list of string representings Hexadecimal numbers 
#Convert it to a list of integer
def Convert_Hexa_series_to_num_series(series):
    new_series = []
    for hexa_ in series:
        new_series.append(Convert_Hexadecimal_to_num(hexa_))
    return new_series








# given a list [1 , 2 ,3 ,4 ,5 , ...] and a key
# run encryption/decryption with key on every element indivually
# output: [314, 2451 ,7624 ,5825 , 1225, ..]
def Run_mod_expo_with_key_on_list(list_ , key):
    new_list = []
    for element in list_:
        new_list.append(Modular_exponentiation_with_key(element, key))
    return new_list
    




#given a hexadecimal_data ex : 'FF41BE69DC'
#break down that string into segments of maximum MAX_LEN lenght
# ex output: ['FF' , '41' , 'BE' , '69' , 'DC']
def Break_down_hash(hash_str):
    MAX_LEN = 2
    segments = []
    c = ""
    
    for char_ in range(0 , len(hash_str)):
        c = c + hash_str[char_]
        if (char_ % MAX_LEN == 0):
            segments.append(c)
            c = ""
    if(len(c) > 0) :
        segments.append(c)
    return segments








#given a private_key , a recipients address and a amount, creates a string of a signature of the transaction
#the signature is a array of numbers : [num1 , num2 , num3 , num4 , num5]
def Create_signature(private_key , to_address , amount , public_key):
    message = Break_down_hash(to_address)
    message = Convert_Hexa_series_to_num_series(message)
    message.append(amount)
    message = Run_mod_expo_with_key_on_list(message, private_key)
    message.append(Turn_key_to_str(public_key))
    return message
    


     
#given a string 
#returns true if its a hexadecimal string

def IsHexaDecimal(str_):
    str_ = str_.upper()
    symboles = {'0' : 0 , '1' : 1 , '2' : 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 , '7' : 7 , '8' : 8 , '9' : 9 , 'A' : 10 , 'B' : 11 , 'C': 12 , 'D' : 13, 'E' : 14 , 'F': 15}
    for c in str_:
        if c not in symboles.keys():
            return False
    return True

def IsSha256Hash(str_):
    if(len(str_) != 64):
        return False
    
    if( not IsHexaDecimal(str_) ):
        return False
    return True







