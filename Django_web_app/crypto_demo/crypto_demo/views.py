

from django.shortcuts import render
from django.http import JsonResponse
from . import Crypto_utulity_v2 as cryptolib , ServerFunctions as SF
from blockchain.models import Block
import json

NULL_ADDRESS = "00000000000000000000"



def index_view(request):
    
    return render(request, 'index.html')


def API_GetWalletBallance(request):
    
    try : 
        
        address = (request.POST['address']).upper()
        
        if(not cryptolib.IsSha256Hash(address)):
            
            return JsonResponse({'error': 'invalid address'} , status = 400)
        
    except:
       
        return JsonResponse({'error': 'invalid address'} , status = 400)
    
    
    
   
    return JsonResponse({'amount' : GetBallance(address)})
        
        
        
    
def API_Derivekeys(request):
    try:
        public_keys = cryptolib.derive_public_key(cryptolib.Turn_str_to_key(request.POST['key']))
        address = cryptolib.HashKeyPair(public_keys)
        return JsonResponse({"public_key" : cryptolib.Turn_key_to_str(public_keys) , 'address' : address})
     
    except:
        return JsonResponse({'error': 'input error'} , status = 400)
def API_GetBlockChainLenght(request):
    print(Block.objects.count())
    return JsonResponse({'lenght' : Block.objects.count()})



#given a user sends a index returns the block of the blockchain at that index
def API_GetBlockData(request):
    try:
       index = int(request.POST['index'])
       
       #here we are making sure the index provided is correct
       # we do not trust the users :)
       if(0 <= index):
           
           if(index < Block.objects.count()):
              
               row = Block.objects.get(index = index)
               
               
               return JsonResponse({'index' : index , 'previouseHash'  : row.last_block_hash, 'blockHash' : row.block_hash , 'toAddress' : row.to_address ,
                                    'fromAddress' : row.from_address,  'amount' : row.amount , 'nonce' : row.random_num , 'signature' : row.signature})
           
            
       return JsonResponse({'error': 'Bad Request - the key <index> must be lower than blockchain lenght but cannot be negative'})
    except:
        return JsonResponse({'error': 'Bad Request - the key <index> must be a integer lower than blockchain lenght but cannot be below 0'})


#API function
def API_Generate_public_and_private_keys(request):
    
    public_key , private_key = cryptolib.generate_public_private_key_pair()
    
    
    public_key = cryptolib.Turn_key_to_str(public_key)
    private_key = cryptolib.Turn_key_to_str(private_key)
    
    
    return JsonResponse({"public" : public_key , "private" : private_key , "address" : cryptolib.HashString(public_key)})



def GetWalletBallance(address):
    return 

#called by a website user
#takes in private key , a target address , and a amount
#then adds to the blockchain a transaction from the owner of the private key to the target address of desired amount
def Create_Transaction(request):
    try:
        
        private_key = cryptolib.Turn_str_to_key(request.POST['privateKey'])
        public_key = cryptolib.Turn_str_to_key(request.POST['publicKey'])
        
        to_address = (request.POST["toAddress"]).upper()
        amount = int(request.POST["amount"])
        
        
        if(not cryptolib.AreCorrespondingKeys(public_key, private_key)):
            
            return JsonResponse({'error': 'keys are not coresponding'} , status = 400)
        
        if(not cryptolib.IsSha256Hash(to_address)):
            
           return JsonResponse({'error': 'invalid to address'} , status = 400)
         
        
        fromAddress = cryptolib.HashKeyPair(public_key)
        
        
        if(GetBallance(fromAddress) < amount):
            return JsonResponse({"message" : "not enought tokens. You are broke"})
        
            
        
        
       
        
      
            
        
        index_ = Block.objects.count()
        signature = json.dumps(cryptolib.Create_signature(private_key, to_address, amount , public_key))
        
        
        previouse_hash = Block.objects.values('last_block_hash')[index_ - 1]
        
        block = cryptolib.Format_data_for_processing(fromAddress, previouse_hash, amount, to_address, signature, public_key, index_)
        mint_block(block)
        
    except:
        return JsonResponse({"error" : "errors in the inputs"})
    
    

#given a block runs some final checks before saving it
def Upload_block(block_data):
    
    
    if(Block.objects.count() == 0):
        new_entrie = Block(block_hash = block_data[0],
                       last_block_hash = block_data[1],
                       from_address = block_data[2],
                       to_address = block_data[3],
                       amount = block_data[4],
                       signature = block_data[5],
                       index = block_data[6],
                       random_num = block_data[7])
        new_entrie.save()
        
        return 
    
    #check if the block hash = last_block_hash
    if(Block.objects.values('block_hash')[Block.objects.count() - 1]['block_hash'] == block_data[1]):
      
        new_entrie = Block(block_hash = block_data[0],
                       last_block_hash = block_data[1],
                       from_address = block_data[2],
                       to_address = block_data[3],
                       amount = block_data[4],
                       signature = block_data[5],
                       index = block_data[6],
                       random_num = block_data[7])
    
        new_entrie.save()
        
        
        
    return 


#this function is for debug
def print_block(data):
   message = ""
   message2 = ""
   for element in data :
       message += str(element)+ "  "
       message2 += str(type(element)) + " "
   print(message)
   print(message2)


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
               block_data.append(nonce)
               
               #the first field is supposed to be the hash
               block_data.insert(0, blockHash)
               
               Upload_block(block_data)
               break
           
         nonce+=1
         

    return True




#this function given a string of wallet will return the amount of tokens that wallets holds
def GetBallance(address):
    blockcount = Block.objects.count()
    
    ballance = 0
    row =  row = Block.objects.get(index = 0)
    
    for i in range(0 , blockcount):
        
        row = Block.objects.get(index = i)
        
        if(row.from_address == address):
            ballance -= row.amount
            
        if(row.to_address == address):
            
            ballance =+ row.amount
    
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
            return JsonResponse({'error': 'The genesis block was not created. Create genesis block first'} , status = 503)
        
        to_address = "1"
        amount = 1
        
        
       
        try:
          
           if('to_adress' and  'amount' in request.POST.keys()):
              
               to_address = (request.POST['to_adress']).upper()
               amount = int(request.POST['amount'])
               
               #checking the input is legit
               if( not cryptolib.IsSha256Hash(to_address)):
                   print("must be valid sha256 string")
                   return  JsonResponse({'error': 'Bad Request - Invalid input data'} , status = 400)
               
           else:
               return  JsonResponse({'error': 'Bad Request - Invalid input data'} , status = 400)
           #amount = int(request.POST["amount"])
        except:
             return  JsonResponse({'error': 'Bad Request - Invalid input data'} , status = 400)
        
       
        
        previouse_hash = Block.objects.values('block_hash')[index_ - 1]['block_hash']
        
        NULL_ADDRESS = cryptolib.NULL_ADDRESS()
        
        blockdata = cryptolib.Format_data_for_processing(NULL_ADDRESS , previouse_hash, amount, to_address, NULL_ADDRESS, NULL_ADDRESS, index_)
        mint_block(blockdata)
        
        
    return JsonResponse({})


#this is the page for the admin / owner , there is only one account , the admin
def owner_view(request):
    if request.user.is_authenticated:
        return render(request, 'owner.html')
    return JsonResponse({"message" : "please log in"})
   
    
   
