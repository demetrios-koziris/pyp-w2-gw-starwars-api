import responses

from tests import BaseStarWarsAPITestCase
from starwars_api.exceptions import SWAPIClientError
from starwars_api.models import *


class ModelsTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_people_model(self):
        luke = People.get(1)
        self.assertEqual(luke.name, 'Luke Skywalker')
        self.assertEqual(luke.height, '172')
        self.assertEqual(luke.mass, '77')
        self.assertEqual(luke.hair_color, 'blond')
        self.assertEqual(luke.skin_color, 'fair')
        self.assertEqual(luke.eye_color, 'blue')
        self.assertEqual(luke.birth_year, '19BBY')
        self.assertEqual(luke.gender, 'male')

    @responses.activate
    def test_people_model_not_found(self):
        error = ('Request to SWAPI "/api/people/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            People.get(100)
    
    @responses.activate
    def test_film_model(self):
        new_hope = Films.get(1)
        self.assertEqual(new_hope.title, 'A New Hope')
        self.assertEqual(new_hope.episode_id, 4)
        self.assertEqual(new_hope.director, 'George Lucas')
        self.assertEqual(new_hope.producer, 'Gary Kurtz, Rick McCallum')
        self.assertEqual(new_hope.release_date, '1977-05-25')

    @responses.activate
    def test_film_model_not_found(self):
        error = ('Request to SWAPI "/api/films/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            Films.get(100)
    
    
    @responses.activate
    def test_planet_model(self):
        Hoth = Planets.get(1)
        self.assertEqual(Hoth.name, 'Tatooine')
        self.assertEqual(Hoth.rotation_period, '23')
        self.assertEqual(Hoth.orbital_period, '304')
        self.assertEqual(Hoth.diameter, '10465')
        self.assertEqual(Hoth.climate, 'arid')

    @responses.activate
    def test_planet_model_not_found(self):
        error = ('Request to SWAPI "/api/planets/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            Planets.get(100)


class QuerySetTestCase(BaseStarWarsAPITestCase):


    @responses.activate
    def test_people_qs_next(self):
        qs = People.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, People))
        self.assertEqual(obj.name, 'Luke Skywalker')

    @responses.activate
    def test_people_qs_iterable(self):
        qs = People.all()
        self.assertEqual(len([elem for elem in qs]), 15)  # 10 in page1, 5 in page2, 0 in page3

    @responses.activate
    def test_people_qs_count(self):
        qs = People.all()
        self.assertEqual(qs.count(), 15)
        
        
    @responses.activate
    def test_films_qs_next(self):
        qs = Films.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, Films))
        self.assertEqual(obj.title, 'A New Hope')

    @responses.activate
    def test_films_qs_iterable(self):
        qs = Films.all()
        self.assertEqual(len([elem for elem in qs]), 7)  # 7 in page1, 0 in page2

    @responses.activate
    def test_films_qs_count(self):
        qs = Films.all()
        self.assertEqual(qs.count(), 7)


    @responses.activate
    def test_planets_qs_next(self):
        qs = Planets.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, Planets))
        self.assertEqual(obj.name, 'Tatooine')

    @responses.activate
    def test_planets_qs_iterable(self):
        qs = Planets.all()
        self.assertEqual(len([elem for elem in qs]), 13)  # 10 in page1, 3 in page2

    @responses.activate
    def test_planet_qs_count(self):
        qs = Planets.all()
        self.assertEqual(qs.count(), 13)
        