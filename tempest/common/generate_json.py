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
import pprint
import traceback

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
    if isinstance(schema_type, list):
        if "integer" in schema_type:
            schema_type = "integer"
        else:
            raise Exception("non-integer list types not supported")
    if isinstance(type_map_invalid[schema_type], list):
        result = []
        for generator in type_map_invalid[schema_type]:
            ret = generator(schema)
            expected_value = None
            if "results" in schema:
                if ret[0] in schema["results"]:
                    expected_value = schema["results"][ret[0]]
            if ret is not None:
                result.append((ret[0], ret[1], expected_value))
        LOG.debug("result: %s" % traceback.format_stack())
        return result
    return type_map_invalid[schema_type](schema)


def generator(fn):
    def wrapped(*args):
        result = fn(*args)
        if result is not None:
            LOG.debug(result)
            return (fn.__name__, result)
        return
    return wrapped


@generator
def gen_int(_):
    return 4


@generator
def gen_string(_):
    return "XXXXXX"


def gen_none(_):
    # Note(mkoderer): it's not using the decorator otherwise it'd be filtered
    return ('gen_none', None)


@generator
def gen_str_min_length(schema):
    min_length = schema.get("minLength", 0)
    if min_length > 0:
        return  "x" * (min_length - 1)


@generator
def gen_str_max_length(schema):
    max_length = schema.get("maxLength", -1)
    if max_length > -1:
        return "x" * (max_length + 1)


@generator
def gen_int_min(schema):
    if "minimum" in schema:
        minimum = schema["minimum"]
        if "exclusiveMinimum" not in schema:
            minimum -= 1
        return minimum


@generator
def gen_int_max(schema):
    if "maximum" in schema:
        maximum = schema["maximum"]
        if "exclusiveMaximum" not in schema:
            maximum += 1
        return maximum


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
            LOG.debug(invalid)
            new_valid = copy.deepcopy(valid)
            new_valid[k] = invalid[1]
            invalids.append(("prop_%s_%s" % (k, invalid[0]), new_valid,
                                             invalid[2]))

    LOG.debug("generate_invalid_object return: %s" % invalids)
    return invalids


type_map_valid = {"string": generate_valid_string,
                  "integer": generate_valid_integer,
                  "object": generate_valid_object}


type_map_invalid = {"string": [gen_int,
                               gen_none,
                               gen_str_min_length,
                               gen_str_max_length],
                    "integer": [gen_string,
                                gen_none,
                                gen_int_min,
                                gen_int_max],
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
           "resources": {"type": "array", "items": {"type": "string"}},
           "results": {"type": "object",
                       "properties": {}}
           },
          "required": ["name", "http-method", "url"],
          "additionalProperties": False,
          }


def validate_negative_test_schema(nts):
    jsonschema.validate(nts, schema)
