"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from os import terminal_size
from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.daemon = kwargs['daemon']
        self.products = products
        self.marketplace = marketplace
        self.wait_time = republish_wait_time
        self.kwargs = kwargs
        self.producer_id = marketplace.register_producer()

    def run(self):
        while True:
            for product_type_info in self.products:
                for _ in range(product_type_info[1]):
                    product = product_type_info[0]
                    delay = product_type_info[2]

                    try_inserting = True

                    # Try to add item
                    while try_inserting:
                        has_inserted = self.marketplace.publish(
                            self.producer_id, product)

                        if not has_inserted:
                            sleep(self.wait_time)
                        else:
                            try_inserting = False
                            sleep(delay)
