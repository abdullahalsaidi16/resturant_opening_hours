from django.db import models

# Create your models here.

class Resturant(models.Model):
    name = models.CharField(max_length = 60  , unique = True)


class RestOpening(models.Model):
    rest_id = models.ForeignKey( Resturant , on_delete=models.CASCADE)
    APPROVAL_CHOICES = (
    (u'0', u'mon'),
    (u'1', u'tue'),
    (u'2', u'wed'),
    (u'3', u'thu'),
    (u'4', u'fri'),
    (u'5', u'sat'),
    (u'6', u'sun'),
)
    day = models.CharField(max_length = 1 , choices = APPROVAL_CHOICES)
    st_time = models.TimeField('start_time' )
    end_time = models.TimeField('end_time')
    # all_day = models.BooleanField('open all day' , default=False)




