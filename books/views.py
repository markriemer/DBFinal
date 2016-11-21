from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import models

from .forms import ChangePasswordForm
from .models import Books, Authors, Publishers, Wrote, Discusses, Users, Notifications, Follows, Checkouts
from django.db import IntegrityError
from django.db.models import Q 
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import sys

# Create your views here.

@login_required(login_url="login/")
def main(request):
    book_data = Books.objects.all()
    books = {'book_data': book_data}
    return render(request,"main.html", books)

#@login_required(login_url="login/")
def change_password(request):
    if request.method == 'POST':
        print("POST to change password")
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            pass1 = form.cleaned_data['password_1']
            pass2 = form.cleaned_data['password_2']
            if pass1 == pass2:
                #update logic
                print(request.user.username)
                user = request.user
                user.set_password(pass1)
                user.save()
                render(request, 'main.html')
            else:
                print("Invalid password")
        else:
            form = ChangePasswordForm()
            print("Invalid password form?")
            return(request, 'change_password.html', {'form' : form})
    else:
        form = ChangePasswordForm()
            
    return render(request, 'change_password.html', {'form': form})

#@login_required(login_url="login/")
def discussion(request, book_id):
    book_dis = Books.objects.get(pk=book_id)
    book_context = {"messages" : book_dis.discussion_set.all()}
    return render(request, 'discussion.html', book_context)

#index is shell that makes ajax calls to booklist to populate list.  
def index(request,orderby='book_id'):
    return render(request, 'books/index.html')

#index is shell that makes ajax calls to booklist to populate list.  
def viewindex(request,orderby='book_id'):
    user=request.user
    context = {"user" : user}
    return render(request, 'books/viewindex.html', context)

#the list of books shown by index. performs sorting and filtering 
def booklist(request, orderby='book_id'):
    #these set the next sort order so clicking on column heading toggles sort
    if orderby=='title': 
        titlesort='-title'
        pubsort='pub'
    elif orderby=='-title': 
        titlesort='title'
        pubsort='pub'
    elif orderby=='pub':
        titlesort='title'
        pubsort='-pub'
    elif orderby=='-pub':
        titlesort='title'
        pubsort='pub'

    #get any search filter and apply it
    search = request.GET.get("search")
    if search is None:
        search=""
    wrote_list = list(Wrote.objects.order_by('book').filter(Q(book__title__icontains=search)|Q(book__pub__name__icontains=search)))

    #sort the list based on the order by
    reverse=False
    if orderby=='-title':
        reverse=True
        wrote_list = sorted(wrote_list,key= lambda x: x.book.title, reverse=reverse)
    if orderby=='pub':
        wrote_list = sorted(wrote_list,key= lambda x: x.book.pub.name, reverse=reverse)
    if orderby=='-pub':
        reverse=True
        wrote_list = sorted(wrote_list,key= lambda x: x.book.pub.name, reverse=reverse)

    #this allows the template to not print duplicate data for books with multiple authors
    prev = 0
    for entry in wrote_list:
         if entry.book == prev:
             entry.id = -1    #marks an entry to not repeat title and publisher
         prev=entry.book
          
    context = {'wrote_list':wrote_list,'titlesort':titlesort,'pubsort':pubsort}
    resp = render(request, 'books/booklist.html', context)
    return resp

#shows a blank book form.  modifybook is what actually adds the book to the database when called by book.html ajax
def addbook(request):
    book = Books(book_id=-1)
    author_list = Authors.objects.all()
    publisher_list = Publishers.objects.all()
    wrote_list = Wrote.objects.filter(book=-1)   #pass this so we can use same template as updatebook
    context = {'book': book,'author_list':author_list,'publisher_list':publisher_list, 'wrote_list':wrote_list}
    return render(request, 'books/book.html', context)

#shows a book to be edited.  modifybook does the actual database update when valled by book.html ajax
def updatebook(request, book_id):
    book = Books.objects.get(book_id=book_id)
    author_list = Authors.objects.all()
    publisher_list = Publishers.objects.all()
    wrote_list = Wrote.objects.filter(book=book_id)
    context = {'book': book,'author_list':author_list,'publisher_list':publisher_list, 'wrote_list':wrote_list}
    return render(request, 'books/book.html', context)

#does database update for ajax calls from book.html
def modifybook(request, book_id):
    title = request.GET.get("title")
    pub = request.GET.get("pub")
    #-1 is used to mark a new book
    if int(book_id)==-1:
         publisher = Publishers.objects.get(id=pub)
         book = Books(title=title, pub=publisher)
    else:
         book = Books.objects.get(book_id=book_id)
         book.title = title
         book.pub = Publishers.objects.get(id=pub)
    book.save()
    return HttpResponse(book.book_id)

