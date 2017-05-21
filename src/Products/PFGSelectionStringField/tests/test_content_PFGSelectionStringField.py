import mock
import unittest


class TestPFGSelectionStringField(unittest.TestCase):

    def createPFGSelectionStringField(self):
        from Products.PFGSelectionStringField.content.field import PFGSelectionStringField
        return PFGSelectionStringField('field')

    def test_instance(self):
        field = self.createPFGSelectionStringField()
        from Products.PFGSelectionStringField.content.field import PFGSelectionStringField
        self.assertTrue(isinstance(field, PFGSelectionStringField))
        from Products.PloneFormGen.content.fields import FGSelectionField
        self.assertTrue(issubclass(PFGSelectionStringField, FGSelectionField))

    def test_portal_type(self):
        item = self.createPFGSelectionStringField()
        self.assertEqual(item.portal_type, 'PFGSelectionStringField')

    def test_interface(self):
        from Products.PFGSelectionStringField.interfaces import IPFGSelectionStringField
        field = self.createPFGSelectionStringField()
        self.assertTrue(IPFGSelectionStringField.providedBy(field))

    def test_schema_fields(self):
        item = self.createPFGSelectionStringField()
        names = [
            'id',
            'title',
            'description',
            'required',
            'hidden',
            'placeholder',
            'fgDefault',
            'fgVocabulary',
            'fgFormat',
            'subject',
            'relatedItems',
            'location',
            'language',
            'effectiveDate',
            'expirationDate',
            'creation_date',
            'modification_date',
            'creators',
            'contributors',
            'rights',
            'allowDiscussion',
            'excludeFromNav']
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names)

    def test_fgField(self):
        item = self.createPFGSelectionStringField()
        from Products.PFGSelectionStringField.content.field import StringVocabularyField
        field = item.fgField
        self.assertTrue(isinstance(field, StringVocabularyField))
        self.assertEqual(field.getName(), 'fg_selection_field')
        self.assertFalse(field.searchable)
        self.assertFalse(field.required)
        from Products.PFGSelectionStringField.content.field import SelectionStringWidget
        self.assertTrue(isinstance(field.widget, SelectionStringWidget))
        self.assertEqual(field.vocabulary, '_get_selection_vocab')
        self.assertTrue(field.enforceVocabulary)
        from Products.CMFCore.permissions import View
        self.assertEqual(field.write_permission, View)

    @mock.patch('Products.PFGSelectionStringField.content.field.getToolByName')
    def test_htmlValue(self, getToolByName):
        item = self.createPFGSelectionStringField()
        request = mock.Mock()
        getToolByName().getSiteEncoding.return_value = 'utf-8'
        request.form = {}
        item.fgField = mock.Mock()
        item.fgField.Vocabulary.return_value = [('aaa', ('aaa', None))]
        item.fgFormat = 'radio'
        self.assertEqual(item.htmlValue(request), '')
        item.fgFormat = 'flex'
        self.assertEqual(item.htmlValue(request), '')
        item.fgField.Vocabulary.return_value = [
            ('aaa', ('aaa', None)),
            ('bbb', ('bbb', None)),
            ('ccc', ('ccc', None)),
            ('ddd', ('ddd', None)),
            ('eee', ('eee', None))]
        self.assertEqual(item.htmlValue(request), '')
        request.form = {'field': 'aaa'}
        item.fgField.Vocabulary.return_value = [('aaa', ('aaa', None))]
        item.fgFormat = 'radio'
        self.assertEqual(item.htmlValue(request), 'aaa')
        item.fgFormat = 'flex'
        self.assertEqual(item.htmlValue(request), 'aaa')
        item.fgField.Vocabulary.return_value = [
            ('aaa', ('aaa', None)),
            ('bbb', ('bbb', None)),
            ('ccc', ('ccc', None)),
            ('ddd', ('ddd', None)),
            ('eee', ('eee', None))]
        self.assertEqual(item.htmlValue(request), 'aaa')
        item.fgFormat = 'select'
        request.form = {'field': 'bbb'}
        self.assertEqual(item.htmlValue(request), 'bbb')
        item.fgField.Vocabulary.return_value = [
            ('aaa', ('aaa', None)),
            ('bbb', ('bbb', 'Desc of BBB')),
            ('ccc', ('ccc', None)),
            ('ddd', ('ddd', None)),
            ('eee', ('eee', None))]
        self.assertEqual(item.htmlValue(request), 'bbb')
        request.form = {'field': 'bbb', 'field_SELECT': 'SELECTION OF BBB', 'field_bbb': 'RADIO OF BBB'}
        self.assertEqual(item.htmlValue(request), 'bbb<br />SELECTION OF BBB')
        item.fgFormat = 'flex'
        self.assertEqual(item.htmlValue(request), 'bbb<br />SELECTION OF BBB')
        item.fgFormat = 'radio'
        self.assertEqual(item.htmlValue(request), 'bbb<br />RADIO OF BBB')
