def get_slow_primes(limit):
    result = []
    for x in range(2, limit):
        is_prime = True
        for y in range(2,x):
            if x % y == 0:
                is_prime = False
        if is_prime:
            result.append(x)
    return result



def get_fast_primes(limit):
    sieve = [False]*limit
    result = []
    for x in range(2, limit):
        if not sieve[x]:
            for y in range(x, limit, x):
		sieve[y] = True
	    result.append(x)
    return result
NUM = 1000000

import time

start_fast = time.time()
print len(get_fast_primes(NUM))
print 'FAST: %f' %(time.time() - start_fast)

start_slow = time.time()
print len(get_slow_primes(NUM))
print 'SLOW: %f' % (time.time() - start_slow)

