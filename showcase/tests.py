from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, StudentOfTheDay

# Create your tests here.
class TestStudentCreatesProfile(TestCase):
    def test_successfully(self):
        user = User.objects.create_user("jimbob")

        self.client.force_login(user)

        self.client.post(
            reverse("showcase:create-profile"),
            {
                "headline": "I like code and such you know",
                "bio": "I'm from a small town and such, ya know",
                "codepen": "https://codepen.io/ilesh",
                "github_repository": "https://github.com/devinbooker616/benchmark-small-business",
            },
        )

        self.assertEqual(user.profile.headline, "I like code and such you know")
        self.assertEqual(user.profile.bio, "I'm from a small town and such, ya know")

    def test_form_is_rendered_on_create_profile_page(self):
        user = User.objects.create_user("jimbob")
        self.client.force_login(user)

        response = self.client.get(reverse("showcase:create-profile"))

        self.assertTemplateUsed(response, "create-profile.html")
        self.assertIn("form", response.context)

    def test_form_errors_are_rendered_on_invalid_post(self):
        user = User.objects.create_user("jimbob")
        self.client.force_login(user)

        response = self.client.post(reverse("showcase:create-profile"))

        self.assertTemplateUsed(response, "create-profile.html")
        self.assertTrue(response.context["form"].errors)


class TestUserSeesExistingProfiles(TestCase):
    def test_successfully(self):
        profiles = [
            Profile.objects.create(
                headline=f"Headline #{i}",
                bio=f"I'm from small town #{i}",
                user=User.objects.create_user(f"tob{i}as"),
                github_repository=f"https://github.com/devinbooker616/ascent #{i}",
                codepen=f"https://codepen.io/cobra_winfrey/pen/BayQeyr #{i}",
            )
            for i in range(3)
        ]

        response = self.client.get(reverse("showcase:profile-list"))

        for p in profiles:
            self.assertContains(response, p.headline)


class TestProfileStrShowsHeadline(SimpleTestCase):
    def test_example(self):
        profile = Profile(headline="totes my headline")

        self.assertEqual(str(profile), "totes my headline")


class TestUserSeesStudentProfile(TestCase):
    def test_successfully(self):
        user = User.objects.create_user("devin")
        profile = Profile.objects.create(
            user=user,
            headline="Totes the coolest",
            bio="you heard me",
            github_repository="https://github.com/devinbooker616/ascent",
            codepen="https://codepen.io/cobra_winfrey/pen/BayQeyr",
        )

        response = self.client.get(
            reverse("showcase:profile-page", kwargs={"id": profile.id})
        )

        self.assertContains(response, "devin")
        self.assertContains(response, "Totes the coolest")
        self.assertContains(response, "you heard me")
        self.assertContains(response, "https://github.com/devinbooker616/ascent")
        self.assertContains(response, "https://codepen.io/cobra_winfrey/pen/BayQeyr")


class TestUserSeesStudentOfTheDay(TestCase):
    def test_first_request_of_the_day(self):
        user = User.objects.create_user("devin")
        profile = Profile.objects.create(
            user=user,
            headline="Totes the coolest",
            bio="you heard me",
            github_repository="https://github.com/devinbooker616/ascent",
            codepen="https://codepen.io/cobra_winfrey/pen/BayQeyr",
        )
        self.assertEqual(StudentOfTheDay.objects.count(), 0)

        self.client.get(reverse("showcase:profile-list"))

        self.assertEqual(StudentOfTheDay.objects.count(), 1)

    def test_later_requests(self):
        for i in range(3):
            user = User.objects.create_user(f"devin{i}")
            profile = Profile.objects.create(
                user=user,
                headline="Totes the coolest",
                bio="you heard me",
                github_repository="https://github.com/devinbooker616/ascent",
                codepen="https://codepen.io/cobra_winfrey/pen/BayQeyr",
            )

        self.client.get(reverse("showcase:profile-list"))

        student = StudentOfTheDay.objects.first()

        self.client.get(reverse("showcase:profile-list"))
        self.assertEqual(StudentOfTheDay.objects.count(), 1)
        self.assertEqual(StudentOfTheDay.objects.first(), student)

        self.client.get(reverse("showcase:profile-list"))
        self.assertEqual(StudentOfTheDay.objects.count(), 1)
        self.assertEqual(StudentOfTheDay.objects.first(), student)

