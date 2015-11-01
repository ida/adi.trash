Introduction
============

An addon for Plone, which changes the deletion-behaviour.

If a user deletes item(s), moves them to a trashcan-folder named 'trash',
living in the upper next available navigation-root-folder – which is usually
the site-root-folder – instead of really deleting them.

Items inside of 'trash'-folders, or trash-folder themselves, will still
be actually, really, deleted.

Missing trash-folders are created on the fly.

Immediately after installation you won't see any trash-folders,
go on, delete something, they'll appear.

Installation
============

Add 'adi.trash to the eggs-section of your buildout-config, run buildout, restart instance(s).

