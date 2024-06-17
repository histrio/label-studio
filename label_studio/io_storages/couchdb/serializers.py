"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import os

from io_storages.couchdb.models import CouchDBExportStorage, CouchDBImportStorage
from io_storages.serializers import ExportStorageSerializer, ImportStorageSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CouchDBImportStorageSerializer(ImportStorageSerializer):
    type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

    class Meta:
        model = CouchDBImportStorage
        fields = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password')
        return result

    def validate(self, data):
        data = super(CouchDBImportStorageSerializer, self).validate(data)

        storage = CouchDBImportStorage(**data)
        try:
            storage.validate_connection()
        except:  # noqa: E722
            raise ValidationError("Can't connect to CouchDB server.")
        return data


class CouchDBExportStorageSerializer(ExportStorageSerializer):
    type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password')
        return result

    class Meta:
        model = CouchDBExportStorage
        fields = '__all__'
