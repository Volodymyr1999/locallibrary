from django.shortcuts import render
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import datetime

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits',0)

    request.session['num_visits'] = num_visits+1
    return render(request, 'index.html',
                  context={'num_books': num_books, 'num_instances': num_instances,
                                   'num_instances_available': num_instances_available, 'num_authors': num_authors,
                           'num_visits': num_visits})


class BookListView(generic.ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"


class AuthorListView(generic.ListView):
    model = Author
    template_name = "author_list.html"
    paginate_by = 10





class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"


class LoanBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LibrarianLoanBookListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = "all_borrowed_books.html"
    paginate_by = 10

    permission_required = "catalog.can_mark_returned"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    template_name = "create_author.html"
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016'}
    permission_required = "catalog.can_author_edit"


class UpdateAuthor(PermissionRequiredMixin,UpdateView):
    model = Author
    template_name = "update_author.html"
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = "catalog.can_author_edit"


class DeleteAuthor(PermissionRequiredMixin,DeleteView):
    model = Author
    template_name = "delete_author_confirm.html"
    success_url = reverse_lazy('authors')
    permission_required = "catalog.can_author_edit"

