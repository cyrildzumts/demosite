from django.test import TestCase
from catalog.models import Category, BaseProduct, Bag, Phone, Parfum, Shoe
from django.utils import timezone

# Create your tests here.


class CategoryParentTest(TestCase):
    fixtures = ['catalog']

    def setUp(self):
        self.shoes_cat = Category.objects.get(name="Chaussures")
        self.mode = Category.objects.get(name="Mode")
        # root cat
        self.phones_cat = Category.objects.get(name="Smartphone")
        # child cat
        self.smartphones = Category.objects.get(name="Smartphones")
        self.parfums = Category.objects.get(name="Parfumerie")
        self.edp = Category.objects.get(name="Eaux de Parfums")
        self.edt = Category.objects.get(name="Eaux de Toilettes")

    def test_root_cat(self):

        self.assertEqual(self.shoes_cat.root_cat(), self.mode)
        self.assertNotEqual(self.phones_cat.root_cat(), self.mode)

        self.assertNotEqual(self.edt.root_cat(), self.mode)
        self.assertNotEqual(self.edp.root_cat(), self.mode)

        self.assertEqual(self.edt.root_cat(), self.parfums)
        self.assertEqual(self.edp.root_cat(), self.parfums)

        self.assertNotEqual(self.edt.root_cat(), self.smartphones)
        self.assertNotEqual(self.edp.root_cat(), self.smartphones)
        self.assertNotEqual(self.phones_cat.root_cat(), self.smartphones)

    def test_is_root(self):

        self.assertFalse(self.shoes_cat.is_root())
        self.assertTrue(self.phones_cat.is_root())

        self.assertFalse(self.edt.is_root())
        self.assertFalse(self.edp.is_root())

        self.assertTrue(self.mode.is_root())
        self.assertTrue(self.parfums.is_root())

        self.assertFalse(self.smartphones.is_root())

    def test_is_parent(self):
        self.assertTrue(self.mode.is_parent())
        self.assertFalse(self.smartphones.is_parent())
        self.assertTrue(self.parfums.is_parent())
        self.assertTrue(self.shoes_cat.is_parent())
        self.assertFalse(self.edt.is_parent())
        self.assertFalse(self.edp.is_parent())
