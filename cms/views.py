from django.shortcuts import render,get_object_or_404
from django.http import request,HttpResponse , JsonResponse
from django.core import serializers
from .models import User,Post,Like
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        name = data['name']
        email = data['email']
        password = data['password']
        no = data['phone_no']

        # Create the user object
        user = User()
        user.name=name
        user.email=email
        user.password=password
        user.phone_no=no
        user.save()

        return JsonResponse({'Success':'User created successfully','user_id': user.id})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
@csrf_exempt
def update_user(request,user_id):
        if request.method == 'PUT':
             u=User.objects.get(id=user_id)
             body_unicode = request.body.decode('utf-8')
             data = json.loads(body_unicode)
             name = data['name']
             email = data['email']
             password = data['password']
             no = data['phone_no']
             u.name=name
             u.email=email
             u.password=password
             u.phone_no=no
             u.save()
             return JsonResponse({'Success':'User updated successfully','user_id': u.id})
        else:
            return JsonResponse({'error': 'Invalid request method'})


def get_user(request,user_id):
    if request.method == "GET":
        user= get_object_or_404(User,id=user_id)
        return JsonResponse({"id":user.id,"name":user.name,"password":user.password,"email":user.email,"phone_no":user.phone_no},safe=False)
    
    else:
         return JsonResponse({'error':'Invalid request method'})
@csrf_exempt   
def delete_user(request,user_id):
     if request.method == "DELETE":
            user= get_object_or_404(User,id=user_id)
            user.delete()
            return JsonResponse({'error': 'User Deleted Successfully'})
     else:
         return JsonResponse({'error':'Invalid request method'})



@csrf_exempt
def create_post(request):
     if request.method == "POST":
           body_unicode = request.body.decode('utf-8')
           data = json.loads(body_unicode)
           title=data['title']
           description=data['description']
           content=data['content']
           created=data['created_at']
           uid=data['u_id']
           post=Post.objects.create(title=title,description=description,content=content,creation_date=created,u_id=User.objects.get(id=uid),is_private=True)
           return JsonResponse({'success':'post created successfully'},safe=True)
     
     else:
          return JsonResponse({'error':'request not error'})

def see_posts(request,user_id):                 #see all the blogs and posts
    if request.method == "GET":
       if(Post.objects.filter(u_id=user_id).exists()):
             p=Post.objects.filter(u_id=user_id)
          
             result=[]  
             for item in p:
                 lcount=Like.objects.filter(id=item.id).count()    #post and its count 
                 data={
                 "title":item.title,
                 "description":item.description,
                 "content":item.content,
                 "creation_date":item.creation_date,
                 "like count":lcount,
                 "Private":item.is_private,
                  }       
                 result.append(data)
             return JsonResponse({'message':'only you have access to it','data':result},safe=False)
 

       else:
            
        post=Post.objects.filter(is_private=False)
        result=[]  
        for item in post:
            lcount=Like.objects.filter(post_id=item.id).count()    #post and its count 
            data={
                 "title":item.title,
                 "description":item.description,
                 "content":item.content,
                 "creation_date":item.creation_date,
                 "like count":lcount,
                 "Private":item.is_private,
                 
            }       
            result.append(data)
        return JsonResponse({'data':result},safe=False)
    
    
    
@csrf_exempt
def delete_post(request,post_id,user_id):      # delete the post if the user is owner of the post or post created by them otherwise we show the approprate message
     if request.method == "DELETE":
         post=Post.objects.get(id=post_id)
         user=User.objects.get(id=user_id)
         if (post.u_id == user):
              print("hello")
              d=get_object_or_404(Post,id=post_id)
              d.delete()
              return JsonResponse({'success':'post/blog deleted successfully'},safe=False)
         else:
                return JsonResponse({'message':'You do not have right to delete this post '},safe=False)
     else:
          return JsonResponse({'error':'request error'},safe=False)

@csrf_exempt
def update_post(request,post_id,user_id):
     if request.method == "PUT":
         post=Post.objects.get(id=post_id)
         user=User.objects.get(id=user_id)
         if (post.u_id == user):
           body_unicode = request.body.decode('utf-8')
           data = json.loads(body_unicode)
           title=data['title']
           description=data['description']
           content=data['content']
           created=data['created_at']
           post=Post.objects.filter(id=post_id)
           post.update(title=title,description=description,content=content,creation_date=created)
           post=Post.objects.get(id=post_id)
           return JsonResponse({'success':'post/blog updated successfully','title':post.title,"description":post.description,"content":post.content,"creation_date":post.creation_date},safe=False)
         else:
              return JsonResponse({'message':'You do not have right to delete this post '},safe=False)
     else:
          return JsonResponse({'error':'request error'},safe=False)

              



@csrf_exempt
def get_post(request,id,user_id):
     if request.method == "GET":
         post=Post.objects.get(id=id)
         user=User.objects.get(id=user_id)
         if (post.u_id == user):
              lcount=Like.objects.filter(post_id=post.id).count()
              return JsonResponse({'title':post.title,"description":post.description,"content":post.content,"creation_date":post.creation_date,'like_count':lcount},safe=False)
         else:
                return JsonResponse({'message':'this is private post you dont have right to access it'},safe=False)
     else:
                return JsonResponse({'error':'requrst error occured'})


def get_like(request,like_id):
     if request.method == "GET":
          like=Like.objects.filter(id=like_id)
          data=serializers.serialize('json',like)
          return JsonResponse(data,safe=False)
       
        #   return JsonResponse({'id':like.id,'post_id':like.post_id,'user_id':like.user_id},safe=False)
     else:
          return JsonResponse({'error':'requrst error occured'})
@csrf_exempt
def create_like(request):
     if request.method == "POST":
         body_unicode = request.body.decode('utf-8')
         data = json.loads(body_unicode)  
         pid=data['post_id']
         uid=data['user_id']
         if(Like.objects.filter(post_id=pid,user_id=uid)):        # here checks that user is already liked or not if it is then like should be denied and unlike functiionality is implemented in PUT request
            
            return JsonResponse({'error':'user already liked post'},safe=False )
         else:
            l=Like.objects.filter(post_id=Post.objects.get(id=pid)).count()
            l=l+1
            like=Like.objects.create(post_id=Post.objects.get(id=pid),user_id=User.objects.get(id=uid),like_count=l)
            like.save()
         
         
         return JsonResponse({'success':'like post successfully'})
     else:
          return JsonResponse({'error':'request error'})


@csrf_exempt
def update_like(request):
     if request.method == "PUT":
         body_unicode = request.body.decode('utf-8')
         data = json.loads(body_unicode) 
         pid=data['post_id']
         uid=data['user_id']
         if(Like.objects.filter(post_id=pid,user_id=uid)):
              like=Like.objects.get(post_id=pid,user_id=uid)
              like.delete()
         return JsonResponse({'success':'like updated succesfully'},safe=False)
     else:
        return JsonResponse({'error':'request error'})




