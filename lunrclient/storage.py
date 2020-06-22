# Copyright 2011-2016 Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import time

from lunrclient.base import BaseAPI


class StorageAPI(BaseAPI):

    def __init__(self, client):
        BaseAPI.__init__(self, client)
        self.version = 'v1.0'

    def buildUrl(self, uri):
        return "%s%s" % (self.client.url, uri)


class StorageStatus(StorageAPI):

    def list(self):
        """
        Return stats on the api status
        """
        return self.http_get('/status')

    def api(self):
        """
        Return stats on the api status
        """
        return self.http_get('/status/api')

    def conf(self):
        """
        Return the storage node configuration
        """
        return self.http_get('/status/conf')


class StorageVolume(StorageAPI):

    def list(self):
        """
        list all available volumes on the storage node
        """
        return self.http_get('/volumes')

    def get(self, volume_id):
        """
        get the details of a volume
        """
        return self.http_get('/volumes/%s' % volume_id)

    def create(self, size, volume_id=None):
        """
        create a volume of the specified size
        """
        volume_id = volume_id or str(uuid.uuid4())
        return self.http_put('/volumes/%s' % volume_id,
                             params=self.unused({'size': size}))

    def clone(self, source_id, backup_id, size,
              volume_id=None, source_host=None):
        """
        create a volume then clone the contents of
        the backup into the new volume
        """
        volume_id = volume_id or str(uuid.uuid4())
        return self.http_put('/volumes/%s' % volume_id,
                             params=self.unused({
                                 'source_host': source_host,
                                 'source_volume_id': source_id,
                                 'backup_id': backup_id,
                                 'size': size
                             }))

    def delete(self, volume_id):
        """
        delete a volume
        """
        return self.http_delete('/volumes/%s' % volume_id)

    def audit(self, volume_id):
        """
        Run an audit job that compares the backup manifest with the blocks
        stored in swift, deleting any blocks that are no longer in the manifest
        """
        return self.http_put('/volumes/%s/audit' % volume_id)

    def lock(self, volume_id):
        """
        Get lock file info for a volume
        """
        return self.http_get('/volumes/%s/lock' % volume_id)

    def rename(self, volume_id, new_volume_id):
        """
       Renames lunr volume
        """
        return self.http_put('/volumes/%s/rename' % volume_id,
                             params=self.unused({'new_name': new_volume_id}))

class StorageBackup(StorageAPI):

    def list(self, volume_id):
        """
        list all the available backups for this volume
        """
        return self.http_get('/volumes/%s/backups' % volume_id)

    def get(self, volume_id, backup_id):
        """
        get the details of a backup
        """
        return self.http_get('/volumes/%s/backups/%s' % (volume_id, backup_id))

    def create(self, volume_id, backup_id=None, timestamp=None):
        """
        create a backup of a volume
        """
        backup_id = backup_id or str(uuid.uuid4())
        timestamp = timestamp or int(time())
        return self.http_put('/volumes/%s/backups/%s' % (volume_id, backup_id),
                             params={'timestamp': timestamp})

    def delete(self, volume_id, backup_id):
        """
        delete the specified backup
        """
        return self.http_delete('/volumes/%s/backups/%s' %
                                (volume_id, backup_id))


class StorageExport(StorageAPI):

    def get(self, volume_id):
        """
        get the details of an export
        """
        return self.http_get('/volumes/%s/export' % volume_id)

    def create(self, volume_id, ip=None):
        """
        create an export for a volume
        """
        if ip:
            return self.http_put('/volumes/%s/export?ip=%s' % (volume_id, ip))
        return self.http_put('/volumes/%s/export' % volume_id)

    def delete(self, volume_id, force=False):
        """
        delete an export
        """
        return self.http_delete('/volumes/%s/export' % volume_id,
                                params={'force': force})
