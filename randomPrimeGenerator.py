#!/usr/bin/env python
"""
Generates large random primes from Random.org
"""
import requests
from random import randrange

class RandomPrimeGenerator():
	"""
	Generates Random Primes from numbers obtained from Random.org.
	"""
	def __init__(self):
		self.url = "https://www.random.org/"
		self.unchecked = []

		# List of first 10000 primes https://primes.utm.edu/lists/small/10000.txt
		with open("10000.txt") as f:
			primes_lst = f.readlines()
			primes_lst = [row.split() for row in primes_lst]
		self.small_primes = [int(prime) for row in primes_lst for prime in row]

	def get_random_prime(self):
		if not self.unchecked:
			self._get_more_random_numbers()

		guess = self.unchecked.pop()
		while not self.is_prime(guess):
			guess -= 1
			if guess.bit_length() < 1024:
				guess = self.unchecked.pop()
		return guess

	def is_prime(self, guess):
		"""Checks whether the guess is prime"""
		for small_prime in self.small_primes:
			if guess == small_prime:
				return True
			if guess % small_prime == 0:
				return False

		return self.miller_rabin_test(guess)

	# Modified from https://gist.github.com/bnlucas/5857478
	def miller_rabin_test(self, guess, no_of_checks=10):
		if guess == 2:
			return True
		if not guess & 1:
			return False

		def check(a, s, d, n):
			x = pow(a, d, n) # equivalent to a**d % n
			if x == 1:
				return True
			for _ in range(s - 1):
				if x == n - 1:
					return True
				x = pow(x, 2, n)
			return x == n - 1

		s = 0
		d = guess - 1

		while d % 2 == 0:
			d >>= 1
			s += 1

		for _ in range(no_of_checks):
			a = randrange(2, guess - 1)
			if not check(a, s, d, guess):
				return False
		return True

	def _get_more_random_numbers(self):
		"""Requests for random numbers to be checked for primality.

		We want to obtain 1024-bit numbers, which are formed by joining 64 random 16-bit numbers.
		"""
		if self.check_quota() < 0:
			raise ValueError("Insufficient quota. Try again later.")

		r = requests.get(self.url + "integers", params={"num": 960, "min": 0, "max": 2**16-1, "col": 1, "base": 2, "format": "plain", "rnd": "new"})

		if r.status_code != 200:
			raise ValueError("Unable to query API. HTTP Error Code: {}".format(r.status_code))

		random_numbers = r.text.split()
		curr_num = []
		while random_numbers:
			curr_num.append(random_numbers.pop())
			if len(curr_num) == 64:
				random_number = "".join(curr_num)
				if random_number[0] != "1":
					random_number = "1" + random_number[1:] # Ensure min size of number
					self.unchecked.append(int(random_number, 2))
				curr_num = []

	def check_quota(self):
		"""Checks for quota from Random.org"""
		r = requests.get(self.url + "quota", params={"format": "plain"})

		if r.status_code != 200:
			raise ValueError("Unable to obtain quota. HTTP Error Code: {}".format(r.status_code))
		
		return int(r.text.strip())



