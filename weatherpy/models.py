from django.db import models


class MessagesDb(models.Model):

    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    message = models.CharField(max_length=1000)

    def __str__(self):
        return(self.name)
