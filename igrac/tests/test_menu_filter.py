import logging
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse_lazy as _
from geonode.base.populate_test_data import create_models

logger = logging.getLogger(__name__)


class BaseTest(TestCase):
    def setUp(self):
        self.url = _('home')
        self.object_ids = create_models()
        self.user, _ = get_user_model().objects.get_or_create(
            username='user', first_name='user'
        )
        self.user.set_password('user')
        self.user.save()

        group_1 = Group.objects.get_or_create(name='Group 1')
        group_2 = Group.objects.get_or_create(name='Group 2')
        self.user.groups.add(group_1)
        self.user.groups.add(group_2)
        logging.debug(" Test setUp. Creating User ")

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.user.username, password=self.user.password)


class TestAboutMenu(BaseTest):
    """
    Test About Menu visibility for unregistered user
    """
    def setUp(self):
        super(TestAboutMenu, self).setUp()

    def test_hidden_about_menu_for_unregistered_user(self):
        """
        About Menu should be hidden for unregistered user,
        so do its child elements
        """
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(response.content, 'aria-expanded="false">About<i class="fa fa-angle-down fa-lg">')
        self.assertNotIn(response.content, '<a href="/people">')
        self.assertNotIn(response.content, '<a href="/groups">')
        self.assertNotIn(response.content, '<a href="/categories">')

    def test_about_menu_child_elements_for_unregistered_user(self):
        """
        About Menu's child element's URLs should not be accessible to unregistered user.
        Unregistered user will be redirected to login page when they access the URLs
        """
        response = self.clien.get('/people', follow=True)
        self.assertRedirects(
            response, _('account_login') + '?next=/people',
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=False
        )

        response = self.clien.get('/groups', follow=True)
        self.assertRedirects(
            response, _('account_login') + '?next=/groups',
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=False
        )

        response = self.clien.get('/groups', follow=True)
        self.assertRedirects(
            response, _('account_login') + '?next=/groups/categories',
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=False
        )

    def test_shown_about_menu_for_registered_user(self):
        self.login()
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.content, 'aria-expanded="false">About<i class="fa fa-angle-down fa-lg">')
        self.assertIn(response.content, '<a href="/people">')
        self.assertIn(response.content, '<a href="/groups">')
        self.assertIn(response.content, '<a href="/categories">')

    def test_about_menu_child_elements_for_registered_user(self):
        """
        About Menu's child element's URLs should be accessible to registered user.
        """
        self.login()
        response = self.clien.get('/people')
        self.assertEqual(response.status_code, 200)

        response = self.clien.get('/groups')
        self.assertEqual(response.status_code, 200)

        response = self.clien.get('/groups/categories')
        self.assertEqual(response.status_code, 200)


class TestAddRemoteService(BaseTest):
    """
    Test About Menu visibility for unregistered user
    """

    def setUp(self):
        super(TestAddRemoteService, self).setUp()

    def test_hidden_add_remote_service_for_unregistered_user(self):
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(response.content, 'Add Remote Service'

    def test_add_remote_service_URL_for_unregistered_user(self):
        """
        Add Remote Service URLs should not be accessible to unregistered user.
        Unregistered user will be redirected to login page when they access the URLs
        """
        response = self.clien.get('/services/register/', follow=True)
        self.assertRedirects(
            response, _('account_login') + '?next=/services/register/',
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=False
        )

    def test_shown_add_remote_service_for_registered_user(self):
        self.login()
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(response.content, 'Add Remote Service')

    def test_add_remote_service_URL_for_registered_user(self):
        """
        Add Remote Service URLs should be accessible to registered user.
        """
        self.login()
        response = self.clien.get('/services/register/')
        self.asserEqual(response.status_code, 200)


class TestDefaultFilterByGroup(BaseTest):
    """
    Test default filter that is set after user login
    """
    def setUp(self):
        super(TestDefaultFilterByGroup, self).setUp()

    def test_filter_creation(self):
        self.login()
        self.client.get(self.url)
        session = self.client.session
        self.assertIn(
            session["filter_by_group"],
            "group__group_profile__slug__in=group-1"
        )
        self.assertIn(
            session["filter_by_group"],
            "group__group_profile__slug__in=group-2"
        )