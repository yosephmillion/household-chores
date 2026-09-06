from django.db import models


class Household(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseholdMember(models.Model):
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="members",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chore(models.Model):
    ONE_TIME = "one_time"
    RECURRING = "recurring"

    CHORE_TYPES = [
        (ONE_TIME, "One-time"),
        (RECURRING, "Recurring"),
    ]

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="chores",
    )
    title = models.CharField(max_length=200)
    chore_type = models.CharField(
        max_length=20,
        choices=CHORE_TYPES,
        default=ONE_TIME,
    )
    assigned_to = models.ForeignKey(
        HouseholdMember,
        on_delete=models.CASCADE,
        related_name="chores",
    )
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ChoreCompletion(models.Model):
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    member = models.ForeignKey(
        HouseholdMember,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chore.title} completed by {self.member.name}"