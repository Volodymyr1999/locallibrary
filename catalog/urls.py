from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns=[
    path('', views.index,name='index'),
    url(r'^books/$', views.BookListView.as_view(), name="books"),
    url(r'^authors/$', views.AuthorListView.as_view(),name="authors"),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name="book-detail"),
    url(r'^author/(?P<pk>\d+)$',views.AuthorDetailView.as_view(), name="author-detail"),

]

urlpatterns+=[
    url(r'^mybooks/$', views.LoanBookByUserListView.as_view(), name='my-borrowed'),
    url(r'^borrowed-books/$',views.LibrarianLoanBookListView.as_view(),name='borrowed'),
]

urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.UpdateAuthor.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.DeleteAuthor.as_view(), name='author_delete'),
]
