from plone import api
from urlparse import urlparse
from zope.i18nmessageid import MessageFactory

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

_ = MessageFactory('plone')


class Trash(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.paths = None
        self.navroot = api.portal.get_navigation_root(context)

        if 'paths' in self.request.form:
            self.paths = self.request.form['paths']

    def __call__(self):
        trash_id = 'trash'
        self.addTrash(trash_id)
        landing_url = self.request.get_header('referer')
        status = IStatusMessage(self.request)

        # We're coming from a folder_contents' delete-button:
        if urlparse(landing_url).path.endswith('/folder_contents'):

            if self.paths:

                for path in self.paths:

                    obj = api.content.get(path)

                    if self.isTrash(obj, trash_id):
                        api.content.delete(obj=obj) # check_linkintegrity=True)
                    else:
                        api.content.move(obj, self.navroot.trash)

                status.add(_(u'Item(s) deleted.'), type=u'info')

            else:
                status.add(_(u'Please select one or more items to delete.'),
                           type=u'info')

        # We're coming from an item's delete-button:
        else:
            if self.isTrash(self.context, trash_id):
                api.content.delete(obj=self.context) # check_linkintegrity=True)
            else:
                self.doAsTmpUserWithRole(
                    'Contributor',
                    api.content.move,
                    source=self.context,
                    target=self.navroot.trash,
                )
            status.add(_(u'Item(s) deleted.'), type=u'info')

            # We want to land on old parent:
            landing_url = '/'.join(self.context.absolute_url().split('/')[:-1])

        return self.request.response.redirect(landing_url)

    def addTrash(self, trash_id):
        """
        Create '[NAVROOT_PATH]/[TRASH_ID]', if not existing.
        """
        # Do we have a trashcan?
        if trash_id not in self.navroot.objectIds():
            # No, create it:
            self.doAsTmpUserWithRole(
                'Contributor',
                api.content.create,
                container=self.navroot,
                type='Folder',
                id=trash_id,
            )
            # Set trash-title:
            self.navroot.trash.setTitle('Trash')
            # Update title in navroot_catalog:
            self.navroot.trash.reindexObject()

    def doAsTmpUserWithRole(self, role, function, *args, **kwargs):
        """Create a temporary user with role and execute function.
        Credits: Copied from add-on 'Products.EasyNewsletter'."""
        sm = getSecurityManager()
        portal = api.portal.get()
        try:
            try:
                tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], '')

                tmp_user = tmp_user.__of__(portal.acl_users)
                newSecurityManager(None, tmp_user)

                return function(*args, **kwargs)

        except:
            raise
        finally:
            setSecurityManager(sm)


    def isTrash(self, obj, trash_id):
        """
        Check, whether an item lives inside of a trashcan,
        or is the trashcan itself. Returns True, if one of
        both is true.
        """
        TRASH = False
        navroot_url = self.navroot.absolute_url()
        item_url = self.context.absolute_url()
        item_rel_url = item_url[len(navroot_url)+1:]
        if item_rel_url == trash_id\
        or item_rel_url.startswith(trash_id + '/')\
        or obj.id == trash_id:
            TRASH = True
        return TRASH

