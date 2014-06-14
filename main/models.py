from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=80)
    def __str__(self):  # Python 3: def __str__(self):
        return self.name


class User(models.Model):
    login = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    type = models.IntegerField(default=2)  #type=1 to bedzie uzytkownik zwykly
    ban = models.BooleanField(default=False)
    date_created = models.DateTimeField(
        auto_now_add=True)  #Automatically set the field to now when the object is first created. Useful for creation of timestamps
    last_update = models.DateTimeField(auto_now=True)
    def __str__(self):  # Python 3: def __str__(self):
        return self.login


class Project(models.Model):
    title = models.CharField(max_length=80)
    short_description = models.CharField(
        max_length=160)  #krotki opis projktu,mozeby byc wyswietlany na st glownej, razem z paskiem postepu itd
    full_description = models.TextField()  #pelny opis projektu
    funding_goal = models.DecimalField(max_digits=8, decimal_places=2)  #ilosc pieniedzy planowanych do zebrania
    money_raised = models.DecimalField(default=0, max_digits=8, decimal_places=2)  #ilosc pieniedzy juz zebranych
    deadline = models.DateField(default=datetime.date(datetime.date.today().year, datetime.date.today().month+1, datetime.date.today().day))  #data zakonczenia projektu
    date_created = models.DateTimeField(
        auto_now_add=True)  #Automatically set the field to now when the object is first created. Useful for creation of timestamps
    last_update = models.DateTimeField(
        auto_now=True)  #Automatically set the field to now every time the object is saved. Useful for 'last-modified' timestamps
    overalrating=models.FloatField(default=0)
    ban = models.BooleanField(default=False)
    visit_counter = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    def __str__(self):  # Python 3: def __str__(self):
        return self.title

class Atachment(models.Model):
    url=models.CharField(max_length=200)
    project=models.ForeignKey(Project)
    def __str__(self):
        return self.url
class Rating(models.Model):
    rating = models.IntegerField(default=0)
    user=models.ForeignKey(User)
    project=models.ForeignKey(Project)
    def __str__(self):
        return self.project.title

class DailyVisit(models.Model):
    day=models.DateField(default=datetime.date.today)
    visitors = models.IntegerField(default=0)
    project=models.ForeignKey(Project)

class Perk(models.Model):
    # poziomy wsparcia projektu i przewidziane nagrody za wsparcie taka suma pieniedzy
    amount = models.DecimalField(max_digits=8, decimal_places=2)  #ilosc pieniedzy w danym poziomie
    title = models.CharField(max_length=80)  #tytul, nazwa poziomu
    description = models.TextField()  #opis poziomu
    number_available = models.IntegerField(null=True,blank=True)  #blank=True znaczy, ze wartosc moze byc null
    #jesli amount=null, to liczba danej nagrody za wsparcie jest nieograniczona
    project = models.ForeignKey(Project)
    def __str__(self):  # Python 3: def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    def __str__(self):  # Python 3: def __str__(self):
        return self.content


class Message(models.Model):
    subject = models.TextField(max_length=80)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user_from = models.ForeignKey(User, related_name='message_user_from')
    user_to = models.ForeignKey(User, related_name='message_user_to')
    def __str__(self):  # Python 3: def __str__(self):
        return self.subject


class Donation(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    perk = models.ForeignKey(Perk)
    def __str__(self):
        return str(self.amount)

class ObservedProject(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
