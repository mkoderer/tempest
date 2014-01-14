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

import testscenarios

from tempest.api.compute import base
from tempest import test


load_tests = testscenarios.load_tests_apply_scenarios


class GetConsoleOutputNegativeTestJSON(base.BaseV2ComputeTest,
                                       test.NegativeAutoTest):
    _interface = 'json'
    _service = 'compute'

    _description = \
        {"name": "get-console-output",
         "http-method": "POST",
         "url": "servers/%s/action",
         "resources": ["server"],
         "json-schema":
            {"type": "object",
             "properties":
             {"os-getConsoleOutput":
              {"type": "object",
               "properties":
               {"length": {"type": ["integer", "string"],
                           "minimum": 0
                           }
                }
               }
              },
            "additionalProperties": False
            }
         }

    scenarios = test.NegativeAutoTest.generate_scenario(_description)

    @classmethod
    def setUpClass(cls):
        super(GetConsoleOutputNegativeTestJSON, cls).setUpClass()
        _resp, server = cls.create_test_server()
        cls.set_resource("server", server['id'])

    @test.attr(type=['negative', 'gate'])
    def test_get_console_output(self):
        self.execute(self._description, self.client)
