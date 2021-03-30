# First Computer Systems Architecture Course

The problem statement can be found [here](https://ocw.cs.pub.ro/courses/asc/teme/tema1).

## Table of Contents

- [First Computer Systems Architecture Course](#first-computer-systems-architecture-course)
  - [Table of Contents](#table-of-contents)
  - [Project structure](#project-structure)
  - [Implementation](#implementation)
    - [Base program logic](#base-program-logic)
    - [Thread-Safe operations](#thread-safe-operations)

## Project structure

The implementation can be found inside the `/tema` directory. (some file names can be in Romanian, as it was required by the checker)

``` bash
tema/
    |-- consumer.py
    |-- marketplace.py
    |-- producer.py
    |-- product.py (this file was not modified)
```

To run the checker, execute the `run_tests.sh` script. You can run a individual test by running the `test.py` script, using the `.in` input as argument.

## Implementation

### Base program logic

Most of the logic is implemented inside the marketplace: producer/cart identification, product management(producing, adding/removing from cart and the _"checkout"_).

The `producer` threads are daemons, allowing them to be closed by the calling thread, when it ends (for this specific case, they will keep running in a loop, until the consumer threads are joined and the main function reaches the end).

The `consumer` threads need to execute a finite number of instructions, so `join` can be called on them. Each consumer can add a product to the cart, remove a product and place it back on the "shelf" (back in the producer's queue). One important aspect is the fact that the consumer will not check if the producer's queue is full(this could lead to a deadlock).

Another possible solution for this problem (which doesn't work for the given tests) would have been: when a consumer adds a product to the cart, the item will not be removed from the queue of the producer that created it. The item will be removed only when it leaves the marketplace (the checkout). I used this variant originally, but it didn't pass the test (some other factors may have been involved).

### Thread-Safe operations

Each instruction run from a thread is protected with locks (if it wasn't thread safe before. For example, list `appends` or `removes`). This includes the terminal output (`print` function), which was made thread-safe by implementing a print function inside the marketplace:

```py
    
    def __init__(...):
        [...]
        
        self.print_lock = Lock()

    def print(self, value):
        with self.print_lock:
            print(value)
```

© 2021 Grama Nicolae, 332CA
