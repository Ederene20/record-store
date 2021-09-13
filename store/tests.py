from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    # Ran before each test
    def setUp(self):
        impossible = Album.objects.create(title='Transmission impossible')
        self.album = Album.objects.get(title="Transmission impossible")

    # Test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    # Test that detail page returns a 404 if the item does not exist
    def test_detail_page_returns_404(self):
        album_id = self.album.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)


class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name="Frederic", email="fred@queen.forever")
        impossible = Album.objects.create(title='Transmission impossible')
        journey = Artist.objects.create(name='Journey')
        impossible.artists.add(journey)
        self.album = Album.objects.get(title='Transmission impossible')
        self.contact = Contact.objects.get(name="Frederic")

    # test that a new booking is made
    def test_new_booking_is_registered(self):
        old_bookings = Booking.objects.count()  # count booking before a request
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings, old_bookings + 1)  # make sure 1 booking was added
