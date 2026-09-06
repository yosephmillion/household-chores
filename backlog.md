# Household Chores Manager — Backlog

## Task 1 — Create the core data models

Create Django models for:

- Household
- HouseholdMember
- Chore
- ChoreCompletion

A Household can have multiple members.

A Chore belongs to a household and can be either one-time or recurring.

A Chore should store its assigned household member and due date.

ChoreCompletion should record when a member completes a chore.

Run migrations after creating the models.

## Task 2 — Create the chore list and dashboard

Create a basic dashboard that shows:

- The current household's chores
- The assigned member
- Due date
- Completion status
- Overdue status

Create Django views, URLs, and templates for the dashboard.

## Task 3 — Implement chore completion

Allow a household member to mark a chore as completed.

When a recurring chore is completed:

1. Create a completion record.
2. Move the chore to the next household member in the rotation.
3. Set its next due date.

## Task 4 — Implement automatic chore rotation

Implement rotation logic for recurring chores.

Members should receive recurring chores in a predictable order.

The rotation should continue through all household members.

## Task 5 — Add overdue notifications

Identify chores whose due date has passed without completion.

Display an overdue notification on the dashboard.

## Task 6 — Add calendar view

Create a calendar-style view showing chores based on their due dates.

Users should be able to see upcoming and overdue chores.

## Task 7 — Add tests

Create tests covering:

- Creating households and members
- Creating chores
- Completing chores
- Recurring chore rotation
- Overdue chores
- Dashboard behavior