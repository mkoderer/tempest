# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack Foundation
# Copyright 2013 IBM Corp.
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

import copy
import json
import jsonschema
import os

from tempest.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def generate_valid(schema):
    """
    Create a valid dictionary based on the types in a json schema.
    """
    LOG.debug("generate_valid: %s" % schema)
    schema_type = schema["type"]
    if isinstance(schema_type, list):
        # Just choose the first one since all are valid.
        schema_type = schema_type[0]
    return type_map_valid[schema_type](schema)


def generate_valid_string(schema):
    size = schema.get("minLength", 0)
    # TODO(dkr mko): handle format and pattern
    return "x" * size


def generate_valid_integer(schema):
    # TODO(dkr mko): handle multipleOf
    if "minimum" in schema:
        minimum = schema["minimum"]
        if "exclusiveMinimum" not in schema:
            return minimum
        else:
            return minimum + 1
    if "maximum" in schema:
        maximum = schema["maximum"]
        if "exclusiveMaximum" not in schema:
            return maximum
        else:
            return maximum - 1
    return 0


def generate_valid_object(schema):
    obj = {}
    for k, v in schema["properties"].iteritems():
        obj[k] = generate_valid(v)
    return obj


def generate_invalid(schema):
    """
    Generate an invalid json dictionary based on a schema.
    Only one value is mis-generated for each dictionary created.
    """
    LOG.debug("generate_invalid: %s" % schema)
    schema_type = schema["type"]
#    if isinstance(schema_type, list):
#        return generate_invalid_value_from_list(schema, schema_type)
    return type_map_invalid[schema_type](schema)


def generate_invalid_string(schema):
    invalids = [("inv_str_number", 4), ("inv_str_none", None)]
    min_length = schema.get("minLength", 0)
    if min_length > 0:
        invalids.append(("inv_str_min_length", "x"
                         * (min_length - 1)))
    max_length = schema.get("maxLength", -1)
    if max_length > -1:
        invalids.append(("inv_str_max_length", "x"
                         * (max_length + 1)))
    # TODO(dkr mko): handle format and pattern
    return invalids


def generate_invalid_integer(schema):
    # TODO(dkr mko): handle multipleOf
    invalids = [("inv_int_str", "xx"), ("inv_int_none", None)]

    if "minimum" in schema:
        minimum = schema["minimum"]
        if "exclusiveMinimum" not in schema:
            minimum -= 1
        invalids.append(("inv_int_min", minimum))
    if "maximum" in schema:
        maximum = schema["maximum"]
        if "exclusiveMaximum" not in schema:
            maximum += 1
        invalids.append(("inv_int_max", maximum))
    return invalids


def generate_invalid_object(schema):
    LOG.debug("generate_invalid_object: %s" % schema)
    valid = generate_valid(schema)
    invalids = []
    properties = schema["properties"]
    required = schema.get("required", [])
    for r in required:
        new_valid = copy.deepcopy(valid)
        del new_valid[r]
        invalids.append(("inv_obj_del_attr", new_valid))

    if not schema.get("additionalProperties", True):
        new_valid = copy.deepcopy(valid)
        new_valid["$$$$$$$$$$"] = "xxx"
        invalids.append(("inv_obj_add_prop", new_valid))

    for k, v in properties.iteritems():
        for invalid in generate_invalid(v):
            new_valid = copy.deepcopy(valid)
            new_valid[k] = invalid[1]
            invalids.append(("prop_%s_%s" % (k, invalid[0]), new_valid))

    LOG.debug("generate_invalid_object return: %s" % invalids)
    return invalids


type_map_valid = {"string": generate_valid_string,
                  "integer": generate_valid_integer,
                  "object": generate_valid_object}


type_map_invalid = {"string": generate_invalid_string,
                    "integer": generate_invalid_integer,
                    "object": generate_invalid_object}


def get_draft4_jsonschema():
    fn = os.path.join(os.path.dirname(__file__), 'jsonschema-draft4.json')
    return json.load(open(fn))


schema = {"type": "object",
          "properties":
          {"name": {"type": "string"},
           "http-method": {"enum": ["GET", "PUT", "HEAD",
                                    "POST", "PATCH", "DELETE"]},
           "url": {"type": "string"},
           "json-schema": get_draft4_jsonschema(),
           "resources": {"type": "array", "items": {"type": "string"}}
           },
          "required": ["name", "http-method", "url"],
          "additionalProperties": False,
          }


def validate_negative_test_schema(nts):
    jsonschema.validate(nts, schema)