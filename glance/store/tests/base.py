# Copyright 2011 OpenStack Foundation
# Copyright 2014 Red Hat, Inc
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

import fixtures
from oslo.config import cfg
import testtools

import glance.store as store
from glance.store import location


class StoreBaseTest(testtools.TestCase):

    def setUp(self):
        super(StoreBaseTest, self).setUp()
        self.conf = cfg.ConfigOpts()
        self.conf(args=[])
        store.register_opts(self.conf)

        # Ensure stores + locations cleared
        location.SCHEME_TO_CLS_MAP = {}

        store.create_stores(self.conf)
        self.addCleanup(setattr, location, 'SCHEME_TO_CLS_MAP', dict())
        self.test_dir = self.useFixture(fixtures.TempDir()).path

    def config(self, **kw):
        """Override some configuration values.

        The keyword arguments are the names of configuration options to
        override and their values.

        If a group argument is supplied, the overrides are applied to
        the specified configuration option group.

        All overrides are automatically cleared at the end of the current
        test by the fixtures cleanup process.
        """
        group = kw.pop('group', None)
        for k, v in kw.iteritems():
            self.conf.set_override(k, v, group)