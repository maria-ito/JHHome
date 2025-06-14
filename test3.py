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

        book.add_order(Order({"type": "BUY", "price": 1300, "quantity": 3, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1200, "quantity": 4, "contract": "GCQ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1400, "quantity": 0, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 0, "contract": "GCZ4 Comdty"}))

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_add_order_match(self):
        '''
        Tests adding orders followed by matching.
        '''
        print('test_add_order_match')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 1300, "quantity": 3, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1200, "quantity": 4, "contract": "GCQ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1400, "quantity": 2, "contract": "GCZ4 Comdty"}))

        book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), True)

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_match_order(self):
        '''
        Tests matching orders with existing orders in the book.
        '''
        print('test_match_order')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 1300, "quantity": 3, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1200, "quantity": 4, "contract": "GCQ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1400, "quantity": 2, "contract": "GCZ4 Comdty"}))

        book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), True)

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def test_cancel_order(self):
        '''
        Tests cancel orders.
        '''
        print('test_cancel_order ')
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 1600, "quantity": 9, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "BUY", "price": 1300, "quantity": 3, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1200, "quantity": 4, "contract": "GCQ4 Comdty"}))
        book.add_order(Order({"type": "SELL", "price": 1400, "quantity": 0, "contract": "GCZ4 Comdty"}))
        book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 0, "contract": "GCZ4 Comdty"}))

        book.cancel_order(list(book.order_map.keys())[0])

        book.sell_list.sort()
        book.buy_list.sort()
        self._run_test_list(book)
        self._run_test_map(book)

    def _run_test_list(self, bookobj):
        '''
        Assertion tests for lists.
        '''
        self.assertEqual(bookobj.buy_list[0][0], 1300)
        self.assertEqual(bookobj.buy_list[0][2], 3)

        self.assertEqual(bookobj.sell_list[0][0], -1400)
        self.assertEqual(bookobj.sell_list[0][2], 0)

    def _run_test_map(self, bookobj):
        '''
        Assertion tests for dicts.
        '''
        self.assertEqual(len(bookobj.order_map), 4)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, bookobj.buy_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, bookobj.buy_list[0][2])

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, bookobj.sell_list[1][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, bookobj.sell_list[1][2])