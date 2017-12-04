# Suggestions for release notes

https://github.com/wagtail/wagtail/blob/master/docs/releases/2.0.rst

* Should clarify that ForeignKey fields will need to be renamed (with example)


# Questions

What if you have a Django app called 'core' or 'sites', will it break things?


# Unhelpful errors if ForeignKey is set to wagtailcore.Page

Impossible to know where the incorrect ForeignKey reference is with these errors.

```
Unhandled exception in thread started by <function check_errors.<locals>.wrapper at 0xb57d392c>
Traceback (most recent call last):
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/utils/autoreload.py", line 228, in wrapper
    fn(*args, **kwargs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/commands/runserver.py", line 125, in inner_run
    self.check(display_num_errors=True)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/base.py", line 359, in check
    include_deployment_checks=include_deployment_checks,
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/base.py", line 346, in _run_checks
    return checks.run_checks(**kwargs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/checks/registry.py", line 81, in run_checks
    new_errors = check(app_configs=app_configs)
  File "/vagrant/wagtail/wagtail/admin/checks.py", line 63, in get_form_class_check
    if not issubclass(edit_handler.get_form_class(cls), WagtailAdminPageForm):
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 314, in get_form_class
    widgets=cls.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 220, in widget_overrides
    widgets.update(handler_class.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 220, in widget_overrides
    widgets.update(handler_class.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 220, in widget_overrides
    widgets.update(handler_class.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 220, in widget_overrides
    widgets.update(handler_class.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 581, in widget_overrides
    can_choose_root=cls.can_choose_root)}
  File "/vagrant/wagtail/wagtail/admin/widgets.py", line 158, in __init__
    models = ', '.join([model._meta.verbose_name.title() for model in target_models if model is not Page])
  File "/vagrant/wagtail/wagtail/admin/widgets.py", line 158, in <listcomp>
    models = ', '.join([model._meta.verbose_name.title() for model in target_models if model is not Page])
AttributeError: 'str' object has no attribute '_meta'
```


# Unsure what is happening with ForeignKey to images



```
Unhandled exception in thread started by <function check_errors.<locals>.wrapper at 0xb5896e84>
Traceback (most recent call last):
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/utils/autoreload.py", line 228, in wrapper
    fn(*args, **kwargs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/commands/runserver.py", line 125, in inner_run
    self.check(display_num_errors=True)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/base.py", line 359, in check
    include_deployment_checks=include_deployment_checks,
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/management/base.py", line 346, in _run_checks
    return checks.run_checks(**kwargs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/core/checks/registry.py", line 81, in run_checks
    new_errors = check(app_configs=app_configs)
  File "/vagrant/wagtail/wagtail/admin/checks.py", line 63, in get_form_class_check
    if not issubclass(edit_handler.get_form_class(cls), WagtailAdminPageForm):
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 314, in get_form_class
    widgets=cls.widget_overrides())
  File "/vagrant/wagtail/wagtail/admin/edit_handlers.py", line 61, in get_form_for_model
    return metaclass(class_name, (form_class,), form_class_attrs)
  File "/vagrant/wagtail/wagtail/admin/forms.py", line 289, in __new__
    new_class = super(WagtailAdminModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/modelcluster/forms.py", line 192, in __new__
    new_class = super(ClusterFormMetaclass, cls).__new__(cls, name, bases, attrs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/forms/models.py", line 266, in __new__
    apply_limit_choices_to=False,
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/forms/models.py", line 186, in fields_for_model
    formfield = formfield_callback(f, **kwargs)
  File "/vagrant/wagtail/wagtail/admin/forms.py", line 270, in formfield_for_dbfield
    return db_field.formfield(**kwargs)
  File "/home/vagrant/.virtualenvs/bakerydemo/lib/python3.4/site-packages/django/db/models/fields/related.py", line 978, in formfield
    (self.name, self.remote_field.model))
ValueError: Cannot create form field for 'image' yet, because its related model 'images.Image' has not been loaded yet
```
