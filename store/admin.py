from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# Register your models here.
from .models import Booking, Contact, Artist, Album


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'contacted']
    readonly_fields = ['created_at', 'contact', 'album', 'contacted']

    def album_link(self, booking):
        path = 'admin:store_booking_change'
        url = reverse(path, args=booking.album.id)
        return mark_safe('<a href="{}">{}</a>'.format(url, booking.album.title))

    def has_add_permission(self, request):
        return False


class AlbumArtistInline(admin.TabularInline):
    verbose_name = "Record"
    verbose_name_plural = "Records"
    model = Album.artists.through  # the query goes through intermediate table.
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]


class BookingInLine(admin.TabularInline):
    verbose_name = "Reservation"
    verbose_name_plural = "Reservations"
    model = Booking
    fieldsets = [
        (None, {'fields': ['album', 'contacted']})
    ]  # list columns
    readonly_fields = ['created_at', 'contacted', 'album']

    def has_add_permission(self, request, obj):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInLine,]  # list of bookings made by a contact


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
