"""Unit tests of the task sort form."""
from django import forms
from django.test import TestCase
from tasks.forms import TaskSortForm

class TaskSortFormTestCase(TestCase):
    """Unit tests of the task sort form."""

    def setUp(self):
        self.form_input = {
            'sort_by': 'deadline',
            'asc_or_desc': True,
            'filter_by': 'name',
            'filter_string': 'task'
        }

    def test_form_has_necessary_fields(self):
        form = TaskSortForm()
        self.assertIn('sort_by', form.fields)
        self.assertIn('asc_or_desc', form.fields)
        self.assertIn('filter_by', form.fields)
        self.assertIn('filter_string', form.fields)
        sort_field = form.fields['sort_by']
        asc_or_desc_field = form.fields['asc_or_desc']
        filter_by_field = form.fields['filter_by']
        self.assertTrue(isinstance(sort_field, forms.ChoiceField))
        self.assertTrue(isinstance(asc_or_desc_field, forms.BooleanField))
        self.assertTrue(isinstance(filter_by_field, forms.ChoiceField))

    def test_valid_user_form(self):
        form = TaskSortForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_sort_by_validation(self):
        self.form_input['sort_by'] = 'bad_sort'
        form = TaskSortForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_sort_by_cannot_be_empty(self):
        self.form_input = {
            'asc_or_desc': True,
            'filter_by': 'name',
            'filter_string': 'task'
        }
        form = TaskSortForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_filter_by_validation(self):
        self.form_input['filter_by'] = 'bad_filter'
        form = TaskSortForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_filter_by_cannot_be_empty(self):
        self.form_input = {
            'sort_by': 'deadline',
            'asc_or_desc': True,
            'filter_string': 'task'
        }
        form = TaskSortForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_ascending_sort(self):
        self.form_input['asc_or_desc'] = False
        form = TaskSortForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_filter_string_can_be_empty(self):
        self.form_input = {
            'sort_by': 'deadline',
            'asc_or_desc': True,
            'filter_by': 'name'
        }
        form = TaskSortForm(data=self.form_input)
        self.assertTrue(form.is_valid())
