'''
Tests designed for task 3.
'''

import unittest

from task2 import *


class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        '''
        Tests adding orders.
        '''
        print('test_add_order')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}))
        book.add_order(Order({"type": "BUY", "price": 110, "quantity": 2}))
        book.add_order(Order({"type": "SELL", "price": 101, "quantity": 6}))

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_add_order_match_1(self):
        '''
        Tests adding orders with matching - version 1.
        '''
        print('test_add_order_match_1')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 7}))
        book.add_order(Order({"type": "BUY", "price": 110, "quantity": 2}))

        book.add_order(Order({"type": "BUY", "price": 111, "quantity": 2}), True)

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_add_order_match_2(self):
        '''
        Tests adding orders with matching - version 2.
        '''
        print('test_add_order_match_2')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}))
        book.add_order(Order({"type": "BUY", "price": 108, "quantity": 2}))

        book.add_order(Order({"type": "BUY", "price": 100, "quantity": 2}), True)

        book.sell_list.sort()
        book.buy_list.sort(reverse=True)
        self._run_test_list(book)
        self._run_test_map(book)

    def test_match_order_1(self):
        '''
        Tests matching orders with existing orders in the book - version 1.
        '''
        print('test_match_order_1')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}))
        book.add_order(Order({"type": "SELL", "price": 101, "quantity": 4}))
        book.match_order(Order({"type": "BUY", "price": 100, "quantity": 4}))

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_match_order_2(self):
        '''
        Tests matching orders with existing orders in the book - version 2.
        '''
        print('test_match_order_2')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}))
        book.add_order(Order({"type": "SELL", "price": 111, "quantity": 4}))
        book.match_order(Order({"type": "BUY", "price": 111, "quantity": 4}))

        book.sell_list.sort(reverse=True)
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_cancel_order(self):
        '''
        Tests cancel orders.
        '''
        print('test_cancel_order')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 106, "quantity": 3}))
        book.add_order(Order({"type": "BUY", "price": 109, "quantity": 1}))
        book.add_order(Order({"type": "SELL", "price": 102, "quantity": 5}))
        book.add_order(Order({"type": "BUY", "price": 110, "quantity": 3}))
        book.add_order(Order({"type": "SELL", "price": 101, "quantity": 9}))
        book.cancel_order(list(book.order_map.keys())[0])

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def _run_test_list(self, bookobj):
        '''
        Assertion tests for lists.
        '''
        self.assertEqual(bookobj.buy_list[0][0], 109)
        self.assertEqual(bookobj.buy_list[0][2], 1)

        self.assertEqual(bookobj.sell_list[0][0], -102)
        self.assertEqual(bookobj.sell_list[0][2], 5)

    def _run_test_map(self, bookobj):
        '''
        Assertion tests for dicts.
        '''
        self.assertEqual(len(bookobj.order_map), 4)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, 109)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, 1)

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, -102)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, 5)
