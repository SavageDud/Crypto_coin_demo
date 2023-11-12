from django.db import models

class Block(models.Model):
    
    block_hash = models.CharField(max_length=512)
    
    last_block_hash = models.CharField(max_length=512)
    from_address = models.CharField(max_length=512)
    to_address = models.CharField(max_length=512)
    amount = models.IntegerField()
    signature = models.CharField(max_length=1024)
    random_num =  models.IntegerField()
    
    