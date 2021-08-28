from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Album, Artist, Contact, Booking


# Create your views here.


def index(request):
    # request album
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        'albums': albums
    }
    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Album.objects.filter(available=True)
    # Slice pages
    paginator = Paginator(albums_list, 6)
    # Get the current page number
    page = request.GET.get('page')
    # Return only this page number and not others
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page not an integer, deliver first page
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginator': True
    }
    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    id = int(album_id)
    # album = Album.objects.get(pk=id)
    album = get_object_or_404(Album, pk=id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')

        contact = Contact.objects.get(email=email)

        if not contact:
            # If contact is not registered yet, create a new one.
            contact = Contact.objects.create(email=email, name=name)

        # If no album matches the id, it means the form must have been tweaked
        album = get_object_or_404(Album, id=album_id)
        booking = Booking.objects.create(
            contact=contact,
            album=album
        )
        # Make sure no one can book the album again
        album.available = False
        album.save()
        context = {
            'album_title': album.title
        }

        return render(request, 'store/merci.html', context)

    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
        'available': album.available
    }
    return render(request, 'store/detail.html', context)


def search(request):
    # query = request.GET['name']
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    context = {
        "albums": albums,
        "title": f"Résultat de la requête: {query}"
    }

    return render(request, 'store/search.html', context)


def booked(request):
    albums = Album.objects.filter(available=False)
    context = {
        'albums': albums
    }
    return render(request, 'store/booked.html', context)
