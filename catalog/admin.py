from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


# Book знизу
class BookInline(admin.StackedInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
     list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
     fields = ('first_name', 'last_name', ('date_of_birth','date_of_death'))
     inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)


# BookInstance знизу
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'id', 'status','borrower', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = ((None, {'fields': ('book', 'imprint', 'id')}), ('Availability', {'fields': ('status', 'due_back',
                                                                                             'borrower')}))
