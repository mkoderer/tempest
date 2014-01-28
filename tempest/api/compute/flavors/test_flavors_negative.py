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

import testscenarios

from tempest.api.compute import base
import tempest.api.compute.flavors.api_schema as schema
from tempest import test


load_tests = testscenarios.load_tests_apply_scenarios


class FlavorsListNegativeTestNewJSON(base.BaseV2ComputeTest,
                                     test.NegativeAutoTest):
    _interface = 'json'
    _service = 'compute'

    _description = schema.FlavorsListJSON

    scenarios = test.NegativeAutoTest.generate_scenario(_description)

    @test.attr(type=['negative', 'gate'])
    def test_list_flavors_with_detail(self):
        self.execute(self._description)


class FlavorDetailsNegativeTestNewJSON(base.BaseV2ComputeTest,
                                       test.NegativeAutoTest):
    _interface = 'json'
    _service = 'compute'

    _description = schema.FlavorDetailsJSON

    scenarios = test.NegativeAutoTest.generate_scenario(_description)

    @classmethod
    def setUpClass(cls):
        super(FlavorDetailsNegativeTestNewJSON, cls).setUpClass()
        cls.set_resource("flavor", cls.flavor_ref)

    @test.attr(type=['negative', 'gate'])
    def test_get_flavor_details(self):
        # flavor details are not returned for non-existent flavors
        self.execute(self._description)
