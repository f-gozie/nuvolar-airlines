from uuid import UUID

from django.db.models import Model

from nuvolar_airlines.contrib import exceptions as airspace_exceptions


class BaseService:
    def __init__(self):
        self.model = Model

    def get_obj_by_public_id(
        self, public_id: UUID, raise_exception: bool = True
    ) -> type[Model]:
        objs = self.model.objects.filter(public_id=public_id)
        if not objs and raise_exception:
            raise airspace_exceptions.DoesNotExist(
                klass=self.model.__name__, public_id=public_id
            )
        return objs.first()
