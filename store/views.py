from django.shortcuts import render
from django.http import HttpResponse
from .models import Album, Artist, Contact, Booking

# Create your views here.


def index(request):
    # request album
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    # then format the request
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return HttpResponse(message)


def listing(request):
    albums = Album.objects.filter(available=True)
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return HttpResponse(message)


def detail(request, album_id):
    id = int(album_id)
    album = Album.objects.get(pk=id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = f"Le nom de l'album est {album.title}. Il a été écrit par {artists}"
    return HttpResponse(message)


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

        if not albums.exists():
            message = "Quel dommage, Nous n'avons trouvé aucun résultat !"

        else:
            albums = ["<li>{}</li>".format(album.title) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("<li></li>".join(albums))
    return HttpResponse(message)
