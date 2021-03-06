import time
from pageobjects.environments import Environments, Wizard
from pageobjects.networks import Networks, NeutronParameters
from pageobjects.nodes import Nodes
from pageobjects.settings import Settings
from pageobjects.tabs import Tabs
from settings import OPENSTACK_CENTOS, OPENSTACK_RELEASE_CENTOS
from tests.base import BaseTestCase
from pageobjects.base import PageObject


class TestEnvironment(BaseTestCase):

    def setUp(self):
        """Each test precondition

        Steps:
            1. Click on create environment
        """
        self.clear_nailgun_database()
        BaseTestCase.setUp(self)
        Environments().create_cluster_box.click()

    def test_default_settings(self):
        """Create default environment

        Scenario:
            1. Create environment with default values
            2. Click on created environment
            3. Verify that correct environment name is displayed
            4. Verify all information is displayed correctly
            5. Verify all info on Networks and Settings tab
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(6):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

        self.get_home()
        cb = Environments().create_cluster_boxes[0]
        self.assertIn(OPENSTACK_CENTOS, cb.text)
        cb.click()

        with Nodes() as n:
            time.sleep(1)
            self.assertIn(OPENSTACK_CENTOS, n.env_summary.text)
            self.assertIn('New', n.env_summary.text)
            self.assertIn('Multi-node', n.env_summary.text)
            self.assertIn('with HA', n.env_summary.text)
        Tabs().networks.click()
        with Networks() as n:
            self.assertTrue(n.flatdhcp_manager.
                            find_element_by_tag_name('input').is_selected())
        Tabs().settings.click()
        with Settings() as s:
            self.assertFalse(s.install_sahara.
                             find_element_by_tag_name('input').is_selected())
            self.assertFalse(s.install_murano.
                             find_element_by_tag_name('input').is_selected())
            self.assertFalse(s.install_ceilometer.
                             find_element_by_tag_name('input').is_selected())
            self.assertTrue(s.hypervisor_qemu.
                            find_element_by_tag_name('input').is_selected())
        pass

    def test_simple_mode(self):
        """Create environment with simple mode

        Scenario:
            1. Create environment with simple mode
            2. Click on created environment
            3. Verify that correct environment name is displayed
            4. Verify all information is displayed correctly
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            w.next.click()
            w.mode_multinode.click()
            for i in range(5):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

        self.get_home()
        cb = Environments().create_cluster_boxes[0]
        cb.click()

        with Nodes() as n:
            self.assertIn(OPENSTACK_CENTOS,
                          PageObject.get_text(n, 'env_summary'))
            self.assertIn('Multi-node', n.env_summary.text)

    def test_hypervisor_kvm(self):
        """Create environment with KVM hypervisor

        Scenario:
            1. Create environment with KVM hypervisor
            2. Click on created environment
            3. Open settings tab
            4. Verify KVM hypervisor is selected
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            w.next.click()
            w.next.click()
            w.hypervisor_kvm.click()
            for i in range(4):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

        Tabs().settings.click()

        with Settings() as s:
            self.assertTrue(s.hypervisor_kvm.
                            find_element_by_tag_name('input').is_selected())

    def test_neutron_gre(self):
        """Create environment with Neutron GRE network

        Scenario:
            1. Create environment with Neutron GRE network
            2. Click on created environment
            3. Open networks tab
            4. Verify Neutron parameters are displayed and
               Neutron with gre segmentation text is displayed
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(3):
                w.next.click()
            w.network_neutron_gre.click()
            for i in range(3):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

        Tabs().networks.click()

        with Networks() as n:
            self.assertEqual(n.segmentation_type.text,
                             'Neutron with GRE segmentation')
            self.assertTrue(NeutronParameters().parent.is_displayed())

    def test_neutron_vlan(self):
        """Create environment with Neutron VLAN network

        Scenario:
            1. Create environment with Neutron VLAN network
            2. Click on created environment
            3. Open networks tab
            4. Verify Neutron parameters are displayed and
               Neutron with vlan segmentation text is displayed
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(3):
                w.next.click()
            w.network_neutron_vlan.click()
            for i in range(3):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

        Tabs().networks.click()

        with Networks() as n:
            self.assertEqual(n.segmentation_type.text,
                             'Neutron with VLAN segmentation')
            self.assertTrue(NeutronParameters().parent.is_displayed())

    def test_storage_ceph(self):
        """Create environment with Ceph storage

        Scenario:
            1. Create environment with Ceph storage for Cinder and Glance
            2. Click on created environment
            3. Open settings tab
            4. Verify that Cinder for volumes, Ceph for volumes
               and images are selected, Ceph for rados isn't selected
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(4):
                w.next.click()
            w.storage_cinder_ceph.click()
            w.storage_glance_ceph.click()
            w.next.click()
            w.next.click()
            w.create.click()
            w.wait_until_exists()

        Tabs().settings.click()

        with Settings() as s:
            self.assertTrue(s.ceph_for_volumes.
                            find_element_by_tag_name('input').is_selected())
            self.assertTrue(s.ceph_for_images.
                            find_element_by_tag_name('input').is_selected())
            self.assertFalse(s.ceph_rados_gw.
                             find_element_by_tag_name('input').is_selected())

    def test_services(self):
        """Create environment with Sahara, Murano, Ceilometer selected

        Scenario:
            1. Create environment with Install Sahara,
               Murano, Ceilometer selected
            2. Click on created environment
            3. Open settings tab
            4. Verify that Install Sahara, Murano,
               Ceilometer checkboxes are selected
        """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(3):
                w.next.click()
            w.network_neutron_gre.click()
            w.next.click()
            w.next.click()
            w.install_sahara.click()
            w.install_murano.click()
            w.install_ceilometer.click()
            w.next.click()
            w.create.click()
            w.wait_until_exists()

        Tabs().settings.click()

        with Settings() as s:
            self.assertTrue(s.install_sahara.
                            find_element_by_tag_name('input').is_selected())
            self.assertTrue(s.install_murano.
                            find_element_by_tag_name('input').is_selected())
            self.assertTrue(s.install_ceilometer.
                            find_element_by_tag_name('input').is_selected())

    def simle_vcenter_env(self):
        """Create VCenter environment with simple
           mode and verify that element will be created
       author: Tatyana Dubyk /8th of August

       Test scenario:
       1.Create openstack env with vCenter hypervisor
       2.Select all settings by default, besides vCenter's settings
       3.Check that on page present new created env with required name
       """
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.next.click()
            w.mode_multinode.click()
            w.next.click()
            w.compute_vcenter.click()
            w.vcenter_ip_inputfield.send_keys('172.16.0.254')
            w.vcenter_username_inputfield.send_keys(
                'administrator@vsphere.local')
            w.vcenter_password_inputfield.send_keys('Qwer!1234')
            w.vcenter_cluster_inputfield.click()
            w.vcenter_cluster_inputfield.send_keys('Cluster1,Cluster2')
            w.next.click()
            w.next.click()
            w.next.click()
            w.next.click()
            w.create.click()
            w.wait_until_exists()
            w.find_required_env(self, OPENSTACK_CENTOS)
            self.assertEquals(self, OPENSTACK_CENTOS.lower().replace(" ", ""),
                              w.vcenter_cluster_created_name)
