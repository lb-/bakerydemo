# Adding Tasks with a Checklist to Wagtail's Workflow System

**Goal:** Create a simple way for Wagtail's CMS admin users to manage custom Workflow Tasks with checklists.

**Why:** Wagtail's Workflow feature is incredibly powerful and can be leveraged to help guide our users through their Page publishing process easier.

## Journey

_Note: Feel free to skip if you just want to see the code._

One of my favourite books is [The Checklist Manifesto: How to Get Things Right](https://www.goodreads.com/book/show/7796228-the-checklist-manifesto) and another I am reading right now is [Everything in Its Place: The Power of Mise-En-Place to Organise Your Life, Work, and Mind](https://www.amazon.com/Everything-Its-Place-Mise-En-Place-Organize/dp/1635650119). The core message that is in common with these is the simple practice of writing a checklist or a plan before you start and where possible, manage those checklists for future work of the same kind.

Now, checklists can become a burden to those who are forced to mindlessly tick 700 boxes they never read for the thousandth time this week, so as in all things there is a balance.

However, I do honestly believe that simple checklists for recurring processes can help both new people to a process and those who are veterans, remember the critical aspects of what they do day to day.

One visceral memory I have of checklists is when my son, Leo, was born. My wife had to go into an emergency C-section and while I won't go into any more details, I do vividly remember up on the wall were two huge checklists (just like described in the Checklist Manifesto) with four or five key steps regarding the surgery process.

This memory is obviously key to me for more than just checklists, I got to see my amazing son for the first time. I often think back to that moment and wonder how many times a day, or that week those in the room would have done the same operation but how many lives a simple checklist on the wall would have saved.

It also puts into perspective the code I write and the processes we design for our team. Most likely what we do is not something that could risk the lives of others but nonetheless, we all have a part to play in helping our teams be excellent and remember the little but non-trivial things they do in their job.

So that leads us to Wagtail's Workflow system, which was introduced in [Wagtail 2.10](https://docs.wagtail.io/en/stable/releases/2.10.html#moderation-workflow). This system replaced the previous moderation workflow and was a sponsored feature (a special thanks to those who contribute to Open Source / Free Software) and may have flown under the radar for many of those who use Wagtail.

However, this Workflow feature has been built from the ground up to be very extensible and even borrows a lot of the approaches from Wagtail's core `Page` model itself where a mix of custom code and CMS Admin editing can be combined to make something incredibly flexible and powerful.

## What We Are Building

In this tutorial, you may have guessed, we will be putting together a way for Workflow Tasks to be created with a checklist and then that checklist is presented to those when they approve that specific step in the workflow.

This means that Wagtail Admin users could create a Workflow Checklist Task that is specifically for approval of types of pages or a generic one for all pages.

## Tutorial

### Step 0 - Getting Started

- It is assumed at this point you have Wagtail running locally and have a basic understanding of the [Workflow system from a user's perspective](https://docs.wagtail.io/en/stable/editor_manual/administrator_tasks/managing_workflows.html#managing-workflows).
- If not, it would be best to start with the [Wagtail Getting Started](https://docs.wagtail.io/en/stable/getting_started/index.html) guide.
- It is also assumed you have a basic understanding of Django's [Model](https://docs.djangoproject.com/en/3.2/topics/db/models/) and [Form](https://docs.djangoproject.com/en/3.2/topics/forms/) systems, although if not maybe this Tutorial will be a good way to get some deeper understanding.
- Versions:
  - Django 3.2
  - Wagtail 2.14

### Step 1 - Create the `ChecklistApprovalTask` Model

- Firstly, we need to think about what this `Task` model is and what we want to let the user fill out.
- The Wagtail `Workflow` area has a few key models, the main being a `Workflow` and a `Task`.
- When creating a `Task` in the Wagtail admin, the user is presented with what kind of `Task` to use (similar to when creating a new `Page`), this UI only shows if there are more than one kind of `Task` models available (Wagtail will search through your models and find all those that are subclasses of the core `Task` model).
- So, the `Task` model we are creating contains the fields that the user enters for multiple `Task`s of that 'kind', which are then mapped to one or more user created `Workflow`s.
- For our base `Task` model in that case, we do not actually need to define sets of checklists but rather a way for users to enter a set of checklist items and the simplest way to do this would be with a multi-line `TextField` where each line becomes a checklist item.
- Along with that, we will also add a field to determine whether this `Task` will require ALL checklist items to be ticked when submitting, this way the checklists can be a 'suggestion' or a 'requirement' on a per `Task` instance basis.
- It is important to remember that the `Task` instance can be changed at any time, so the checklist the user views today could be different tomorrow and as such we will keep this implementation simpler by not tracking that the checklist was submitted and which items were ticked but that could be implemented as an enhancement down the road.
- The following code is loosely based on the [Wagtail docs How to add new Task Types](https://docs.wagtail.io/en/stable/advanced_topics/custom_tasks.html) section, however, to save a bunch of reimplementation, instead of building all the user logic on our own we will just extend the existing (built-in) [`GroupApprovalTask`](https://github.com/wagtail/wagtail/blob/main/wagtail/core/models/__init__.py#L3425).
- The reason for extending `GroupApprovalTask` is that our `ChecklistApprovalTask` is very similar, we want to assign a user group that can approve/reject as a `Task` but we just want to allow the approve step to show extra content in the approval screen.
- Once you implement the code below you should be able to create a new Workflow and add one of the new `ChecklistApprovalTask` instances. For the rest of this tutorial it would be good to have one ready to go to test with as we build out the features.

#### Code `models.py`

- Create a new model `ChecklistApprovalTask` that extends `GroupApprovalTask`.
- This new model will contain two fields; `checklist` a `TextField` which will be used to generate the checklist items (per line), and a `is_checklist_required` `BooleanField` which will be ticked to force each checklist item to be ticked.
- Similar to `Page` `panels`, we can use the `admin_form_fields` class attribute to define a List of fields that will be shown when a user creates/edits this `Task`.
- The last part of our model is to leverage the `get_description` class method and the meta verbose names to provide a user-facing description & name of this `Task` type, plus we want to override the one that comes with the `GroupApprovalTask` class.
- Once you have built your model, run `django-admin makemigrations` and then `django-admin migrate` to apply your new model.

```python

from django.db import models

from wagtail.core.models import GroupApprovalTask


class ChecklistApprovalTask(GroupApprovalTask):
    """
    Custom task type where all the features of the GroupApprovalTask will exist but
    with the ability to define a custom checklist that may be required to be checked for
    Approval of this step. Checklist field will be a multi-line field, each line being
    one checklist item.
    """

    # Reminder: Already has 'groups' field as we are extending `GroupApprovalTask`

    checklist = models.TextField(
        "Checklist",
        help_text="Each line will become a checklist item shown on the Approve step.",
    )

    is_checklist_required = models.BooleanField(
        "Required",
        help_text="If required, all items in the checklist must be ticked to approve.",
        blank=True,
    )

    admin_form_fields = GroupApprovalTask.admin_form_fields + [
        "checklist",
        "is_checklist_required",
    ]

    @classmethod
    def get_description(cls):
        return (
            "Members of the chosen User Groups can approve this task with a checklist."
        )

    class Meta:
        verbose_name = "Checklist approval task"
        verbose_name_plural = "Checklist approval tasks"

```

![Step 1a - Create the Model](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hrki188v8nwm4fyk58ol.png)

![Step 1b - Task Model Editing](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b96xndiwoita8j3auh9m.png)

**Before you continue:** Check that when you create a new Task you can now see that there are two options available; 'Group approval task' and 'Checklist approval task'.

### Step 2 - Revise the Actions to Always Show the Form Modal

- The built-in `GroupApprovalTask`, when in a Workflow, will give the user two options; 'Approve and Publish' and 'Approve with Comment and Publish', the difference is that the one with the comment will open a form modal when clicked where the user can fill out a comment.
- What we want to do for our custom `Task` is to ensure that the approval step can **only** be completed with a form modal variant, and in this form we will show the checklist.
- Each `Task` has a method [`get_actions`](https://docs.wagtail.io/en/stable/advanced_topics/custom_tasks.html?highlight=get_actions#customising-behaviour) which will return a list of `(action_name, action_verbose_name, action_requires_additional_data_from_modal)` tuples.
- We will now revise this method to leverage the existing check if the user is in the right group but only return one option with the form modal being required, we will also ensure there is a reject action allowed.

#### Code `models.py`

- Within the `CrosscheckApprovalTask` built above, create a new method `get_actions`, this should copy the user check from [the GroupApprovalTask implementation](https://github.com/wagtail/wagtail/blob/main/wagtail/core/models/__init__.py#L3456) but only return two actions.

```python
class CrosscheckApprovalTask(GroupApprovalTask):
    # ... checklist etc, from above step

    def get_actions(self, page, user):
        """
        Customise the actions returned to have a reject and only one approve.
        The approve will have a third value as True which indicates a form is
        required.
        """

        if self.groups.filter(id__in=user.groups.all()).exists() or user.is_superuser:
            REJECT = ("reject", "Request changes", True)
            APPROVE = ("approve", "Approve", True)
            return [REJECT, APPROVE]

        return []

    # ... @classmethod etc
```

**Before you continue:** Check that when you put an existing Page into the workflow that contains this new task type, when approving the change it will show only one option 'Approve and Publish' and this should open a form modal. No need to approve just yet though.

![Step 2 - Basic actions form modal](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3902n6avyawhiwso3tim.png)

### Step 3 - Build a Basic Checklist Form

- We now need to create a custom form that leverages the existing form that `GroupApprovalTask` makes, this form needs to have a `MultipleChoiceField` where each of the `choices` is a line in our `Task` model's `checklist` field.
- We also want to make the form field dynamic based on the `Task` model's `is_checklist_required` saved value.
- To override the `Task` form we can add a [`get_form_for_action`](https://docs.wagtail.io/en/stable/advanced_topics/custom_tasks.html?highlight=get_actions#customising-behaviour) method and when the action is `'approve'` we can provide a custom Form.
- The things we need to answer is what form to extend (we want to ensure we get the comment field still), how do we ensure that the checklist values do not try to be 'saved' to the `TaskState` (the model that reflects each state for a `Task` as it is processed).
- If we take a look at the implementation of [`get_form_for_action` on the `GroupApprovalTask`](https://github.com/wagtail/wagtail/blob/main/wagtail/core/models/__init__.py#L3319) we can see that it returns a [`TaskStateCommentForm`](https://github.com/wagtail/wagtail/blob/main/wagtail/core/forms.py#L23) which extends a Django `Form` with one field, `comments`.

#### Code `models.py`

- To build a dynamic Class in Python, we can declare a new class in a function or we can also use the [`type`](https://docs.python.org/3/library/functions.html#type) built-in function, passing in three args. A name, base classes tuple and a dict where each key will be used to generate dynamic attributes (fields) and methods (e.g. the clean method).
- In this dynamic class we will extend whatever the super's `get_form_for_action` returns, this way we do not need to think about what this is in the code, but know that it is the `TaskStateCommentForm` above.
- We will also need to add a [`clean` method](https://docs.djangoproject.com/en/3.2/ref/forms/api/#django.forms.Form.clean) that will remove any checklist values that are submitted (as we do not want to save these).
- We will need to add a field, `checklist`, which we will pull out to a new class method `get_checklist_field` which can return a [`forms.MultipleChoiceField`](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#multiplechoicefield) that has dynamic values for `required` and the `choices` based on the `Task` instance. Note: The default widget used for this field is `SelectMultiple` which is a bit cluncky, but we will enhance that in the next step.
- We will also want to ensure that our `checklist` field shows before the `comment` field, for that we can dynamically add a [`field_order`](https://docs.djangoproject.com/en/3.2/ref/forms/api/#django.forms.Form.field_order) attribute.

```python
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

# ... other imports

class ChecklistApprovalTask(GroupApprovalTask):

    # ... checklist etc, from above step


    def get_checklist_field(self):
        """
        Prepare a form field that is a list of checklist boxes for each line in the
        checklist on this Task instance.
        """

        required = self.is_checklist_required

        field = dict(label=_("Checklist"), required=required)

        field["choices"] = [
            (index, label) for index, label in enumerate(self.checklist.splitlines())
        ]

        return forms.MultipleChoiceField(**field)

    def get_form_for_action(self, action):
        """
        If the action is 'approve', return a new class (using type) that has access
        to the checklist items as a field based on this Task's instance.
        """

        form_class = super().get_form_for_action(action)

        if action == "approve":

            def clean(form):
                """
                When this form's clean method is processed (on a POST), ensure we do not pass
                the 'checklist' data any further as no handling of this data is built.
                """
                cleaned_data = super(form_class, form).clean()
                if "checklist" in cleaned_data:
                    del cleaned_data["checklist"]
                return cleaned_data

            return type(
                str("ChecklistApprovalTaskForm"),
                (form_class,),
                dict(
                    checklist=self.get_checklist_field(),
                    clean=clean,
                    field_order=["checklist", "comment"],
                ),
            )

        return form_class

    # ... @classmethod etc

```

**Before you continue:** Check that when you click the Approve step on a Page with this Task, you now see a list of checklist items and it is required (or not, based on the data saved on the original Task type).

![Step 3 - Basic checklist form](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ubp07ihvacszr2w2pz9u.png)

### Step 4 - Enhance the Checklist Form

- Now, we will modify the [`help_text`](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#help-text), [`validators`](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#validators) and the [`widget`](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#widget) of our field generated in the method `get_checklist_field`.
- The goals here are to ensure that, when the checklist is required, we show and actually validate against all items being ticked.
- I find all of this pretty amazing, how powerful it is to build up blocks of built-in functions and logic into what we want without really writing much code ourselves, just calling the right methods/functions/classes.

#### Code `models.py`

- `help_text` needs to be a dynamic value based on the required value we set up in the previous step.
- If the checklist is required, we will leverage the built-in [`MinLengthValidator`](https://docs.djangoproject.com/en/3.2/ref/validators/#minlengthvalidator), while this is usually used to validate string length it can be used just the same for validating the length of the list of values provided to the field (in our case it will be a list of indices). We will also pass in a custom `message` kwarg to this validator so it makes sense to the user.
- For the `widget` we will use the built-in [`CheckboxSelectMultiple`](https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.CheckboxSelectMultiple), but note in the docs that even if we set `required` on the field the checkbox will not actually put required on the inputs HTML attributes so we need to pass in an extra `attrs` to the widget to handle this.
- Note: the only parts added below are the `min_length_validator`, `help_text`, `validators` and `widget` lines.

```python
from django import forms
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _, ngettext_lazy

# ... other imports

class ChecklistApprovalTask(GroupApprovalTask):

    # ... checklist etc, from above step

    def get_checklist_field(self):
        """
        Prepare a form field that is a list of checklist boxes for each line in the
        checklist on this Task instance.
        """

        required = self.is_checklist_required

        field = dict(label=_("Checklist"), required=required)

        field["choices"] = [
            (index, label) for index, label in enumerate(self.checklist.splitlines())
        ]

        min_length_validator = MinLengthValidator(
            len(field["choices"]),
            message=ngettext_lazy(
                "Only %(show_value)d item has been checked (all %(limit_value)d are required).",
                "Only %(show_value)d items have been checked (all %(limit_value)d are required).",
                "show_value",
            ),
        )

        field["help_text"] = (
            _("Please check all items.") if required else _("Please review all items.")
        )

        field["validators"] = [min_length_validator] if required else []

        field["widget"] = forms.CheckboxSelectMultiple(
            # required attr needed as not rendered by default (even if field required)
            # https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.CheckboxSelectMultiple
            attrs={"required": "required"} if required else {}
        )

        return forms.MultipleChoiceField(**field)

```

**Before you continue:** Check that the Approve modal form now contains actual checkboxes for each checklist item and that validation works as expected.

## Final Implementation

![Step 4 - Final form modal implementation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/04v9e6orsuzr9q4qxr8d.png)

- You should now have a fully functional new Task type where your CMS admin users can create for specific workflows that leverage existing user group approval logic along with custom checklists on a per Task instance.
- You can view the steps on the [tutorial/workflow-checklist](https://github.com/lb-/bakerydemo/commits/tutorial/workflow-checklist) branch or the [final code in the models.py file](https://github.com/lb-/bakerydemo/blob/tutorial/workflow-checklist/bakerydemo/base/models.py#L29-L150).
- I think it is really important to now require all the checklist items by default, but some will insist that this is required no doubt, but checklists work better as reminders and not rigid rules in this context.
- Please comment in response if you think something is missing here or have some other useful content relating to Wagtail Workflows that might be helpful.
- Thanks to my brother Sam for proofing and to [Danielle MacInnes](https://unsplash.com/photos/IuLgi9PWETU) for the cover photo.

## Future Improvements Ideas

- Adding a `description` field to the `Task` so that users can put content above the checklist that explains part of a process.
- Storing the checklist values (or maybe how many were checked), if that is useful for reporting, remember that the Page history will contain which users Approved the step and that may be enough as it is.
- Other Form content that applies to an Approval (or some other step like Rejection) and needs to be dynamic, maybe even requiring a comment when the workflow is Rejected.
- If you end up building one of these, even as a Github Gist, be sure to put a link to it in the comments.
