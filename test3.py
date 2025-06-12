import unittest

from task3 import *

class TestOrderBook(unittest.TestCase):
    # def test_add_order(self):
    #     book = OrderBook()
    #
    #     book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 3, "contract": "GCZ4 Comdty"}), False)
    #     book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 4, "contract": "GCQ4 Comdty"}), False)
    #     self._run_test_list(book)
    #     self._run_test_map(book)
    #
    # def test_add_order_match(self):
    #     book = OrderBook()
    #
    #     book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 3, "contract": "GCZ4 Comdty"}), False)
    #     book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 4, "contract": "GCQ4 Comdty"}), False)
    #     book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), False)
    #
    #     book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), True)
    #
    #     self._run_test_list(book)
    #     self._run_test_map(book)

    def test_match_order(self):
        book = OrderBook()

        book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 3, "contract": "GCZ4 Comdty"}), False)
        book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 4, "contract": "GCQ4 Comdty"}), False)
        book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), False)

        book.match_order(Order({"type": "BUY", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), True)

        self._run_test_list(book)
        self._run_test_map(book)

    # def test_cancel_buy_order(self):
    #     book = OrderBook()
    #
    #     book.add_order(Order({"type": "BUY", "price": 1500, "quantity": 3, "contract": "GCZ4 Comdty"}), False)
    #     book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 4, "contract": "GCQ4 Comdty"}), False)
    #     book.add_order(Order({"type": "SELL", "price": 1500, "quantity": 2, "contract": "GCZ4 Comdty"}), False)
    #     book.cancel_order(list(book.order_map.keys())[-1])
    #     self._run_test_list(book)
    #     self._run_test_map(book)

    def _run_test_list(self, bookobj):
        self.assertEqual(bookobj.buy_list[0][0], 1500)
        self.assertEqual(bookobj.buy_list[0][2], 3)

        self.assertEqual(bookobj.sell_list[0][0], -1500)
        self.assertEqual(bookobj.sell_list[0][2], 4)

    def _run_test_map(self, bookobj):
        self.assertEqual(len(bookobj.order_map), 2)
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].price, bookobj.buy_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[0]].quantity, bookobj.buy_list[0][2])

        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].price, -bookobj.sell_list[0][0])
        self.assertEqual(bookobj.order_map[list(bookobj.order_map.keys())[1]].quantity, bookobj.sell_list[0][2])