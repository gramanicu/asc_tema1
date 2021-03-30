"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.wait_time = retry_wait_time
        self.name = kwargs['name']

    def run(self):
        cart_id = self.marketplace.new_cart()
        for operations in self.carts:
            for operation in operations:
                if operation['type'] == 'add':
                    # Try adding the product to the cart
                    count = operation['quantity']
                    product = operation['product']

                    for _ in range(count):
                        try_adding = True

                        while try_adding:
                            has_added = self.marketplace.add_to_cart(
                                cart_id, product)

                            if not has_added:
                                sleep(self.wait_time)
                            else:
                                try_adding = False
                elif operation['type'] == 'remove':
                    # Remove product from cart
                    count = operation['quantity']
                    product = operation['product']
                    for _ in range(count):
                        self.marketplace.remove_from_cart(
                            cart_id, product)

            bought_products = self.marketplace.place_order(cart_id)

            # Print all bought products
            for prod in bought_products:
                self.marketplace.print(f'{self.name} bought {prod}')
