"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers_current_id = 0
        self.carts_current_id = 0
        self.products = []
        self.carts = []

        self.prod_id_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # Make the operation thread-safe
        with self.prod_id_lock:
            producer_id = self.producers_current_id
            self.producers_current_id += 1
            self.products.append([])

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: Int
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        with self.producer_list_lock:
            if self.products_per_producer[producer_id] < self.queue_size_per_producer:
                self.products.append((product, producer_id))
                self.products_per_producer[producer_id] += 1
                return True

            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.carts_id_lock:
            cart_id = self.carts_current_id
            self.carts_current_id += 1

            # Add a new cart(list) to the carts list
            self.carts.insert(cart_id, [])

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # Search for the product in the product-producer id pairs list.
        with self.products_lock:
            prod_pair = next(
                (prod_id_pair for prod_id_pair in self.products
                 if prod_id_pair[0].name == product.name), None)

            if prod_pair is not None:
                # Add the product from the cart and remove it from the store
                self.carts[cart_id].append(prod_pair)
                self.products.remove(prod_pair)
                return True

            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # Search for the product_pair in the cart.
        with self.products_lock:
            prod_pair = next(
                (prod_id_pair for prod_id_pair in reversed(self.carts[cart_id])
                 if prod_id_pair[0].name == product.name), None)

            if prod_pair is not None:
                # This should always be true (the product should be already in the cart)
                self.products.append(prod_pair)

                self.carts[cart_id].reverse()
                self.carts[cart_id].remove(prod_pair)
                self.carts[cart_id].reverse()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        prod_list = []

        for prod_pair in self.carts[cart_id]:
            with self.producer_list_lock:
                self.products_per_producer[prod_pair[1]] -= 1
            prod_list.append(prod_pair[0])

        self.carts[cart_id].clear()

        return prod_list
