from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^main/$', views.main, name='main'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^discussion/(?P<book_id>[0-9]+)/$', views.discussion, name='discussion'),
    
###############################################################
#Administrator pages
###############################################################
    url(r'^index/$', views.index, name='index'),         # shell for main book list
    url(r'^index/orderby/(?P<orderby>-?title|-?pub)$', views.booklist, name='booklist'),    #responds to ajax call to populate index

    #pages for the publisher list
    url(r'^pub/$', views.pubshell, name='pubshell'),     #shell for publishers list
    url(r'^publishers/$', views.publishers, name='publishers'),   #responds to ajax call to populate publisher list
    url(r'^publishers/orderby/(?P<orderby>-?pub\_id|-?name)$', views.publishers, name='sortedpublishers'),  #responds to ajax call to populate publisher list
    url(r'^publishers/addpub$', views.addpub, name='addpublishers'),
    url(r'^publishers/deletepub/(?P<pub_id>[0-9]+)$', views.deletepub, name='deletepub'),
    url(r'^publishers/updatepub/(?P<pub_id>[0-9]+)$', views.updatepub, name='updatepub'),

    #pages for the author list
    url(r'^auth/$', views.authshell, name='authshell'),  #shell for authors list
    url(r'^authors/$', views.authors, name='authors'),
    url(r'^authors/addauth$', views.addauth, name='addauthors'),
    url(r'^authors/orderby/(?P<orderby>-?auth\_id|-?name)$', views.authors, name='sortedauthors'),
    url(r'^authors/deleteauth/(?P<auth_id>[0-9]+)$', views.deleteauth, name='deleteauth'),
    url(r'^authors/updateauth/(?P<auth_id>[0-9]+)$', views.updateauth, name='updateauth'),

    #pages for the single book view 
    url(r'^book/(?P<book_id>[0-9]+)$', views.updatebook, name='updatebook'),
    url(r'^book/modify/(?P<book_id>[0-9]+)$', views.modifybook, name='modifybook'),
    url(r'^book/modify/(?P<book_id>-1)$', views.modifybook, name='modifybook'),
    url(r'^book/unlink/(?P<wrote_id>[0-9]+)$', views.unlink, name='unlink'),
    url(r'^book/link$', views.link, name='link'),
    url(r'^book/deletebook/(?P<book_id>[0-9]+)$', views.deletebook, name='deletebook'),
    url(r'^book/add/$', views.addbook, name='addbook'),

###############################################################
#User pages
###############################################################
    #pages for user booklist
    url(r'^viewindex/$', views.viewindex, name='index'),
    url(r'^view/orderby/(?P<orderby>-?title|-?pub)$', views.viewbooklist, name='viewbooklist'),
    url(r'^notifications/(?P<user_id>[0-9]+)$', views.notifications, name='notifications'),

    #single author view with follow button
    url(r'^author/view/(?P<auth_id>[0-9]+)$', views.viewauthor, name='viewauthor'),
    url(r'^follow/(?P<auth_id>[0-9]+)$', views.follow, name='follow'),

    #single book view with forum
    url(r'^book/view/(?P<book_id>[0-9]+)$', views.viewbook, name='viewbook'),
    url(r'^forum/(?P<book_id>[0-9]+)$', views.forum, name='forum'),
    url(r'^message/post/$', views.postmessage, name='postmessage'),

    #handles checkouts from booklist and author views
    url(r'^checkout/(?P<book_id>[0-9]+)$', views.checkout, name='checkout'),
]
