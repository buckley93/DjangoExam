from django.db import models
from datetime import date
import re
import bcrypt

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        usersWithMatchingEmail = User.objects.filter(Email = postData['Email'])
        errors = {}
        today = date.today()
        if len(postData['Fname']) < 2:
            errors['FirstNamelength'] = "First name should be atleast 2 characters!"
        if len(postData['Lname']) < 3:
            errors['LastNameLength'] = "Last name should be atleast 2 characters!"
        if len(postData['Email']) < 10:
            errors['EmailLength'] = "Email should be atleast 10 characters!"
        elif not EMAIL_REGEX.match(postData['Email']):    # test whether a field matches the pattern            
            errors['emailPattern'] = ("Invalid email address!")
        elif len(usersWithMatchingEmail) > 0:
            errors['emailTaken'] = "This email is taken!"
        if len(postData['PW']) < 8:
            errors['PasswordLength'] = "Password should be atleast 8 characters!"
        if len(postData['Date']) == 0:
            errors['Birthday_req'] = "Birthday required"
        elif postData['Date'] > str(today):
            errors["future_notallowed"] = "cannot enter Date after today"
        
        return errors

    def loginValidator(self, postData):
        errors = {}
        #make sure that the email is found in the database
        usersWithMatchingEmail = User.objects.filter(Email = postData['Email'])
        if len(usersWithMatchingEmail) == 0:
            errors['emailNotFound'] = 'this email is not yet registered!'
        else:
            print("********")
            print(usersWithMatchingEmail[0].Password)
            print('***********')
            # if usersWithMatchingEmail[0].Password != postData['PW']:
            #     errors['incorrectpassword'] = 'Password is incorrect!'
            #     this is for not encrypted passwords

            if not bcrypt.checkpw(postData['PW'].encode(), usersWithMatchingEmail[0].Password.encode()):
                errors['incorrectpassword'] = 'Password is incorrect!'

        return errors

class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        quotes = Quote.objects.filter(message = postData['message'])
        errors = {}
        if len(postData['madeBy']) < 2:
            errors['madeBylength'] = "Quoted by should be atleast 2 characters!"
        elif len(quotes) > 0:
            errors['QuoteTaken'] = "This Quoted has already been used!"
        if len(postData['message']) < 10:
            errors['quoteLength'] = "Message should be atleast 10 characters!"
        
        return errors

    def messageValidator(self, postData):
        errors = {}
        if len(postData['message']) < 10:
            errors['messageLength'] = "Message should be atleast 10 characters!"
        
        return errors

class User(models.Model):
    First_name = models.CharField(max_length=40)
    Last_name = models.CharField(max_length=40)
    Date = models.DateField(null=True)
    Email = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    message = models.TextField()
    madeBy = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, related_name="quote_uploaded", on_delete = models.CASCADE)
    # uploaded_by = user who uploaded a given quote
    favorited_by = models.ManyToManyField(User, related_name="favorite_quote")
    # favorited_by = a list of users who like a given book
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()


