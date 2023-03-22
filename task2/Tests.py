from Cafe import Cafe
from Beverage import Beverage
from Customer import Customer
from Review import Review
import unittest

class TestCafe(unittest.TestCase):
    
    def setUp(self):
        self.cafe = Cafe('Test Cafe', '123 Main St')
        self.beverage = Beverage('Coffee', 'A hot beverage made from brewed coffee beans', 2.99)
        self.review = Review('Test User', 4.0, 'Great coffee!', '2042-11-06')

    def test_get_location_from_address(self):
        self.assertEqual(Cafe('CafeName', 'Didlaukio g. 51').get_location_from_address(), (54.7320874, 25.26302265347409))
        self.assertEqual(Cafe('CafeName', '86 Claylands Road').get_location_from_address(), (51.48256685, -0.11694134211189416))
        self.assertEqual(Cafe('CafeName', '11 Maldon Road').get_location_from_address(), (42.99882247977637, -81.29705629904535))

    def test_add_menu_item(self):
        self.cafe.add_menu_item(self.beverage)
        self.assertIn(self.beverage, self.cafe.menu)

    def test_remove_menu_item(self):
        self.cafe.add_menu_item(self.beverage)
        self.cafe.remove_menu_item(self.beverage)
        self.assertNotIn(self.beverage, self.cafe.menu)

    def test_place_order_insufficient_balance(self):
        customer = Customer('CustomerX', 10.0)
        customer.total = 12.00
        self.assertRaises(AssertionError, lambda: self.cafe.place_order(customer, customer.total, customer.balance))

    def test_calculate_average_rating(self):
        self.cafe.reviews = [Review('User1', 4, 'Great coffee', '2002-10-13'), Review('User2', 1, 'Terrible service', '2002-10-05')]
        self.assertEqual(self.cafe.calculate_average_rating(), 2.5)

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.beverage1 = Beverage('Coffee', {'mock': 'recipe'}, 2.50)
        self.beverage2 = Beverage('Tea', {'mock': 'recipe'}, 2.00)
        self.cafe1 = Cafe('Coffee House', '123 Main St')
        self.cafe2 = Cafe('Tea House', '456 Oak St')
        self.customer = Customer('Alice', 10.00)

    def test_add_order_item(self):
        self.cafe1.add_menu_item(self.beverage1)
        self.customer.add_order_item(self.cafe1, self.beverage1)
        self.assertIn(self.beverage1, self.customer.order)
        self.assertEqual(self.customer.total, 2.50)

    def test_remove_order_item(self):
        self.cafe1.add_menu_item(self.beverage1)
        self.customer.add_order_item(self.cafe1, self.beverage1)
        self.customer.remove_order_item(self.beverage1)
        self.assertNotIn(self.beverage1, self.customer.order)
        self.assertEqual(self.customer.total, 0)

    def test_place_order(self):
        self.cafe2.add_menu_item(self.beverage2)
        self.customer.add_order_item(self.cafe2, self.beverage2)
        self.customer.place_order(self.cafe2)
        self.assertEqual(self.customer.balance, 8.00)




if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestCustomer))
    suite.addTests(loader.loadTestsFromTestCase(TestCafe))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)