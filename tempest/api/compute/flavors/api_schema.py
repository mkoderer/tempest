# Copyright 2014 Red Hat, Inc.
# Copyright 2014 Deutsche Telekom AG
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


FlavorsListJSON = {
    "name": "list-flavors-with-detail",
    "http-method": "GET",
    "url": "flavors/detail",
    "json-schema": {
        "type": "object",
        "properties": {
            "minRam": {
                "type": "integer",
                "results": {
                    "gen_none": 400,
                    "gen_string": 400
                }
            },
            "minDisk": {
                "type": "integer",
                "results": {
                    "gen_none": 400,
                    "gen_string": 400
                }
            }
        }
    }
}

FlavorDetailsJSON = {
    "name": "get-flavor-details",
    "http-method": "GET",
    "url": "flavors/%s",
    "resources": ["flavor"]
}
