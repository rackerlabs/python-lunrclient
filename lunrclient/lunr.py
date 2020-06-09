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

from lunrclient.base import BaseAPI
import uuid


class LunrAPI(BaseAPI):

    def __init__(self, client):
        BaseAPI.__init__(self, client)
        self.client = client
        self.version = 'v1.0'

    def buildUrl(self, uri):
        return "%s/%s/%s%s" % (self.client.url, self.version,
                               self.client.tenant_id, uri)


class LunrVolume(LunrAPI):

    def list(self, **kwargs):
        """
        list all the available volumes for this tenant_id
        You can filter the results returned by the api with
        these parameters ['status', 'account_id', 'node_id', 'id']
        """
        return self.http_get('/volumes', params=kwargs)

    def get(self, volume_id):
        """
        get the details of a volume
        """
        return self.http_get('/volumes/%s' % (volume_id))

    def create(self, volume_id, vtype, size, affinity):
        """
        create a volume
        """
        volume_id = volume_id or str(uuid.uuid4())
        params = {'volume_type_name': vtype,
                  'size': size,
                  'affinity': affinity}
        return self.http_put('/volumes/%s' % volume_id,
                             params=self.unused(params))

    def restore(self, volume_id, **kwargs):
        """
        restore a volume from a backup
        """
        # These arguments are required
        self.required('create', kwargs, ['backup', 'size'])
        # Optional Arguments
        volume_id = volume_id or str(uuid.uuid4())
        kwargs['volume_type_name'] = kwargs['volume_type_name'] or 'vtype'
        kwargs['size'] = kwargs['size'] or 1
        # Make the request
        return self.http_put('/volumes/%s' % volume_id,
                             params=self.unused(kwargs))

    def delete(self, volume_id):
        """
        delete a volume
        """
        return self.http_delete('/volumes/%s' % volume_id)

    def update_status(self, volume_id, status):
        """
        Update the status of a volume
        """
        return self.http_post('/volumes/%s' % volume_id,
                              params={'status': status})

    def update_vol_node_id(self, volume_id, node_id):
        """
        update node_id of a volume
        """
        return self.http_put('/volumes/%s' % volume_id,
                              params={'node_id': node_id})

class LunrBackup(LunrAPI):

    def list(self, **kwargs):
        """
        list all the available backups for this account

        filters: status, account_id, id, volume_id
        """
        return self.http_get('/backups', params=kwargs)

    def get(self, backup_id):
        """
        get the details of a backup
        """
        return self.http_get('/backups/%s' % backup_id)

    def create(self, volume_id, backup_id):
        """
        create a backup
        """
        backup_id = backup_id or str(uuid.uuid4())
        return self.http_put('/backups/%s' % backup_id,
                             params={'volume': volume_id})

    def update(self, backup_id, params=None):
        """
        update the information on the backup
        (This does not re-create the backup on the storage node)
        """
        return self.http_post('/backups/%s' % backup_id, params=params)

    def delete(self, backup_id):
        """
        delete a backup
        """
        return self.http_delete('/backups/%s' % backup_id)


class LunrAccount(LunrAPI):

    def list(self, **kwargs):
        """
        list all the available accounts

        filters: status, id
        """
        return self.http_get('/accounts', params=kwargs)

    def get(self, account_id):
        """
        get the details of an account
        """
        return self.http_get('/accounts/%s' % account_id)

    def create(self, **kwargs):
        """
        create a new account
        """
        self.required('create', kwargs, ['id'])
        return self.http_post('/accounts', params=kwargs)

    def delete(self, account_id):
        """
        delete an account
        """
        return self.http_delete('/accounts/%s' % account_id)


class LunrNode(LunrAPI):

    def list(self, **kwargs):
        """
        list all the available nodes

        filters: name, status, volume_type_name
        """
        return self.http_get('/nodes', params=kwargs)

    def get(self, node_id):
        """
        get the details of a node
        """
        return self.http_get('/nodes/%s' % node_id)

    def create(self, name, **kwargs):
        """
        Create a new node
        """
        # These arguments are required
        self.required('create', kwargs, ['hostname', 'port',
                      'storage_hostname', 'volume_type_name', 'size'])
        kwargs['name'] = name
        return self.http_post('/nodes', params=kwargs)

    def update(self, name, **kwargs):
        """
        Create a new node
        """
        # These arguments are allowed
        self.allowed('update', kwargs, ['hostname', 'port', 'status',
                     'storage_hostname', 'volume_type_name', 'size'])
        # Remove parameters that are None
        kwargs = self.unused(kwargs)
        return self.http_post('/nodes/%s' % name, params=kwargs)

    def delete(self, node_id):
        """
        delete a node
        """
        return self.http_delete('/nodes/%s' % node_id)


class LunrExport(LunrAPI):

    def get(self, volume_id):
        """
        get the details of an export
        """
        return self.http_get('/volumes/%s/export' % volume_id)

    def create(self, volume_id, ip, initiator):
        """
        create an export for a volume
        """
        return self.http_put('/volumes/%s/export' % volume_id, params={
                             'ip': ip,
                             'initiator': initiator
                             })

    def delete(self, volume_id, force=False):
        """
        delete an export
        """
        return self.http_delete('/volumes/%s/export'
                                % volume_id, params={'force': force})

    def update(self, volume_id, **kwargs):
        """
        update an export
        """
        # These arguments are allowed
        self.allowed('update', kwargs,
                     ['status', 'instance_id',
                      'mountpoint', 'ip', 'initiator', 'session_ip',
                      'session_initiator'])
        # Remove parameters that are None
        params = self.unused(kwargs)
        return self.http_post('/volumes/%s/export' % volume_id, params=params)
