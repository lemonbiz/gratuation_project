from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import User
from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve
from django.test import TransactionTestCase


class LoginRequiredPasswordChangeTests(TransactionTestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TransactionTestCase):
    def setUp(self, data=None):
        # 因为函数参数的初始值只会在函数定义的时间里计算一次
        # 例如如果你第一次调用函数a(data=0): func 将data = 1，下次调用的时候
        # 将会无视data=0, 直接取用data=1, 还有我的输入法怎么是繁体的
        # 所以将default赋值可变（mutable）对象会导致超过预期的结果
        if data is None:
            data = {}
        self.user = User.objects.create_user(
            username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self, data=None):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        """
                refresh the user instance from database to get the new password
        hash updated by the change password view.
        """
        # 刷新下数据库确保有最新状态的数据
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """
                Create a new request to an arbitrary page.
        The resulting response should now have an `user` to i
        ts context, after a successful sign up.
        """
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        """
        An invalid form submission should return to the same
        page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        """
        refresh the user instance from the database to make
        sure we have the latest data.
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))