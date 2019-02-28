from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length=50)
    added_by =models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(max_length=500)
    poster = models.ImageField(upload_to='event_poster')
    location = models.CharField(max_length=30)
    time = models.TimeField()
    date = models.DateField(null=True)
    seats = models.IntegerField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})
    
    def remain_ticket(self):
        booked = sum(self.tickets.all().values_list("tickets",flat=True))
        return self.seats - booked
    
class BookEvent(models.Model):
    tickets = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')

