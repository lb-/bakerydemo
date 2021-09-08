"""
* ALSO - this will likely only work in Wagtail 2.15!
* Pages that use the mixin should show an 'Archive' button
* If Archive is clicked, the user goes to an archive confirmation view
* If they Confirm, the archive is done, otherwise they go back to the previous page
* There should also be a way to view the archived pages
* Might be nice to not use modeladmin (just to see what it is like)
* ArchiveUtil class?
"""

from django.db import models


class ArchivablePageMixin(models.Model):

    archived_on = models.DateTimeField(blank=True, null=True)

    @property
    def can_archive(self):
        return True

    class Meta:
        abstract = True
