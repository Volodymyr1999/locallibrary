from django.test import TestCase
from catalog.models import Author,Genre,Language,Book,BookInstance
from django.urls import reverse
from django.contrib.auth.models import Permission,User
import datetime
class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors=13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name='Christian %s'%author_num, last_name='Surname %s'%author_num)



    def test_view_url_exist_at_desired_location(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code,200)

    def test_view_accesible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code,200)

    def test_view_uses_correct_template(self):
        resp=self.client.get(reverse('authors'))

        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp, 'author_list.html')

    def test_pagination_is_10(self):
        resp=self.client.get(reverse('authors'))

        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated']==True)
        self.assertTrue(len(resp.context['author_list'])==10)


    def test_list_second_page(self):
        resp=self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated']==True)
        self.assertTrue(len(resp.context['author_list'])==3)


class RenewBookInstanceViewTest(TestCase):

    def setUp(self):
        test_user1=User.objects.create_user(username='testuser1',password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # create book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(title='Book Title', summary='My book summary', isbn='ABCDEFG',
                                        author=test_author, language=test_language, )
        genre_objects_for_book = Genre.objects.all()
        test_book.genre=genre_objects_for_book
        test_book.save()

        return_date = datetime.date.today() + datetime.timedelta(days=5)

        self.test_bookinstance1 = BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016',
                                                              due_back=return_date, borrower=test_user1, status='o')
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016',
                                                              due_back=return_date, borrower=test_user2, status='o')

