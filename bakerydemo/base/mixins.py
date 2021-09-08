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

from wagtail.core.models import Page, PagePermissionTester, UserPagePermissionsProxy


class ArchivePagePermissionTester(PagePermissionTester):
    def can_unlock(self):
        print("can_unlock", self)
        return False


class ArchiveUserPagePermissionsProxy(UserPagePermissionsProxy):
    def for_page(self, page):
        print("ArchiveUserPagePermissionsProxy for page")
        """Return a PagePermissionTester object that can be used to query whether this user has
        permission to perform specific tasks on the given page"""
        return ArchivePagePermissionTester(self, page)


class ArchivablePageMixin(Page):

    archived_on = models.DateTimeField(blank=True, null=True)

    @property
    def can_archive(self):
        print("can_archive", self)
        print("archived_on", self.archived_on)
        if self.archived_on:
            return False
        return True

    def permissions_for_user(self, user):
        """
        Return a PagePermissionsTester object defining what actions the user can perform on this page
        """
        print("permissions_for_user")
        user_perms = ArchiveUserPagePermissionsProxy(user)
        return user_perms.for_page(self)

    class Meta:
        abstract = True
