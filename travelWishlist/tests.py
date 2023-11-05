

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from .models import Place


class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self=None):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travelWishlist/wishlist.html')
        self.assertContains(response, "You have no places in your wishlist")

class TestWishList(TestCase):
    fixtures = ['tests_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travelWishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')

class TestVisitedPage(TestCase):
    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travelWishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class VisitedList(TestCase):
    fixtures = ('test_places')

    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travelWishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

class TestAddNewPlace(TestCase):
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.posta(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travelWishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))
        tokyo_from_response = response_places[0]

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_database, tokyo_from_response)

class TestVisitPlace(TestCase):
    fixtures = ['test_place']

    def test_visit_place(self, true=None):
        visit_place_url = reverse('place_was_visited', args=(2,))
        response = self.client.post(visit_place_url, follow=true)

        self.assertTemplateUsed(response, 'travelWishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited, args=(123456, ')
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)

# Create your tests here.
