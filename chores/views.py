from datetime import timedelta


from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import Household, Chore, ChoreCompletion


def home(request):
    household = Household.objects.filter(chores__isnull=False).first()

    if household is None:
        return redirect("/admin/")

    return redirect("dashboard", household_id=household.id)


def dashboard(request, household_id):
    household = get_object_or_404(Household, id=household_id)

    chores = household.chores.select_related("assigned_to").order_by("due_date")

    today = timezone.localdate()

    for chore in chores:
        chore.is_overdue = chore.due_date < today and not chore.completed

    return render(
        request,
        "chores/dashboard.html",
        {
            "household": household,
            "chores": chores,
        },
    )


def complete_chore(request, chore_id):
    chore = get_object_or_404(Chore, id=chore_id)

    if request.method == "POST" and not chore.completed:

        # Record the completion
        ChoreCompletion.objects.create(
            chore=chore,
            member=chore.assigned_to,
        )

        if chore.chore_type == Chore.RECURRING:
            # Get household members in a predictable order
            members = list(
                chore.household.members.order_by("id")
            )

            # Find the current member
            current_index = next(
                i for i, member in enumerate(members)
                if member.id == chore.assigned_to_id
            )

            # Move to the next member
            next_index = (current_index + 1) % len(members)
            chore.assigned_to = members[next_index]

            # Make it due 7 days later
            chore.due_date = chore.due_date + timedelta(days=7)

            # Recurring chores become pending again
            chore.completed = False

        else:
            # One-time chores stay completed
            chore.completed = True

        chore.save()

    return redirect("dashboard", household_id=chore.household.id)

def calendar(request, household_id):
    household = get_object_or_404(Household, id=household_id)

    chores = household.chores.select_related("assigned_to").order_by("due_date")

    return render(
        request,
        "chores/calendar.html",
        {
            "household": household,
            "chores": chores,
        },
    )