'''
Tests designed for task 1.
'''

import unittest

from order_book import *


class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        '''
        Tests adding orders.
        '''
        print('test_add_order')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 102, "quantity": 7}))
        book.add_order(Order({"type": "SELL", "price": 109, "quantity": 6}))

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_type_error(self):
        '''
        Checks for type errors.
        '''
        print('test_type_error')
        book = OrderBook()

        with self.assertRaises(KeyError) as context:
            book.add_order(Order({"type": "BY", "price": 102, "quantity": 7}))
        self._test_variable_error(context, 'Type')

    def test_quantity_error(self):
        '''
        Checks for quantity errors.
        '''
        print('test_quantity_error')
        book = OrderBook()

        with self.assertRaises(ValueError) as context:
            book.add_order(Order({"type": "BUY", "price": 102, "quantity": -7}))
        self._test_variable_error(context, 'Quantity')

    def test_price_error(self):
        '''
        Checks for price errors.
        '''
        print('test_price_error')
        book = OrderBook()

        with self.assertRaises(ValueError) as context:
            book.add_order(Order({"type": "BUY", "price": -102, "quantity": 7}))
        self._test_variable_error(context, 'Price')

    def test_add_order_instrument(self):
        '''
        Tests adding orders with intruments.
        '''
        print('test_add_order_instrument')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 102, "quantity": 7, "instrument": 'EQ'}))
        book.add_order(Order({"type": "SELL", "price": 109, "quantity": 6, "instrument": 'FI'}))

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)
        self._run_test_instrument(book)

    def test_cancel_order(self):
        '''
        Tests cancel orders.
        '''
        print('test_cancel_order')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 104, "quantity": 5}))
        book.add_order(Order({"type": "BUY", "price": 102, "quantity": 7}))
        book.add_order(Order({"type": "SELL", "price": 109, "quantity": 6}))

        book.cancel_order(list(book.order_map.keys())[0])

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def _run_test_list(self, bookobj):
        '''
        Assertion tests for lists.
        '''

        self.assertEqual(bookobj.buy_list[0][0], 102)
        self.assertEqual(bookobj.buy_list[0][2], 7)

        self.assertEqual(bookobj.sell_list[0][0], -109)
        self.assertEqual(bookobj.sell_list[0][2], 6)

    def _run_test_map(self, bookobj):
        '''
        Assertion tests for dicts.
        '''
        self.assertEqual(len(bookobj.order_map), 2)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, bookobj.buy_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, bookobj.buy_list[0][2])

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, bookobj.sell_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, bookobj.sell_list[0][2])

    def _run_test_instrument(self, bookobj):
        '''
        Specific test for orders with instryments.
        '''
        self.assertEqual(bookobj.buy_list[0][5], 'EQ')
        self.assertEqual(bookobj.sell_list[0][5], 'FI')

    def _test_variable_error(self, context, variable_name):
        '''
        Assertion tests for exceptions.
        '''
        if variable_name == 'Type':
            self.assertEqual(str(context.exception), "'Order type not available.'")
        else:
            self.assertEqual(str(context.exception), f'{variable_name} must be positive.')

if __name__ == '__main__':
    unittest.main()
