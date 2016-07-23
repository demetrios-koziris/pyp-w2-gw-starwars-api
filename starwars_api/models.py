from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError
import json

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        result = json_data.items()
        for key, value in result:
            setattr(self, key, value)


    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        get_method = getattr(api_client, 'get_'+cls.RESOURCE_NAME)
        json_result = get_method(resource_id)
        return cls(json_result)
        

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        return BaseQuerySet(cls)


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)
        
        
class Planets(BaseModel):
    RESOURCE_NAME = 'planets'

    def __init__(self, json_data):
        super(Planets, self).__init__(json_data)

    def __repr__(self):
        return 'Planets: {0}'.format(self.name)


class BaseQuerySet(object):

    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.counter = 0
        self.get_page = getattr(api_client, 'get_'+self.model_cls.RESOURCE_NAME)
        self.current_page = self.get_page(page=1)


    def __iter__(self):
        self.counter = 0
        self.current_page = self.get_page(page=1)
        return self

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        if self.counter < len(self.current_page['results']):
            model_json = self.current_page['results'][self.counter]
            model_object = self.model_cls(model_json)
            self.counter += 1
            return model_object
        try:
            next_page_num = self.current_page['next'].split('page=')[1]
            self.current_page = self.get_page(page=next_page_num)
            self.counter = 0
            return self.next()
        except:
            raise StopIteration()
    

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        return self.current_page['count']


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))


class PlanetsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'planets'

    def __init__(self):
        super(PlanetsQuerySet, self).__init__()

    def __repr__(self):
        return 'PlanetsQuerySet: {0} objects'.format(str(len(self.objects)))