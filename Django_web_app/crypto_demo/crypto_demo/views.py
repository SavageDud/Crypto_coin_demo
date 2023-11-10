

from django.shortcuts import render
from django.http import JsonResponse
from . import Crypto_utulity_v2 as cryptolib


def index_view(request):
    
    return render(request, 'index.html')

def Generate_public_and_private_keys(request):
    
    public_key , private_key = cryptolib.generate_public_private_key_pair()
    public_key = cryptolib.Turn_key_to_str(public_key)
    private_key = cryptolib.Turn_key_to_str(private_key)
    
    return JsonResponse({"public" : public_key , "private" : private_key})

"""
def login(request):
    
def derivekeys(request):
    
def GenereateKeys(request):
    
def add_transaction(request):


def get_ballance
    
"""