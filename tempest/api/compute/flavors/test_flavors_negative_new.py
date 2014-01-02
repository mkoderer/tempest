# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from tempest.api.compute import base
from tempest import exceptions
from tempest.test import attr


list_flavors_with_detail = \
    {"name": "list-flavors-with-detail",
     "http-method": "GET",
     "url": "flavors/detail",
     "json-schema":
        {"type": "object",
         "properties": {
                        "minRam": {"type": "integer"},
                        "minDisk": {"type": "integer"}
                        }
         }
     }


get_flavor_details = \
    {"name": "get-flavor-details",
     "http-method": "GET",
     "url": "flavors/%s",
     "resources": ["flavor"]
     }


class NewFlavorsNegativeTestJSON(base.BaseV2ComputeTest):
    _interface = 'json'
    _service = 'compute'

    @classmethod
    def setUpClass(cls):
        super(NewFlavorsNegativeTestJSON, cls).setUpClass()
        cls.client = cls.os.negative_client

    @attr(type=['negative', 'gate'])
    def test_list_flavors_with_detail(self):
        self.generate_negative(list_flavors_with_detail, self.client)

    @attr(type=['negative', 'gate'])
    def test_get_flavor_details(self):
        # flavor details are not returned for non-existent flavors
        self.generate_negative(get_flavor_details, self.client)
