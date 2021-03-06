# Copyright (c) 2016 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.


import shade
from shade import exc
from shade.tests import base


class TestRangeSearch(base.TestCase):

    def setUp(self):
        super(TestRangeSearch, self).setUp()
        self.cloud = shade.openstack_cloud(cloud='devstack')

    def test_range_search_bad_range(self):
        flavors = self.cloud.list_flavors()
        self.assertRaises(exc.OpenStackCloudException,
                          self.cloud.range_search, flavors, {"ram": "<1a0"})

    def test_range_search_exact(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": "4096"})
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual("m1.medium", result[0]['name'])

    def test_range_search_min(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": "MIN"})
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual("m1.tiny", result[0]['name'])

    def test_range_search_max(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": "MAX"})
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual("m1.xlarge", result[0]['name'])

    def test_range_search_lt(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": "<4096"})
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        flavor_names = [r['name'] for r in result]
        self.assertIn("m1.tiny", flavor_names)
        self.assertIn("m1.small", flavor_names)

    def test_range_search_gt(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": ">4096"})
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        flavor_names = [r['name'] for r in result]
        self.assertIn("m1.large", flavor_names)
        self.assertIn("m1.xlarge", flavor_names)

    def test_range_search_le(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": "<=4096"})
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))
        flavor_names = [r['name'] for r in result]
        self.assertIn("m1.tiny", flavor_names)
        self.assertIn("m1.small", flavor_names)
        self.assertIn("m1.medium", flavor_names)

    def test_range_search_ge(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors, {"ram": ">=4096"})
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))
        flavor_names = [r['name'] for r in result]
        self.assertIn("m1.medium", flavor_names)
        self.assertIn("m1.large", flavor_names)
        self.assertIn("m1.xlarge", flavor_names)

    def test_range_search_multi_1(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors,
                                         {"ram": "MIN", "vcpus": "MIN"})
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual("m1.tiny", result[0]['name'])

    def test_range_search_multi_2(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors,
                                         {"ram": "<8192", "vcpus": "MIN"})
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        flavor_names = [r['name'] for r in result]
        # All of these should have 1 vcpu
        self.assertIn("m1.tiny", flavor_names)
        self.assertIn("m1.small", flavor_names)

    def test_range_search_multi_3(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors,
                                         {"ram": ">=4096", "vcpus": "<6"})
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))
        flavor_names = [r['name'] for r in result]
        self.assertIn("m1.medium", flavor_names)
        self.assertIn("m1.large", flavor_names)

    def test_range_search_multi_4(self):
        flavors = self.cloud.list_flavors()
        result = self.cloud.range_search(flavors,
                                         {"ram": ">=4096", "vcpus": "MAX"})
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        # This is the only result that should have max vcpu
        self.assertEqual("m1.xlarge", result[0]['name'])
