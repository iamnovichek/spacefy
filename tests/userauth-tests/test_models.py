from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.userauth.models import CustomUser, CustomUserManager, UserProfile
from apps.spacefy.models import Friend, Post, Photo, Descriprion, Story


class TestCustomManager(TestCase):
    def setUp(self):
        self.valid_email = "test@gmail.com"
        self.invalid_email = "invalidemail.com"
        self.password = "password123"
        self.manager = CustomUser.objects

    def test_create_user_valid_data(self) -> None:
        user = self.manager.create_user(
            email=self.valid_email,
            password=self.password
        )

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertTrue(CustomUser.objects.filter(id=user.id).exists())

        created_user = CustomUser.objects.get(id=user.id)
        self.assertEqual(created_user.email, self.valid_email)

    def test_create_user_no_email(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                email=None,
                password=self.password
            )

            self.assertEqual(e.message, "Email is required!")

    def test_create_user_invalid_email(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                email=self.invalid_email,
                password=self.password
            )

            self.assertEqual(e.message, "Invalid email format!")

    def test_create_user_no_password(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                email=self.valid_email,
                password=None
            )

            self.assertEqual(e.message, "Password is required!")

    def test_create_superuser_valid(self) -> None:
        user = self.manager.create_superuser(
            email=self.valid_email,
            password=self.password
        )

        self.assertTrue(user.is_active)
        self.assertTrue(user.is_admin)
        self.assertTrue(CustomUser.objects.filter(id=user.id).exists())

        created_superuser = CustomUser.objects.get(id=user.id)
        self.assertEqual(created_superuser.email, self.valid_email)

    def test_create_superuser_no_email(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                email=None,
                password=self.password
            )

            self.assertEqual(e.message, "Email is required!")

    def test_create_superuser_invalid_email(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                email=self.invalid_email,
                password=self.password
            )

            self.assertEqual(e.message, "Invalid email format!")

    def test_create_superuser_no_password(self) -> None:
        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                email=self.valid_email,
                password=None
            )

            self.assertEqual(e.message, "Password is required!")


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.superuser = CustomUser.objects.create_superuser(
            email="test@gmail.com",
            password="password123"
        )
        self.user = CustomUser.objects.create_user(
            email="user@gmail.com",
            password="password123"
        )

    def test_create_instance(self) -> None:
        self.assertEqual(self.user.email, "user@gmail.com")
        self.assertEqual(self.superuser.email, "test@gmail.com")
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_admin)
        self.assertFalse(self.user.is_admin)
        self.assertEqual(self.user.USERNAME_FIELD, "email")
        self.assertEqual(self.superuser.USERNAME_FIELD, "email")
        self.assertEqual(self.user.REQUIRED_FIELDS, [])
        self.assertEqual(self.superuser.REQUIRED_FIELDS, [])

    def test___str__(self) -> None:
        self.assertEqual(str(self.superuser), "test@gmail.com")
        self.assertEqual(str(self.user), "user@gmail.com")

    def test_has_perm(self) -> None:
        self.assertTrue(self.superuser.has_perm)
        self.assertTrue(self.user.has_perm)

    def test_has_module_perm(self) -> None:
        self.assertTrue(self.superuser.has_module_perms)
        self.assertTrue(self.user.has_module_perms)

    def test_is_staff(self) -> None:
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.user.is_staff)


class TestUserProfile(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="test@gmail.com",
            password="password123"
        )

        self.userprofile = UserProfile.objects.create(
            user=self.user,
            username="username",
            slug="username",
            first_name="John",
            last_name="Doe",
        )

    def test_create_instance(self) -> None:
        self.assertEqual(self.userprofile.user, self.user)
        self.assertEqual(self.userprofile.avatar, "default.png")
        self.assertEqual(self.userprofile.username, "username")
        self.assertEqual(self.userprofile.first_name, "John")
        self.assertEqual(self.userprofile.last_name, "Doe")
        self.assertEqual(self.userprofile.slug, "username")

    def test___str__(self) -> None:
        self.assertEqual(str(self.userprofile), "username")

    def test_save(self) -> None:
        self.assertTrue(UserProfile.objects.filter(username="username").exists())
        self.assertEqual(UserProfile.objects.get(username="username").slug, "username")