#unlinks an author from a book by deleting from wrote table. called by book.html ajax
def unlink(request, wrote_id):
    link=Wrote.objects.get(id=wrote_id)  
    link.delete()
    return HttpResponse()

#links an author to a book by adding to wrote table. called by book.html ajax
def link(request):
    auth = Authors.objects.get(id=request.GET.get("auth"))
    book = Books.objects.get(book_id=request.GET.get("book"))
    wrote = Wrote(author=auth,book=book)
    wrote.save()
    return HttpResponse(str(wrote.id))

#deletes a book and all links to authors for book.  called by index.html ajax
def deletebook(request, book_id):
    book = Books.objects.get(book_id=book_id)
    Wrote.objects.filter(book=book).delete()
    book.delete()
    return HttpResponse(book.title + " deleted successfully.")

#shows author shell which wraps authors to prevent postbacks
def authshell(request):
    return render(request, 'books/authshell.html')

#returns a sorted and filterd list of authors.
def authors(request, orderby='id'):
    #these identify the next sort order to handle toggling 
    if orderby=='id': 
        idsort='-id'
        namesort='name'
    elif orderby=='-id':
        idsort='id'
        namesort='name'
    elif orderby=='name':
        idsort='id'
        namesort='-name'
    elif orderby=='-name':
        idsort='id'
        namesort='name'

    #apply a search if there is one
    search = request.GET.get("search")
    if search is None:
        search=""  #empty string will return all for icontains search
    auth_list = Authors.objects.filter(name__icontains=search).order_by(orderby)[:]

    context = {'auth_list': auth_list,'idsort':idsort,'namesort':namesort,'orderby':orderby}
    return render(request, 'books/authors.html', context)

#adds new author record.  handles ajax calls from authshell.html
def addauth(request):
    newtext = request.GET.get("newtext")
    auth=Authors(name=newtext)
    auth.save()
    return HttpResponse(str(auth.id))

#modifies author record.  handles ajax calls from authshell.html
def updateauth(request, auth_id):
    auth = Authors.objects.get(id=auth_id)
    newtext = request.GET.get("newtext")
    auth.name = newtext
    auth.save()
    return HttpResponse("Author name chaged to " +newtext)

#deletes author record.  handles ajax calls from authshell.html
def deleteauth(request, auth_id):
    auth = Authors.objects.get(id=auth_id)
    try:
        auth.delete()
        return HttpResponse(auth.name + " deleted successfully.")

    #can't delete an author if linked to a book  
    except IntegrityError as e:
        return HttpResponse(auth.name + " could not be deleted due to a referential integrity error.", status=403)

#shows pubshell which wraps publishers to prevent postbacks
def pubshell(request):
    return render(request, 'books/pubshell.html')

#returns a sorted/filtered list of publishers.  called by pubshell.html ajax
def publishers(request, orderby='id'):
    #set next sort order for toggling
    if orderby=='id': 
        idsort='-id'
        namesort='name'
    elif orderby=='-id':
        idsort='id'
        namesort='name'
    elif orderby=='name':
        idsort='id'
        namesort='-name'
    elif orderby=='-name':
        idsort='id'
        namesort='name'

    search = request.GET.get("search")
    if search is None:
        search=""
    pub_list = Publishers.objects.filter(name__icontains=search).order_by(orderby)[:]

    context = {'pub_list': pub_list,'idsort':idsort,'namesort':namesort,'orderby':orderby}
    return render(request, 'books/publishers.html', context)

#adds a new publisher to the publishers table.  handles ajax from pubshell.html
def addpub(request):
    newtext = request.GET.get("newtext")
    pub=Publishers(name=newtext)
    pub.save()
    return HttpResponse(str(pub.id))

#updates a publisher in the publishers table.  handles ajax from pubshell.html
def updatepub(request,pub_id):
    pub = Publishers.objects.get(id=pub_id)
    newtext = request.GET.get("newtext")
    pub.name = newtext
    pub.save()
    return HttpResponse("Publisher name chaged to " +newtext)

#deletes a publisher from the publishers table.  handles ajax from pubshell.html
def deletepub(request, pub_id):
    pub = Publishers.objects.get(id=pub_id)
    try:
        pub.delete()
        return HttpResponse(pub.name + " deleted successfully.")
    except IntegrityError as e:
        return HttpResponse(pub.name + " could not be deleted due to a referential integrity error.", status=403)
        

