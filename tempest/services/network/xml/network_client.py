# vim: tabstop=4 shiftwidth=4 softtabstop=4
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

from lxml import etree
import xml.etree.ElementTree as ET

from tempest.common.rest_client import RestClientXML
from tempest.services.compute.xml.common import Document
from tempest.services.compute.xml.common import Element
from tempest.services.compute.xml.common import xml_to_json


class NetworkClientXML(RestClientXML):

    def __init__(self, config, username, password, auth_url, tenant_name=None):
        super(NetworkClientXML, self).__init__(config, username, password,
                                               auth_url, tenant_name)
        self.service = self.config.network.catalog_type
        self.version = '2.0'
        self.uri_prefix = "v%s" % (self.version)

    def list_networks(self):
        uri = '%s/networks' % (self.uri_prefix)
        resp, body = self.get(uri, self.headers)
        networks = self._parse_array(etree.fromstring(body))
        networks = {"networks": networks}
        return resp, networks

    def create_network(self, name):
        uri = '%s/networks' % (self.uri_prefix)
        post_body = Element("network")
        p2 = Element("name", name)
        post_body.append(p2)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def create_bulk_network(self, count, names):
        uri = '%s/networks' % (self.uri_prefix)
        post_body = Element("networks")
        for i in range(count):
                p1 = Element("network")
                p2 = Element("name", names[i])
                p1.append(p2)
                post_body.append(p1)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        networks = self._parse_array(etree.fromstring(body))
        networks = {"networks": networks}
        return resp, networks

    def delete_network(self, uuid):
        uri = '%s/networks/%s' % (self.uri_prefix, str(uuid))
        return self.delete(uri, self.headers)

    def show_network(self, uuid):
        uri = '%s/networks/%s' % (self.uri_prefix, str(uuid))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def create_subnet(self, net_uuid, cidr):
        uri = '%s/subnets' % (self.uri_prefix)
        subnet = Element("subnet")
        p2 = Element("network_id", net_uuid)
        p3 = Element("cidr", cidr)
        p4 = Element("ip_version", 4)
        subnet.append(p2)
        subnet.append(p3)
        subnet.append(p4)
        resp, body = self.post(uri, str(Document(subnet)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def delete_subnet(self, subnet_id):
        uri = '%s/subnets/%s' % (self.uri_prefix, str(subnet_id))
        return self.delete(uri, self.headers)

    def list_subnets(self):
        uri = '%s/subnets' % (self.uri_prefix)
        resp, body = self.get(uri, self.headers)
        subnets = self._parse_array(etree.fromstring(body))
        subnets = {"subnets": subnets}
        return resp, subnets

    def show_subnet(self, uuid):
        uri = '%s/subnets/%s' % (self.uri_prefix, str(uuid))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def create_port(self, net_uuid, **kwargs):
        uri = '%s/ports' % (self.uri_prefix)
        port = Element("port")
        p1 = Element('network_id', net_uuid)
        port.append(p1)
        for key, val in kwargs.items():
            key = Element(key, val)
            port.append(key)
        resp, body = self.post(uri, str(Document(port)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def delete_port(self, port_id):
        uri = '%s/ports/%s' % (self.uri_prefix, str(port_id))
        return self.delete(uri, self.headers)

    def _parse_array(self, node):
        array = []
        for child in node.getchildren():
            array.append(xml_to_json(child))
        return array

    def list_ports(self):
        url = '%s/ports' % (self.uri_prefix)
        resp, body = self.get(url, self.headers)
        ports = self._parse_array(etree.fromstring(body))
        ports = {"ports": ports}
        return resp, ports

    def show_port(self, port_id):
        uri = '%s/ports/%s' % (self.uri_prefix, str(port_id))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def update_port(self, port_id, name):
        uri = '%s/ports/%s' % (self.uri_prefix, str(port_id))
        port = Element("port")
        p2 = Element("name", name)
        port.append(p2)
        resp, body = self.put(uri, str(Document(port)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def update_subnet(self, subnet_id, name):
        uri = '%s/subnets/%s' % (self.uri_prefix, str(subnet_id))
        subnet = Element("subnet")
        p2 = Element("name", name)
        subnet.append(p2)
        resp, body = self.put(uri, str(Document(subnet)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def update_network(self, net_id, name):
        uri = '%s/networks/%s' % (self.uri_prefix, str(net_id))
        network = Element("network")
        p2 = Element("name", name)
        network.append(p2)
        resp, body = self.put(uri, str(Document(network)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def create_security_group(self, name):
        uri = '%s/security-groups' % (self.uri_prefix)
        post_body = Element("security_group")
        p2 = Element("name", name)
        post_body.append(p2)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def list_security_groups(self):
        url = '%s/security-groups' % (self.uri_prefix)
        resp, body = self.get(url, self.headers)
        secgroups = self._parse_array(etree.fromstring(body))
        secgroups = {"security_groups": secgroups}
        return resp, secgroups

    def delete_security_group(self, secgroup_id):
        uri = '%s/security-groups/%s' % (self.uri_prefix, str(secgroup_id))
        return self.delete(uri, self.headers)

    def show_security_group(self, secgroup_id):
        uri = '%s/security-groups/%s' % (self.uri_prefix, str(secgroup_id))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def list_security_group_rules(self):
        url = '%s/security-group-rules' % (self.uri_prefix)
        resp, body = self.get(url, self.headers)
        rules = self._parse_array(etree.fromstring(body))
        rules = {"security_group_rules": rules}
        return resp, rules

    def create_security_group_rule(self, secgroup_id,
                                   direction='ingress', **kwargs):
        uri = '%s/security-group-rules' % (self.uri_prefix)
        rule = Element("security_group_rule")
        p1 = Element('security_group_id', secgroup_id)
        p2 = Element('direction', direction)
        rule.append(p1)
        rule.append(p2)
        for key, val in kwargs.items():
            key = Element(key, val)
            rule.append(key)
        resp, body = self.post(uri, str(Document(rule)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def delete_security_group_rule(self, rule_id):
        uri = '%s/security-group-rules/%s' % (self.uri_prefix, str(rule_id))
        return self.delete(uri, self.headers)

    def show_security_group_rule(self, rule_id):
        uri = '%s/security-group-rules/%s' % (self.uri_prefix, str(rule_id))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def create_bulk_subnet(self, subnet_list):
        uri = '%s/subnets' % (self.uri_prefix)
        post_body = Element("subnets")
        for i in range(len(subnet_list)):
            v = subnet_list[i]
            p1 = Element("subnet")
            for k, kv in v.iteritems():
                p2 = Element(k, kv)
                p1.append(p2)
            post_body.append(p1)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        subnets = self._parse_array(etree.fromstring(body))
        subnets = {"subnets": subnets}
        return resp, subnets

    def create_bulk_port(self, port_list):
        uri = '%s/ports' % (self.uri_prefix)
        post_body = Element("ports")
        for i in range(len(port_list)):
            v = port_list[i]
            p1 = Element("port")
            for k, kv in v.iteritems():
                p2 = Element(k, kv)
                p1.append(p2)
            post_body.append(p1)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        ports = self._parse_array(etree.fromstring(body))
        ports = {"ports": ports}
        return resp, ports

    def list_vips(self):
        url = '%s/lb/vips' % (self.uri_prefix)
        resp, body = self.get(url, self.headers)
        vips = self._parse_array(etree.fromstring(body))
        vips = {"vips": vips}
        return resp, vips

    def create_vip(self, name, protocol, protocol_port, subnet_id, pool_id):
        uri = '%s/lb/vips' % (self.uri_prefix)
        post_body = Element("vip")
        p1 = Element("name", name)
        p2 = Element("protocol", protocol)
        p3 = Element("protocol_port", protocol_port)
        p4 = Element("subnet_id", subnet_id)
        p5 = Element("pool_id", pool_id)
        post_body.append(p1)
        post_body.append(p2)
        post_body.append(p3)
        post_body.append(p4)
        post_body.append(p5)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def delete_vip(self, vip_id):
        uri = '%s/lb/vips/%s' % (self.uri_prefix, str(vip_id))
        return self.delete(uri, self.headers)

    def show_vip(self, vip_id):
        uri = '%s/lb/vips/%s' % (self.uri_prefix, str(vip_id))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def update_vip(self, vip_id, new_name):
        uri = '%s/lb/vips/%s' % (self.uri_prefix, str(vip_id))
        put_body = Element("vip")
        p2 = Element("name", new_name)
        put_body.append(p2)
        resp, body = self.put(uri, str(Document(put_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def list_pools(self):
        url = '%s/lb/pools' % (self.uri_prefix)
        resp, body = self.get(url, self.headers)
        pools = self._parse_array(etree.fromstring(body))
        pools = {"pools": pools}
        return resp, pools

    def create_pool(self, name, lb_method, protocol, subnet_id):
        uri = '%s/lb/pools' % (self.uri_prefix)
        post_body = Element("pool")
        p1 = Element("lb_method", lb_method)
        p2 = Element("protocol", protocol)
        p3 = Element("subnet_id", subnet_id)
        post_body.append(p1)
        post_body.append(p2)
        post_body.append(p3)
        resp, body = self.post(uri, str(Document(post_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def delete_pool(self, pool_id):
        uri = '%s/lb/pools/%s' % (self.uri_prefix, str(pool_id))
        return self.delete(uri, self.headers)

    def show_pool(self, pool_id):
        uri = '%s/lb/pools/%s' % (self.uri_prefix, str(pool_id))
        resp, body = self.get(uri, self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body

    def update_pool(self, pool_id, new_name):
        uri = '%s/lb/pools/%s' % (self.uri_prefix, str(pool_id))
        put_body = Element("pool")
        p2 = Element("name", new_name)
        put_body.append(p2)
        resp, body = self.put(uri, str(Document(put_body)), self.headers)
        body = _root_tag_fetcher_and_xml_to_json_parse(body)
        return resp, body


def _root_tag_fetcher_and_xml_to_json_parse(xml_returned_body):
    body = ET.fromstring(xml_returned_body)
    root_tag = body.tag
    if root_tag.startswith("{"):
        ns, root_tag = root_tag.split("}", 1)
    body = xml_to_json(etree.fromstring(xml_returned_body))
    body = {root_tag: body}
    return body
