from datetime import datetime, timedelta
from django.test import TestCase
from couchforms.signals import xform_archived, xform_unarchived

from corehq.form_processor.generic import GenericXFormInstance, GenericFormAttachment
from corehq.form_processor.interfaces.processor import FormProcessorInterface
from corehq.form_processor.interfaces.xform import XFormInterface


class TestFormArchiving(TestCase):

    def testArchive(self):
        xform = XFormInterface.create_from_generic(
            GenericXFormInstance(form={'foo': 'bar'}),
            GenericFormAttachment(name='form.xml', content='<data/>')
        )

        self.assertEqual("XFormInstance", xform.doc_type)
        self.assertEqual(0, len(xform.history))

        lower_bound = datetime.utcnow() - timedelta(seconds=1)
        XFormInterface.archive(xform, user='mr. librarian')
        upper_bound = datetime.utcnow() + timedelta(seconds=1)

        xform = XFormInterface.get_xform(xform.id)
        self.assertEqual('XFormArchived', xform.doc_type)

        [archival] = xform.history
        self.assertTrue(lower_bound <= archival.date <= upper_bound)
        self.assertEqual('archive', archival.operation)
        self.assertEqual('mr. librarian', archival.user)

        lower_bound = datetime.utcnow() - timedelta(seconds=1)
        XFormInterface.unarchive(xform, user='mr. researcher')
        upper_bound = datetime.utcnow() + timedelta(seconds=1)

        xform = XFormInterface.get_xform(xform.id)
        self.assertEqual('XFormInstance', xform.doc_type)

        [archival, restoration] = xform.history
        self.assertTrue(lower_bound <= restoration.date <= upper_bound)
        self.assertEqual('unarchive', restoration.operation)
        self.assertEqual('mr. researcher', restoration.user)

    def testSignal(self):
        global archive_counter, restore_counter
        archive_counter = 0
        restore_counter = 0

        def count_archive(**kwargs):
            global archive_counter
            archive_counter += 1

        def count_unarchive(**kwargs):
            global restore_counter
            restore_counter += 1

        xform_archived.connect(count_archive)
        xform_unarchived.connect(count_unarchive)

        xform = XFormInterface.create_from_generic(
            GenericXFormInstance(form={'foo': 'bar'}),
            GenericFormAttachment(name='form.xml', content='<data/>')
        )

        self.assertEqual(0, archive_counter)
        self.assertEqual(0, restore_counter)

        XFormInterface.archive(xform)
        self.assertEqual(1, archive_counter)
        self.assertEqual(0, restore_counter)

        XFormInterface.unarchive(xform)
        self.assertEqual(1, archive_counter)
        self.assertEqual(1, restore_counter)
