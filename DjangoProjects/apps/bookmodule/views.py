from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Student, Address,Publisher
# Create your views here.
from django.http import HttpResponse
'''def index(request):
   # return HttpResponse("Hello, world!")
   name = request.GET.get("name") or "world!" #add this line
   #return HttpResponse("Hello, "+name) #replace the word “world!” with the variable nam
   #return render(request, "bookmodule/index.html")
   return render(request, "bookmodule/index.html" , {"name": name}) '''

def index2(request, val1 = 0): #add the view function (index2)
   return HttpResponse("value1 = "+str(val1))

def viewbook(request, bookId):
# assume that we have the following books somewhere (e.g. database)
  book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
  book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
  targetBook = None
  if book1['id'] == bookId: targetBook = book1
  if book2['id'] == bookId: targetBook = book2
  context = {'book':targetBook} # book is the variable name accessible by the template
  return render(request, 'bookmodule/show.html', context)
def index(request):
  return render(request, "bookmodule/index.html")
def list_books(request):
  return render(request, 'bookmodule/list_books.html')
def viewbook(request, bookId):
  return render(request, 'bookmodule/one_book.html')
def aboutus(request):
  return render(request, 'bookmodule/aboutus.html')

def html5_links(request):
    return render(request, "bookmodule/html5_links.html")

def html5_text_formatting(request):
    return render(request, "bookmodule/html5_text_formatting.html")

def html5_listing(request):
    return render(request, "bookmodule/html5_listing.html")

def html5_tables(request):
    return render(request, "bookmodule/html5_tables.html")

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765, 'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

def insert_book(request):
    mybook = Book(
        title='Continuous Delivery',
        author='J.Humble and D. Farley',
        price=50,
        edition=1
    )
    mybook.save()

    return HttpResponse("Book inserted successfully")

def insert_book2(request):
    mybook = Book.objects.create(
        title='Clean Code',
        author='Robert Martin',
        price=60,
        edition=1
    )
    mybook.save()
    return HttpResponse("Book inserted successfully")

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False
    ).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(
        price__lte=100
    )[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__contains='qu') | Q(author__contains='qu'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) & (~Q(title__contains='qu') | ~Q(author__contains='qu'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        count=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/bookStats.html', {'stats': stats})

def lab8_task7(request):
    cities = Address.objects.all()
    return render(request, 'bookmodule/studentCities.html', {'cities': cities})

def lab9_task1(request):
    total_books = Book.objects.aggregate(total=Sum('quantity'))['total'] or 1

    books = Book.objects.all()

    for book in books:
        book.availability = (book.quantity / total_books) * 100

    return render(request, 'bookmodule/task1.html', {'books': books})


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        stock_counter=Count("book")
    )

    return render(request, 'bookmodule/task2.html', {'publishers': publishers})

def lab9_task3(request):
    publishers = Publisher.objects.annotate(
        oldest_pubdate=Min("book__pubdate")
    )

    return render(request, 'bookmodule/task3.html', {'publishers': publishers})


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg("book__price"),
        min_price=Min("book__price"),
        max_price=Max("book__price")
    )

    return render(request, 'bookmodule/task4.html', {'publishers': publishers})

from django.db.models import Count, Q

def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        quantity=Count('book', filter=Q(book__rating__gte=7))
    )
    return render(request, 'bookmodule/task5.html', {'publishers': publishers})

def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        book_count=Count(
            'book',
            filter=Q(
                book__price__gt=50,
                book__quantity__lt=5,
                book__quantity__gte=1
            )
        )
    )

    return render(request, 'bookmodule/task6.html', {'publishers': publishers})