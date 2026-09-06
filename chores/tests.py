from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Household, HouseholdMember, Chore, ChoreCompletion


class HouseholdChoresTests(TestCase):

    def setUp(self):
        self.household = Household.objects.create(
            name="Test Household"
        )

        self.yoseph = HouseholdMember.objects.create(
            household=self.household,
            name="Yoseph"
        )

        self.abel = HouseholdMember.objects.create(
            household=self.household,
            name="Abel"
        )

    def test_can_create_chore(self):
        chore = Chore.objects.create(
            household=self.household,
            title="Wash dishes",
            chore_type=Chore.RECURRING,
            assigned_to=self.yoseph,
            due_date=timezone.localdate() + timedelta(days=1),
        )

        self.assertEqual(chore.title, "Wash dishes")
        self.assertEqual(chore.assigned_to, self.yoseph)

    def test_one_time_chore_completion(self):
        chore = Chore.objects.create(
            household=self.household,
            title="Clean garage",
            chore_type=Chore.ONE_TIME,
            assigned_to=self.yoseph,
            due_date=timezone.localdate() + timedelta(days=1),
        )

        response = self.client.post(
            reverse("complete_chore", args=[chore.id])
        )

        chore.refresh_from_db()

        self.assertTrue(chore.completed)
        self.assertEqual(ChoreCompletion.objects.count(), 1)
        self.assertRedirects(
            response,
            reverse("dashboard", args=[self.household.id])
        )

    def test_recurring_chore_rotates_to_next_member(self):
        due_date = timezone.localdate() + timedelta(days=1)

        chore = Chore.objects.create(
            household=self.household,
            title="Wash dishes",
            chore_type=Chore.RECURRING,
            assigned_to=self.yoseph,
            due_date=due_date,
        )

        self.client.post(
            reverse("complete_chore", args=[chore.id])
        )

        chore.refresh_from_db()

        self.assertFalse(chore.completed)
        self.assertEqual(chore.assigned_to, self.abel)
        self.assertEqual(
            chore.due_date,
            due_date + timedelta(days=7)
        )
        self.assertEqual(ChoreCompletion.objects.count(), 1)

    def test_overdue_chore_is_shown(self):
        chore = Chore.objects.create(
            household=self.household,
            title="Take out trash",
            chore_type=Chore.ONE_TIME,
            assigned_to=self.yoseph,
            due_date=timezone.localdate() - timedelta(days=1),
        )

        response = self.client.get(
            reverse("dashboard", args=[self.household.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overdue")
        self.assertContains(response, chore.title)

    def test_calendar_page_loads(self):
        chore = Chore.objects.create(
            household=self.household,
            title="Wash dishes",
            chore_type=Chore.RECURRING,
            assigned_to=self.yoseph,
            due_date=timezone.localdate() + timedelta(days=1),
        )

        response = self.client.get(
            reverse("calendar", args=[self.household.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, chore.title)