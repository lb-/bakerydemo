FieldSet -> https://developer.mozilla.org/en-US/docs/Web/HTML/Element/fieldset
A custom field type of 'section'
Ideally a custom InlinePanel that offers two options; field and section
When form is rendered, it will spit out the fields as is and also a fieldsets for use in the template

- Basic functionality working (it renders a fieldset)
- Next steps are to ensure that the sections do not show in exported data or data reports
- Then validate it works when section is put in random places, start/end/multiple in a row
- Maybe refactor to be `fieldset` instead of `section` and clean up the form utils
- ideally, when InlinePanel is shown, it renders TWO buttons one for field and one for section
