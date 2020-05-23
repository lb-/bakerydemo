Great question, I think this is probably an underlying issue with Wagtail's `ModelAdmin` and it might be good to raise an issue. There is a similar issue relating to 'collapsed state' [here](https://github.com/wagtail/wagtail/issues/3844).

## Option 1 - CSS Work around

A quick, css only, work around would be to 'move' the content to the top near the button. You may want to refine to work within different view port breakpoints, plus this would not be the most accessible solution, but it gets you there quickly.

You can add css to the `ModelAdmin` index listing via [`index_view_extra_css`](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/indexview.html#modeladmin-index-view-extra-css).

The example approach below makes the assumption that this is the desktop view, and users can 'hover' over the list filter which is moved to the header.


####**`wagtail_hooks.py`**
```python
class opportunitiesAdmin(ModelAdmin):
    model = opportunities
    #...
    index_view_extra_css = ('css/modeladmin-index.css',)
```

####**`static/css/modeladmin-index.css`**
```css
@media screen and (min-width: 50em) {
  .changelist-filter {
    position: fixed;
    top: 0;
    right: 15rem;
    z-index: 1;
    background: white;
    transform: translateY(-100vh);
  }

  .changelist-filter h2 {
    margin-top: 1rem;
    transform: translateY(100vh);
  }

  .changelist-filter:hover {
    transform: none;
  }

  .changelist-filter:hover h2 {
    margin-top: 0;
    transform: none;
  }
}
```

## Option 2 - Revise Template

You can go further, modifying the template used (either on a per model or for all index pages basis). See [`ModelAdmin` Overriding Templates](https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/primer.html#overriding-templates) docs.

For the underlying `index.html` template you can see the source of [`contrib/modeladmin/templates/modeladmin/index.html`](https://github.com/wagtail/wagtail/blob/master/wagtail/contrib/modeladmin/templates/modeladmin/index.html).

