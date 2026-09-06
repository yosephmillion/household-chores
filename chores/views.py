from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Household


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

def home(request):
    household = Household.objects.filter(chores__isnull=False).first()

    if household is None:
        return redirect("/admin/")

    return redirect("dashboard", household_id=household.id)