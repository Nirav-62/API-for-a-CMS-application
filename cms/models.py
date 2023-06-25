from django.db import models

class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    password=models.CharField(max_length=60)
    phone_no=models.IntegerField()

    def __str__(self):
          return self.name
class Post(models.Model):
        id=models.AutoField(primary_key=True)
        title=models.CharField(max_length=30)
        description=models.CharField(max_length=100)
        content=models.TextField()
        creation_date = models.DateTimeField(auto_now_add=True)
        u_id=models.ForeignKey("User",on_delete=models.CASCADE)
        is_private=models.BooleanField(default=False)

     

class Like(models.Model):
     id = models.AutoField(primary_key=True)
     post_id=models.ForeignKey("Post",on_delete=models.CASCADE)
     user_id = models.ForeignKey("User",on_delete=models.CASCADE)
     like_count=models.IntegerField(default=0)



        


