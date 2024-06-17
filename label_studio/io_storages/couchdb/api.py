"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.utils.decorators import method_decorator
from drf_yasg import openapi as openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from io_storages.api import (
    ExportStorageDetailAPI,
    ExportStorageFormLayoutAPI,
    ExportStorageListAPI,
    ExportStorageSyncAPI,
    ExportStorageValidateAPI,
    ImportStorageDetailAPI,
    ImportStorageFormLayoutAPI,
    ImportStorageListAPI,
    ImportStorageValidateAPI,
)
from io_storages.couchdb.models import CouchDBExportStorage, CouchDBImportStorage
from io_storages.couchdb.serializers import CouchDBExportStorageSerializer, CouchDBImportStorageSerializer

from .openapi_schema import (
    _couchdb_export_storage_schema,
    _couchdb_export_storage_schema_with_id,
    _couchdb_import_storage_schema,
    _couchdb_import_storage_schema_with_id,
)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='list',
        x_fern_audiences=['public'],
        operation_summary='Get all import storage',
        operation_description='Get a list of all CouchDB import storage connections.',
        manual_parameters=[
            openapi.Parameter(
                name='project',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description='Project ID',
            ),
        ],
        request_body=no_body,
    ),
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='create',
        x_fern_audiences=['public'],
        operation_summary='Create import storage',
        operation_description='Create a new CouchDB import storage connection.',
        request_body=_couchdb_import_storage_schema,
    ),
)
class CouchDBImportStorageListAPI(ImportStorageListAPI):
    queryset = CouchDBImportStorage.objects.all()
    serializer_class = CouchDBImportStorageSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='get',
        x_fern_audiences=['public'],
        operation_summary='Get import storage',
        operation_description='Get a specific CouchDB import storage connection.',
        request_body=no_body,
    ),
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='update',
        x_fern_audiences=['public'],
        operation_summary='Update import storage',
        operation_description='Update a specific CouchDB import storage connection.',
        request_body=_couchdb_import_storage_schema,
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='delete',
        x_fern_audiences=['public'],
        operation_summary='Delete import storage',
        operation_description='Delete a specific CouchDB import storage connection.',
        request_body=no_body,
    ),
)
class CouchDBImportStorageDetailAPI(ImportStorageDetailAPI):
    queryset = CouchDBImportStorage.objects.all()
    serializer_class = CouchDBImportStorageSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='sync',
        x_fern_audiences=['public'],
        operation_summary='Sync import storage',
        operation_description='Sync tasks from a specific CouchDB import storage connection.',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_PATH,
                description='Storage ID',
            ),
        ],
        request_body=no_body,
    ),
)
class CouchDBImportStorageSyncAPI(ExportStorageSyncAPI):
    serializer_class = CouchDBImportStorageSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='sync',
        x_fern_audiences=['public'],
        operation_summary='Sync export storage',
        operation_description='Sync tasks from a specific CouchDB export storage connection.',
        request_body=no_body,
    ),
)
class CouchDBExportStorageSyncAPI(ExportStorageSyncAPI):
    serializer_class = CouchDBExportStorageSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['import_storage', 'couchdb'],
        x_fern_sdk_method_name='validate',
        x_fern_audiences=['public'],
        operation_summary='Validate import storage',
        operation_description='Validate a specific CouchDB import storage connection.',
        request_body=_couchdb_import_storage_schema_with_id,
        responses={200: openapi.Response(description='Validation successful')},
    ),
)
class CouchDBImportStorageValidateAPI(ImportStorageValidateAPI):
    serializer_class = CouchDBImportStorageSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='validate',
        x_fern_audiences=['public'],
        operation_summary='Validate export storage',
        operation_description='Validate a specific CouchDB export storage connection.',
        request_body=_couchdb_export_storage_schema_with_id,
        responses={200: openapi.Response(description='Validation successful')},
    ),
)
class CouchDBExportStorageValidateAPI(ExportStorageValidateAPI):
    serializer_class = CouchDBExportStorageSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='list',
        x_fern_audiences=['public'],
        operation_summary='Get all export storage',
        operation_description='Get a list of all CouchDB export storage connections.',
        manual_parameters=[
            openapi.Parameter(
                name='project',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description='Project ID',
            ),
        ],
        request_body=no_body,
    ),
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='create',
        x_fern_audiences=['public'],
        operation_summary='Create export storage',
        operation_description='Create a new CouchDB export storage connection to store annotations.',
        request_body=_couchdb_export_storage_schema,
    ),
)
class CouchDBExportStorageListAPI(ExportStorageListAPI):
    queryset = CouchDBExportStorage.objects.all()
    serializer_class = CouchDBExportStorageSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='get',
        x_fern_audiences=['public'],
        operation_summary='Get export storage',
        operation_description='Get a specific CouchDB export storage connection.',
        request_body=no_body,
    ),
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='update',
        x_fern_audiences=['public'],
        operation_summary='Update export storage',
        operation_description='Update a specific CouchDB export storage connection.',
        request_body=_couchdb_export_storage_schema,
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        tags=['Storage: CouchDB'],
        x_fern_sdk_group_name=['export_storage', 'couchdb'],
        x_fern_sdk_method_name='delete',
        x_fern_audiences=['public'],
        operation_summary='Delete export storage',
        operation_description='Delete a specific CouchDB export storage connection.',
        request_body=no_body,
    ),
)
class CouchDBExportStorageDetailAPI(ExportStorageDetailAPI):
    queryset = CouchDBExportStorage.objects.all()
    serializer_class = CouchDBExportStorageSerializer


class CouchDBImportStorageFormLayoutAPI(ImportStorageFormLayoutAPI):
    pass


class CouchDBExportStorageFormLayoutAPI(ExportStorageFormLayoutAPI):
    pass