def viewauthor(request,auth_id):
    auth = Authors.objects.get(id=auth_id)
    wrote_list = Wrote.objects.filter(author_id=auth)
    followed = Follows.objects.filter(user_id=request.user.id,author_id=auth_id).count();

    user_checkouts = list(Checkouts.objects.filter(user_id=request.user.id, returned_date__isnull=True))
    books_out = [bk.book_id for bk in user_checkouts] 
    checkouts=[entry for entry in wrote_list if entry.book.book_id in books_out]
    wrote_list=[entry for entry in wrote_list if entry.book.book_id not in books_out]

    context = {'auth':auth,'wrote_list':wrote_list, 'user':request.user, 'followed':followed, 'checkouts':checkouts}
    return render(request, 'books/author.html', context)

def viewbook(request, book_id):
    book = Books.objects.get(book_id=book_id)
    author_list = Authors.objects.all()
    publisher_list = Publishers.objects.all()
    wrote_list = Wrote.objects.filter(book=book_id)
    discussion = Discusses.objects.filter(book_id=book_id);
    context = {'book': book,'author_list':author_list,'publisher_list':publisher_list, 'wrote_list':wrote_list, 'discussion':discussion}
    return render(request, 'books/viewbook.html', context)


#the list of books shown by index. performs sorting and filtering
def viewbooklist(request, orderby='book_id'):
    #these set the next sort order so clicking on column heading toggles sort
    if orderby=='title':
        titlesort='-title'
        pubsort='pub'
    elif orderby=='-title':
        titlesort='title'
        pubsort='pub'
    elif orderby=='pub':
        titlesort='title'
        pubsort='-pub'
    elif orderby=='-pub':
        titlesort='title'
        pubsort='pub'

    #get any search filter and apply it
    search = request.GET.get("search")
    if search is None:
        search=""
    wrote_list = list(Wrote.objects.order_by('book').filter(Q(book__title__icontains=search)|Q(book__pub__name__icontains=search)))

    #sort the list based on the order by
    reverse=False
    if orderby=='-title':
        reverse=True
        wrote_list = sorted(wrote_list,key= lambda x: x.book.title, reverse=reverse)
    if orderby=='pub':
        wrote_list = sorted(wrote_list,key= lambda x: x.book.pub.name, reverse=reverse)
    if orderby=='-pub':
        reverse=True
        wrote_list = sorted(wrote_list,key= lambda x: x.book.pub.name, reverse=reverse)

    user_checkouts = list(Checkouts.objects.filter(user_id=request.user.id, returned_date__isnull=True))
    books_out = [bk.book_id for bk in user_checkouts] 
    checkouts=[entry for entry in wrote_list if entry.book.book_id in books_out]
    wrote_list=[entry for entry in wrote_list if entry.book.book_id not in books_out]


    #this allows the template to not print duplicate data for books with multiple authors
    prev = 0
    for entry in checkouts:
         if entry.book == prev:
             entry.id = -1    #marks an entry to not repeat title and publisher
         prev=entry.book

    #this allows the template to not print duplicate data for books with multiple authors
    prev = 0
    for entry in wrote_list:
         if entry.book == prev:
             entry.id = -1    #marks an entry to not repeat title and publisher
         prev=entry.book


    context = {'wrote_list':wrote_list,'titlesort':titlesort,'pubsort':pubsort,'checkouts':checkouts}
    resp = render(request, 'books/viewbooklist.html', context)
    return resp

def postmessage(request):
    text = request.GET.get("text")
    book = Books.objects.get(book_id=request.GET.get("book"))
    now = datetime.datetime.now()
    
    message=Discusses(post_text=text, post_time=now,book=book, user_id=request.user.id)
    message.save()
    return HttpResponse(str(message.id))

def forum(request, book_id):
    discussion = Discusses.objects.filter(book_id=book_id);
    context = {'discussion':discussion,'user':request.user}
    return render(request, 'books/forum.html', context)

def notifications(request, user_id):
    notifications = Notifications.objects.filter(user_id=user_id);
    context = {'notifications':notifications}
    return render(request, 'books/notifications.html', context)

def follow(request, auth_id):
    follows = Follows.objects.filter(user_id=request.user.id,author_id=auth_id);
    if len(follows)==1:
        follows.delete()
        response="unfollowed"
    else:
        newfollow=Follows(user_id=request.user.id,author_id=auth_id)
        newfollow.save()
        response="followed"
    return HttpResponse(response)

def checkout(request, book_id):
    returned_book = Checkouts.objects.filter(user_id=request.user.id, book_id=book_id, returned_date__isnull=True)
    if len(returned_book) > 0:
       returned_book[0].returned_date=datetime.datetime.now()
       returned_book[0].save()
       return HttpResponse("returned");
    user_checkouts = Checkouts.objects.filter(user_id=request.user.id, returned_date__isnull=True);
    if len(user_checkouts)<5:
        checkout = Checkouts(user_id=request.user.id, book_id=book_id, due_date=datetime.datetime.now()); 
        checkout.save();
        response="checkedout";
    else:
        response="toomany";
    return HttpResponse(response)
