from djongo import models

class TicketCollection(models.Model):

    user_id = models.IntegerField(null=True, blank=True)
    ticket_details = models.JSONField(null=True, blank=True) 
    #ticket_details = models.JSONField(default={}) 

    def __str__(self):
        return self.user_id
