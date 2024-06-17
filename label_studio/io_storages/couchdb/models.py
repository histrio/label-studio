"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import json
import logging

import requests

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from io_storages.base_models import (
    ExportStorage,
    ExportStorageLink,
    ImportStorage,
    ImportStorageLink,
    ProjectStorageMixin,
)
from tasks.models import Annotation

logger = logging.getLogger(__name__)



class CouchDB():

    CHUNK_SIZE = 1000

    def __init__(self, db, charset, decode_responses, **kwargs):
        self.db = db
        self.charset = charset
        self.decode_responses = decode_responses
        self.kwargs = kwargs

        self.port = kwargs.get('port', 5984)
        self.host = kwargs.get('host', 'http://localhost')
        self.user = kwargs.get('user', 'admin')
        self.password = kwargs.get('password', 'admin')

        print(f'Connecting to {self.host}:{self.port}/{self.db} as {self.user} with {self.password}')

        # couchdb session qith requests
        self.session = requests.Session()
        self.session.auth = (self.user, self.password)


    def ping(self):
        url = f'{self.host}:{self.port}/{self.db}'
        r = self.session.get(url)
        r.raise_for_status()

    def get(self, key):
        r = self.session.get(f'{self.host}:{self.port}/{self.db}/{key}')
        r.raise_for_status()
        result = r.json()
        result.pop('_id', None)
        result.pop('_rev', None)
        return result

    def set(self, key, value):
        # Check if key exists
        r = self.session.get(f'{self.host}:{self.port}/{self.db}/{key}')
        value['_id'] = key
        if r.status_code == 200:
            # Update
            value['_rev'] = r.json()['_rev']
            r = self.session.put(f'{self.host}:{self.port}/{self.db}/{key}', json=value)
        else:
            # Create
            r = self.session.post(f'{self.host}:{self.port}/{self.db}', json=value)
        r.raise_for_status()


    def keys(self, pattern=None):
        """ Iter keys from db """
        while True:
            r = self.session.get(f'{self.host}:{self.port}/{self.db}/_all_docs?limit={self.CHUNK_SIZE}')
            r.raise_for_status()
            data = r.json().get('rows', [])
            if not data:
                break
            for row in data:
                yield row['id']
            if len(data) < self.CHUNK_SIZE:
                break


class CouchDBStorageMixin(models.Model):
    host = models.TextField(_('host'), null=True, blank=True, help_text='Server Host IP (optional)')
    port = models.TextField(_('port'), null=True, blank=True, help_text='Server Port (optional)')
    db = models.TextField(_('db'), default='tasks', help_text='Server Database')
    user = models.TextField(_('user'), null=True, blank=True, help_text='Server User (optional)')
    password = models.TextField(_('password'), null=True, blank=True, help_text='Server Password (optional)')
    prefix_filter = models.TextField(
        _('prefix'), null=True, blank=True, help_text='Cloud storage prefix for filtering objects'
    )

    def get_couchdb_connection(self, db=None, couchdb_config={}):
        """Get a couchdb connection from the provided arguments.

        Args:
            db (int): Database ID of database to use. This needs to
                      always be provided to prevent accidental overwrite
                      to a default value. Therefore, the default is None,
                      but raises an error if not provided.
            couchdb_config (dict, optional): Further couchdb configuration.

        Returns:
            CouchDB object with connection to database.
        """
        if not db:
            # This should never happen, but better to check than to accidentally
            # overwrite an existing database by choosing a wrong default:
            raise ValueError(
                'Please explicitly pass a couchdb db id to prevent accidentally overwriting existing database!'
            )

        # Since tasks are always text, we use StrictCouchDB with utf-8 decoding.
        r = CouchDB(db=db, charset='utf-8', decode_responses=True, **couchdb_config)
        # Test connection
        # (this will raise couchdb.exceptions.ConnectionError if it cannot connect)
        r.ping()
        return r

    def get_client(self):
        couchdb_config = {}
        if self.host:
            couchdb_config['host'] = self.host
        if self.port:
            couchdb_config['port'] = self.port
        if self.user:
            couchdb_config['user'] = self.user
        if self.password:
            couchdb_config['password'] = self.password

        return self.get_couchdb_connection(db=self.db, couchdb_config=couchdb_config)

    def validate_connection(self, client=None):
        if client is None:
            client = self.get_client()
        client.ping()


class CouchDBImportStorageBase(CouchDBStorageMixin, ImportStorage):

    def can_resolve_url(self, url):
        return False

    def iterkeys(self):
        client = self.get_client()
        for key in client.keys():
            yield key

    def get_data(self, key):
        client = self.get_client()
        value = client.get(key)
        if not value:
            return
        return value

    def scan_and_create_links(self):
        return self._scan_and_create_links(CouchDBImportStorageLink)


    class Meta:
        abstract = True


class CouchDBImportStorage(ProjectStorageMixin, CouchDBImportStorageBase):
    class Meta:
        abstract = False


class CouchDBExportStorage(CouchDBStorageMixin, ExportStorage):

    def save_annotation(self, annotation):
        client = self.get_client()
        logger.debug(f'Creating new object on {self.__class__.__name__} Storage {self} for annotation {annotation}')
        ser_annotation = self._get_serialized_data(annotation)

        # get key that identifies this object in storage
        key = CouchDBExportStorageLink.get_key(annotation)

        # put object into storage
        client.set(key, ser_annotation)

        # create link if everything ok
        CouchDBExportStorageLink.create(annotation, self)


@receiver(post_save, sender=Annotation)
def export_annotation_to_couchdb_storages(sender, instance, **kwargs):
    project = instance.project
    if hasattr(project, 'io_storages_couchdbexportstorages'):
        for storage in project.io_storages_couchdbexportstorages.all():
            logger.debug(f'Export {instance} to CouchDB storage {storage}')
            storage.save_annotation(instance)


class CouchDBImportStorageLink(ImportStorageLink):
    storage = models.ForeignKey(CouchDBImportStorage, on_delete=models.CASCADE, related_name='links')


class CouchDBExportStorageLink(ExportStorageLink):
    storage = models.ForeignKey(CouchDBExportStorage, on_delete=models.CASCADE, related_name='links')
