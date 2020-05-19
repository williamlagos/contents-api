#!/usr/bin/python
#
# This file is part of django-emporio project.
#
# Copyright (C) 2011-2020 William Oliveira de Lagos <william.lagos@icloud.com>
#
# Emporio is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Emporio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Emporio. If not, see <http://www.gnu.org/licenses/>.
#

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToOneRel, RelatedField
from restless.dj import DjangoResource
from restless.exceptions import NotFound, BadRequest
from restless.preparers import FieldsPreparer, SubPreparer

isnot_fk = lambda field: not isinstance(field, (RelatedField, ManyToOneRel))
# nested = lambda f: {f.name: f.name for f in f.remote_field.model._meta.get_fields() if isnot_fk(f)}

class DefaultServiceResource(DjangoResource):
    
    service = None

    def __init__(self, *args, **kwargs):
        super(DefaultServiceResource, self).__init__(self, args, kwargs)
        self.fields = {}
        for field in self.service.model._meta.get_fields():
            if isnot_fk(field):
                self.fields[field.name] = field.name
            else:
                nested_field_names = field.remote_field.model._meta.get_fields()
                nested_fields = {f.name: f.name for f in nested_field_names if isnot_fk(f)}
                self.fields[field.name] = SubPreparer(field.name, FieldsPreparer(nested_fields)) 
        # model_fields = self.service.model._meta.get_fields()
        # flat_fields = {f.name: f.name for f in model_fields if isnot_fk(f)}
        # nested_fields = {f.name: SubPreparer(f.name, FieldsPreparer(nested(f))) for f in model_fields if not isnot_fk(f)}
        # self.fields = {**nested_fields, **flat_fields}
        self.preparer = FieldsPreparer(self.fields)

    # Add this!
    def is_authenticated(self):
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        return True

        # Alternatively, if the user is logged into the site...
        # return self.request.user.is_authenticated()

        # Alternatively, you could check an API key. (Need a model for this...)
        # from myapp.models import ApiKey
        # try:
        #     key = ApiKey.objects.get(key=self.request.GET.get('api_key'))
        #     return True
        # except ApiKey.DoesNotExist:
        #     return False

    def list(self):
        print(self.preparer)
        print(self.fields)
        return self.service.list()

    def detail(self, pk):
        try:
            return self.service.detail(pk)
        except ObjectDoesNotExist:
            raise NotFound()

    def create(self):
        return self.service.create(self.data)

    def update(self, pk):
        return self.service.update(pk, self.data)

    def delete(self, pk):
        self.service.delete(pk)