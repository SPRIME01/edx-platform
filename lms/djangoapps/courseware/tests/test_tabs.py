from courseware.tests.modulestore_config import TEST_DATA_MIXED_MODULESTORE
from .helpers import LoginEnrollmentTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from mock import patch


@override_settings(MODULESTORE=TEST_DATA_MIXED_MODULESTORE)
class StaticTabDateTestCase(LoginEnrollmentTestCase, ModuleStoreTestCase):
    """Test cases for Static Tab Dates."""

    def setUp(self):
        self.course = CourseFactory.create()
        self.page = ItemFactory.create(
            category="static_tab", parent_location=self.course.location,
            data="OOGIE BLOOGIE", display_name="new_tab"
        )

    def test_logged_in(self):
        self.setup_user()
        url = reverse('static_tab', args=[self.course.id, 'new_tab'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("OOGIE BLOOGIE", resp.content)

    def test_anonymous_user(self):
        url = reverse('static_tab', args=[self.course.id, 'new_tab'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("OOGIE BLOOGIE", resp.content)


@override_settings(MODULESTORE=TEST_DATA_MIXED_MODULESTORE)
class StaticTabDateTestCaseXML(LoginEnrollmentTestCase, ModuleStoreTestCase):
    # The following XML test course (which lives at common/test/data/2014)
    # is closed; we're testing that tabs still appear when
    # the course is already closed
    xml_course_id = 'edX/detached_pages/2014'

    # this text appears in the test course's tab
    # common/test/data/2014/tabs/8e4cce2b4aaf4ba28b1220804619e41f.html
    xml_data = "static 463139"
    xml_url = "8e4cce2b4aaf4ba28b1220804619e41f"

    @patch.dict('django.conf.settings.FEATURES', {'DISABLE_START_DATES': False})
    def test_logged_in_xml(self):
        self.setup_user()
        url = reverse('static_tab', args=[self.xml_course_id, self.xml_url])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.xml_data, resp.content)

    @patch.dict('django.conf.settings.FEATURES', {'DISABLE_START_DATES': False})
    def test_anonymous_user_xml(self):
        url = reverse('static_tab', args=[self.xml_course_id, self.xml_url])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.xml_data, resp.content)


