

from django.shortcuts import render
from django.http import JsonResponse
from . import Crypto_utulity_v2 as cryptolib , ServerFunctions as SF
from blockchain.models import Block
import json

NULL_ADDRESS = "00000000000000000000"



def index_view(request):
    
    return render(request, 'index.html')


# 
def Generate_public_and_private_keys(request):
    
    public_key , private_key = cryptolib.generate_public_private_key_pair()
    
    
    public_key = cryptolib.Turn_key_to_str(public_key)
    private_key = cryptolib.Turn_key_to_str(private_key)
    
    
    return JsonResponse({"public" : public_key , "private" : private_key , "address" : cryptolib.HashString(public_key)})





#called by a website user
#takes in private key , a target address , and a amount
#then adds to the blockchain a transaction from the owner of the private key to the target address of desired amount
def Create_Transaction(request):
    try:
        
        private_key = request.POST["private_key"]
        to_address = request.POST["to_adress"]
        amount = int(request.POST["amount"])
        
        private_key = cryptolib.Turn_str_to_key(private_key)
        
        #data inside the block
        public_key = cryptolib.derive_public_key(private_key)
        
        fromAdress = cryptolib.HashKeyPair(public_key)
        
        if(amount > GetBallance(fromAdress)):
            return JsonResponse({"message" : "not enought tokens. You are broke"})
        index_ = Block.objects.count()
        signature = str(cryptolib.Create_signature(private_key, to_address, amount))
        
        
        previouse_hash = Block.objects.values('last_block_hash')[index_ - 1]
        
        block = cryptolib.Format_data_for_processing(fromAdress, previouse_hash, amount, to_address, signature, public_key, index_)
        mint_block(block)
        
    except:
        return JsonResponse({"error" : "errors in the inputs"})
    
    

#given a block adds it to the database of the model <Block>
def Upload_block(block_data):
    new_entrie = Block(block_hash = block_data[0],
                       last_block_hash = block_data[1],
                       from_address = block_data[2],
                       to_address = block_data[3],
                       amount = block_data[4],
                       signature = block_data[5],
                       random_num = block_data[6])
    
    new_entrie.save()
    return 


#this function is for debug
def print_block(data):
   message = ""
   for element in data :
       message += str(element)+ "  "
   print(message)



def mint_block(block_data):
    #previouse_block
    str_data = json.dumps(block_data)
    nonce = 0
    MAX_TRIES =10000
    
    print("mining block")
    while nonce < MAX_TRIES:
         blockHash = cryptolib.HashString(str_data + str(nonce))
         if(blockHash[:2] == "00"):
               
               print("found needed nonce , uploading block")
               #the last field in blockchain/models.py Block , is the nonce not the index
               block_data[len(block_data) - 1] = nonce
               
               #the first field is supposed to be the hash
               block_data.insert(0, blockHash)
               
               print_block(block_data)
         nonce+=1
         

    return True


#this function given a string of wallet will return the amount of tokens that wallets holds
def GetBallance(wallet):
    ballance = 0
    for i in range(0 , Block.objects.count()):
        row = Block.objects[i]
        if(row["from.."] == wallet):
            ballance -= row["amount"]
            
        if(row["to .."] == wallet):
            ballance += row["amount"]
    return ballance


def Create_genesis_block(request):
    if( request.user.is_authenticated):
       
        if(Block.objects.count() == 0):
            print("hello world")
            block_data = cryptolib.Format_data_for_processing("Beging of the blochain", "000000000000", 0, "000000000000", "000000000000", "Genesis block", 0)
            mint_block(block_data)
    return JsonResponse({})
       


#once in the admin is in his page he can decide to mint new tokens
#and he will make a call to this function

def Admin_command_mint(request):
    if(request.user.is_authenticated):
        
        index_ = Block.objects.count()
        
        #check if the genesis block exists -
        if(index_ == 0 ):
            return JsonResponse({"message" : "genesis block not created. Please create it"})
        
        try:
           to_address = request.POST["to_adress"]
           amount = int(request.POST["amount"])
        except:
             return JsonResponse({"message" : "errors in the inputs"})
        
       
        
        previouse_hash = Block.objects.values('last_block_hash')[index_ - 1]
        
        NULL_ADDRESS = cryptolib.NULL_ADDRESS()
        
        blockdata = cryptolib.Format_data_for_processing(NULL_ADDRESS , previouse_hash, amount, to_address, NULL_ADDRESS, NULL_ADDRESS, index_)
        mint_block(blockdata)
        
        
    return JsonResponse({})
#this is the page for the admin / owner , there is only one account , the admin
def owner_view(request):
    if request.user.is_authenticated:
        return render(request, 'owner.html')
    
   
    
   
"""

def derivekeys(request):
    

    



def get_ballance
    
"""