
# packages for the blockchain

#SHA256 
import hashlib 

#Time stamps for blocks
import datetime

import time
#Convert data to json for encoding then hashing
import json 


# package for Key generation and cryptographie
import rsa 

#packages for node communication

#run app on local host or port
from flask import Flask , jsonify , request

#send requests 
import requests

#to avoid repeating requests and sent information
from uuid import uuid4

#analize url strings
from urllib.parse import urlparse




#creating keys and Address's
class Keys:
    def GenerateKeyPair(ByteSize = 512):
        
        #generate a key pair
        (public_key , private_key) = rsa.newkeys(ByteSize) 
        
        #format
        return {'private key' : private_key,
                'public key' : public_key}
        
    
    def FormatString(key_pair):
        encoded_keys = [key_pair['private key'].save_pkcs1("PEM"),
                        key_pair['public key'].save_pkcs1("PEM")]
        
        str_keys = [encoded_keys[0].decode("utf-8"),
                    encoded_keys[1].decode("utf-8")]
        
        formated_keys = {'private key' : str_keys[0],
                         'public key' : str_keys[1]}
        return formated_keys
    
    
    
    def SaveKeyPair(key_pair,filename): #save the key pair
        
        
        # right now the keys are <rsa.keys> we want to save so we need it into string
        # but you can't convert <rsa.keys> to str. so first convert to bytes then str
        
        encoded_keys = [key_pair['private key'].save_pkcs1("PEM"),
                        key_pair['public key'].save_pkcs1("PEM")]
        
        str_keys = [encoded_keys[0].decode("utf-8"),
                    encoded_keys[1].decode("utf-8")]
        
        formated_keys = {'private key' : str_keys[0],
                         'public key' : str_keys[1]}
        
        file = open(filename + ".json" ,mode = 'w')
        file.write(json.dumps(formated_keys))
        file.close()
    
    def StringToHex(str_keys):
        encoded_keys = [str_keys['private key'].encode("utf-8"),
                        str_keys['public key'].encode("utf-8")]
        
        key_pair = [rsa.PrivateKey.load_pkcs1(encoded_keys[0]),
                    rsa.PublicKey.load_pkcs1(encoded_keys[1])]
        
        return {'private key' : key_pair[0],
                'public key' : key_pair[1]}
      
    def OpenKeyPair(filename):
        
        #first we open and extract convert the data
        with open(filename + '.json', 'r', encoding='utf-8') as f:
             file = json.load(f)
        
        str_keys = [file['private key'],
                    file['public key']]
        
        encoded_keys = [str_keys[0].encode("utf-8"),
                        str_keys[1].encode("utf-8")]
        
        key_pair = [rsa.PrivateKey.load_pkcs1(encoded_keys[0]),
                    rsa.PublicKey.load_pkcs1(encoded_keys[1])]
        
        return {'private key' : key_pair[0],
                'public key' : key_pair[1]}
    
    def DeriveWalletAddress(Public_key):
        encoded_key = Public_key.save_pkcs1("PEM")
        
        key_hash = hashlib.sha256(encoded_key).hexdigest()
        
        return key_hash
        
        
    
    
'''

Security Flaw

if someone has 

the transaction and its signature

the guy can send out multiple copy's of it 

into the network 

so we need to add

a unique id to each transaction 

and check for duplicates

the id is going to be a 16 bit or 4(byte) 
so a integer with a max limit of 65536

so you can send bob 65536 time 1 PumpAndDump



'''

class Transaction:
    def Format(FromAddress , ToAddress , Amount):
        return {'From Address' : FromAddress,
                'To Address' : ToAddress,
                'Amount' : Amount}
     
    
    def CreateTransaction(Public_key,ToAddress,Ammount):
        
        FromAddress = Keys.DeriveWalletAddress(Public_key)
        
        return Transaction.Format(FromAddress,ToAddress,Ammount)
    
    def GenerateUniqueId():
        return 1
        
        #is the Signature valide?
        #does the wallet have enough funds?
        #is when was the transaction issued ?
        #is the Address valid?



#this class is just


# a Signature is usally just a hash but <class Signature> is object that will contain the 
# the stuff to validate a transaction but the won't be saved on the blockchain itself
# to save space

class Signature:
    def __init__(self):
        return None
    def Format(PublicKey , Signature_hash):
        return {'Signature' : Signature_hash,
                'PublicKey' : PublicKey}
        
    def ValidateSignature(Transaction , public_key, Signature):
        encoded_transaction = json.dumps(Transaction , sort_keys = True).encode()
        
        try:
          if(rsa.verify(encoded_transaction,Signature,public_key) == 'SHA-256'):
              return True
          
        except:
          return False
        
    
    def Sign(Transaction, private_key):
        #encode
        encoded_transaction = json.dumps(Transaction , sort_keys = True).encode()
        #sign
        Signature = rsa.sign(encoded_transaction, private_key,"SHA-256")
        
        return Signature
    
    







class Blockchain:
    def __init__(self):
        self.chain = []
        self.CreateGenesisBlock()
        self.difficulty = 3
        self.transactionperblock = 1
        self.Mining_Reward = 10
        self.NullAdress = "000000000000000"
    def GetChainLength(self):
        return len(self.chain)
    
    
    def GetPreviousBlock(self):
        return self.chain[-1] 
    
    def Get_Previous_hash(self):
        return self.BlockHash(self.GetPreviousBlock())
    
    
    
    def create_block(self , data ,previous_hash,Miner_Wallet = "none"):
        
        
        block = {'index': self.GetChainLength(),
                 'data' : [data],
                 'Timestamp': str(datetime.datetime.now),
                 'nonce' : int(1),
                 'previous hash' : previous_hash,
                 'Miner Wallet' : Miner_Wallet}
        
        return block
    
    def Add_Miner_Reward_To_Block(self,block):
        
        #miner reward transaction
        Miner_Reward = Transaction.Format('00000000',block['Miner Wallet'],self.Mining_Reward)
        
        #new block
        new_block = block
        
        #appending miner reward
        new_block['data'].append(Miner_Reward)
        
        return new_block
        
    def GetWalletBallance(self, Wallet_Address):

        
        ballance = 0
        

        #we want to check all blocks
        for blocks in self.chain[1:]:
            if blocks['data'] == "Genesis_block":
                pass
            #now we want to check all transactions withing these blocks
            
            for transaction in blocks['data']:
                if(type(transaction[0][0]) is not dict):
                    print(transaction[0][0])
                    pass
          
                print(type(transaction[0][0]))
            
                    #each time the from address is the target address we remove
                if(transaction[0][0]['From Address'] == str(Wallet_Address)):
    
                    ballance -= transaction[0][0]['Amount']
                    
                #each time the to address is the target address
                if(transaction[0][0]['To Address'] == str(Wallet_Address)):
                    ballance += transaction[0][0]['Amount']
                    
        
        return ballance
    
    
    
    def BlockHash(self , block):
        encoded_block = json.dumps(block , sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 

    
    
    def CreateGenesisBlock(self):
        previous_hash = "000000000000000000000"
        self.chain.append(self.create_block("Genesis_block", previous_hash,"0"))
    

    
    def AddBlock(self , block ):
       self.chain.append(block)
    
    
    
    def MineBlock(self , block , node):
        
        checkproof = True
        while checkproof:
            bitHash = self.BlockHash(block)
            if bitHash[:self.difficulty ] == "0"*self.difficulty:
                checkproof = False;

            else:
                block['nonce']+= 1;
        return block
    
    
    
    
    def ChainValidation( chain): #checks if all hash are corresponding
        
        for block_index in range(1,len(chain)):
            if(chain[block_index]['previous hash'] != Blockchain.BlockHash(chain[block_index -1 ])):
                return False
            
            if(Blockchain.BlockHash(chain[block_index])[:Blockchain.difficulty] != Blockchain.difficulty * '0'):
                return False
        return True
    


class Node:
    
    def __init__(self,Wallet_Address):
        self.mempool = [{},{}] #index 0 is for transactions , index 1 for Signatures
        self.blockchain = Blockchain()
        self.NodeIps = set()
        self.WalletAddress = Wallet_Address
        
        #next variable is checking if a message has been already received
        self.Messagelog = {}
        self.MaxTimeDelay = 10
        
        
    
    '''
    
    Following functions are for creating blocks and adding transaction to mempool
    
    #Center of logic and decision of the miner
    Main_Func()
    
    Create_Next_Block()
    
    Check for mining interruption
    
    Add a transaction to mempool
    
    (!Test Function !)
    Add transction without verify
    
    Create first coins
    
    ValidateTimeStamp()
    
    
    
    '''
    def Main_Func(self):
        return None
    
    #once there are transactions on the mempool we will create a block 
    def Create_Next_Block(self):
        

      
        next_block = self.blockchain.create_block([list(self.mempool[0].values()),list(self.mempool[1].values())],self.blockchain.Get_Previous_hash(),self.WalletAddress)
        
        if(self.WalletAddress != False): 
           next_block = self.blockchain.Add_Miner_Reward_To_Block(next_block)
        
        #we start to mine it
        
        mined_block = self.blockchain.MineBlock(next_block,self)
        
        self.blockchain.AddBlock(mined_block)
        
        self.mempool = [{},{}]
    
    # During mining we want to check for interrupting event 
    # for example another node mined before us the next block
    # Or we receive an new transaction and we need to add it to our mempool
    
    def Check_For_Mining_Interruptions():
        return 0
    
    
    #The next function is just for testing 
    def AppendTransaction_without_Verify(self,transaction,Signature):
        transaction_hash = Node.Transaction_hash(transaction)
        self.mempool[0][transaction_hash] = transaction
        self.mempool[1][transaction_hash] = Signature
        

    #The next function is just for testing
    def Create_first_coins(self,wallets,amount):
        for keypair in wallets:
            pair = Keys.OpenKeyPair(keypair)
            
            transaction = Transaction.Format("000000" , Keys.DeriveWalletAddress(pair['public key']), amount)
            
            self.AppendTransaction(transaction)
            
     
    def Add_Transaction_To_Mempool(self,transaction, tr_Signature):
        #first we verify the authenticty of the transaction
       
        if(not Signature.ValidateSignature(transaction,tr_Signature['PublicKey'],tr_Signature['Signature'])):
            print("Signature not valid")
            return False
        
        # then we verify the blockchain to check if the wallet has enough balance
        if(self.blockchain.GetWalletBallance(transaction['From Address']) < transaction['Amount']):
            print("Not enough funds")
            return False
        
        # transaction is valid
        
        transaction_hash = self.Transaction_hash(transaction)
        
        self.mempool[1][transaction_hash] = tr_Signature
        
        self.mempool[0][transaction_hash] = transaction
        
        return True
    
    

    
    
    '''
   
    ////
    The next functions are for verification and handleging data
   
    Transaction_hash() is for dictonary storing data in mempool
    
    Find a transaction-signtare  in mempool
   
    remove a transaction-Signature 
   
    return currenct chain
   
    verify a block 
    
    Get hash of <transaction>-<Signature> pair
    
    (this function is called after the node accepts a block from another miner
    its purpose is removing all transaction that we in a block)
    
    RemoveListOfTransaction()
    
    ///
    
    '''
    
    
    
    
    def Transaction_hash(transaction):
        encoded_json = json.dumps(transaction,sort_keys = True).encode()
        return hashlib.sha256(encoded_json).hexdigest()
    
    def Remove_Transaction_From_mempool(self,transaction_hash):
        self.mempool[0][transaction_hash] = None
        self.mempool[1][transaction_hash] = None
        
    
    def Return_Chain(self):
        return self.blockchain.chain
    
    def Verify_Block(self,block,Signatures):
        # verify hash 
        if(block['previous hash'] == self.blockchain.Get_Previous_hash()):
            return False
        if(self.blockchain.BlockHash(block)[:self.blockchain.difficulty] != '0' * self.blockchain.difficulty):
            return False
        
        
        # verify transaction
        transactions  = block['data']  
        Number_of_transaction = len(transactions) -1
        
        for transaction in range(0,Number_of_transaction):
            #check Signature
            if(Signature.ValidateSignature(transactions[transaction],Signatures[transaction]['public key'],Signatures[transaction]['Signature']) == False):
                return False
            
            #if the Signatures are all valid
            #check wallet ballence
            if(self.blockchain.GetWalletBallance(transactions[transaction]['From Address']) <= transactions[transaction]['Amount']):
                return False
        # the last transaction is the reward for the miner so
        
        Miner_Reward = "!!note !! under construction" 
        
        #now the block is valid so we add it and we send it to other miners
        
        self.blockchain.AddBlock(block)
        self.RemoveListOfTransactions(transactions)
        return True 
    
    
    def RemoveListOfTransactions(self,transaction_list):
        for transaction in transaction_list:
            _hash = Node.Transaction_hash(transaction)
            if(_hash in self.mempool[0].keys):
                self.Remove_Transaction_From_mempool(_hash)
    """
    
    ///
    This is handling the web-requests ids
    to check if we already received a transaction
    or block .
    
    nodes are suposed to relay info to each other,
    so to make sure they dont relay infinitly
    
    we will attach a mesage id to message
    
    these functions are for handling that
    
    ///
    
    
    
    """
    
    def IsMessageDuplicate(self,message_id):
        try:
            if self.Messagelog[message_id] != None:
               return True
        except:
            return False
    

    def Refactor_Message_Log(self,Max_Time_Difference):
        current_time = time.time()
        for key , value in self.Messagelog.items():
            if(current_time - value):
                self.Remove_Entry_Message_Log(key)
                
        
    def Add_Entry_Message_Log(self, message_id , timestamp):
        self.Messagelog[message_id] = timestamp
        
    def Remove_Entry_Message_Log(self, message_id):
        self.Messagelog.pop(message_id, None)
        
    
    
    
    def Create_message_id(self,message):
        
        Json_id = {'A' : self.WalletAddress,
                   'B' : message,
                   'C' : str(time.time)}
        
        encoded_id = json.dumps( Json_id ,sort_keys = True ).encode()
        
        return hashlib.sha256(encoded_id).hexdigest()
    """
    
    ///
    Networking related transaction 
    
    Send transaction to other nodes
    
    Send the new block
    
    Add Ip
    
    Replace Chain
    
    Send block to other nodes
    
    Send Transaction to other nodes
    
    ///
    
    
    
    """
    
    def Add_IP(self, address):
        parsel_url = urlparse(address)
        self.NodeIps.add(parsel_url.netloc)
    
    def ReplaceChain(self):
           network = self.NodeIps
           
           CurrentChainLenght = len(self.blockchain.chain)
           LongestChain = None
           
           for nodes in network:
               response = requests.get(f'https://{nodes}/get_chain')
               
               if response.status.code == 200:
                   length = response.json()['length'] 
                   chain = response.json()['chain']
                   if length > CurrentChainLenght and Blockchain.ChainValidation(chain) :
                       LongestChain = chain
            
           if LongestChain:
                self.blockchain.chain = LongestChain
                return True
           return False
    
    def Send_transaction_to_other_nodes(self , transaction , signature , message_id):
        
        json_object = {'transaction' : transaction,
                       'Signature' : signature,
                       'message_id' : message_id}
        
        for node in self.NodeIps:
            r = requests.post(node + '/send_transaction' , json_object)
            
            if(r.status_code == 401):
                print("Error send_transaction_to_other_nodes()")
                print(json.dumps(json_object , sort_keys = True))
    
    def Send_Block_to_other_nodes(self, block ,Signatures , message_id):
        
        #the object that we will send to other people
        json_object = {'block':block,
                       'Signatures' : Signatures,
                       'message_id' : message_id}
        
        for node in self.NodeIps:
            r = requests.post(node+'/send_block' , json_object)
            
            if(r.status_code == 401):
                
                '''this is for debuging only 
                In a real senario we cannot know if 401 is really a bug 
                because we cant trust the other party to have the same software as us'''
                
                
                print('////////////////////\n \n',
                      'Function : Send_Block_to_other_nodes\n',
                      'Class: Node  Line: 547 \n \n',
                      'Networking error : The format of json_object is incorrect \n \n',
                      str(json_object),
                      '////////////////////\n')
            
        
       

Miner = Node("A")
        




list_of_key_files = ["Bobick_keys","Suzane_keys","Jhonny_keys","Joes_keys"]

Openned = Keys.OpenKeyPair("Bobick_keys")

Trans = Transaction.CreateTransaction(Openned["public key"],"gayniger", 10)

Signature = Signature.Format(Openned["public key"],Signature.Sign(Trans,Openned['private key']))

Trans1 = Transaction.Format("A" , Keys.DeriveWalletAddress(Openned["public key"]), 100)

Miner.AppendTransaction_without_Verify(Trans1 , 'signatur_Legit');

Miner.Create_Next_Block()








app = Flask(__name__)



#response the chain
@app.route("/get_chain" , methods = ['GET'])
def get_chain():
    response = {'chain' : Miner.blockchain.chain,
                'length' : len(Miner.blockchain.chain)}
    return jsonify(response) , 200





@app.route('/send_block', methods = ['POST'])
def send_block():
    json = request.get_json()
    keys = ['message_id','block','Signatures']
    
    if(not all(key in json for key in keys)):
        return 'Some elements are missing' , 400 
    
    
    
    if(Miner.IsMessageDuplicate(json['message_id'])):
        return 
    block = json['block']
    signaturs = json['Signatures']
    
    if(Miner.Verify_Block(block,signaturs)):
        
        Miner.Send_Block_to_other_nodes(block,signaturs,json['message_id'])
        
    response = {'message' : 'all good'}
    
    return jsonify(response),201





@app.route('/connect_node' , methods = ['POST'])
def connect_node():
    
    json = request.get_json()
    if(json.get('node') == None ):
        return 'No nodes found', 400
    address = json.get('node')
    
    for node in address:
        Miner.Add_IP(node)
        
    return 'Node added',201

    
@app.route('/send_transaction' , methods = ['POST'])
def Add_Transaction():
   json = request.get_json()
   
   keys = ['transaction','Signature', 'message_id']
   
   if(not all(key in keys for key in json)):
       return "elements are missing",400
   
   if(not Miner.IsMessageDuplicate(json['message_id'])):
        return 'message is already received',200
    
   if(Miner.Add_Transaction_To_Mempool(json['transaction'],json['Signature'])):
       Miner.Send_transaction_to_other_nodes(json)
   return "Under_Construction"    

 
