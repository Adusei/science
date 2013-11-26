#!/usr/bin/env python
import math as m
from random import choice

def mse(y,h):
    return(np.mean(np.square(y-h)))

# Consider a case where target function is  sin( pi x ) 
def target_fn(x):
	x = float(x)
	y = m.sin(x)
	return y

def model_1 (ex_1,ex_2):
	# minimize mean squared error.
	# a(x) + b
	y_1 = target_fn(ex_1)
	y_2 = target_fn(ex_2)

	print 'y_1:' + str(y_1)
	print 'y_2:' + str(y_2)
	return y_1, y_2

	#return a, b

def model_2 (x):
	# b = x
	# return b

def generate_distribution(range_len):
# the input distribution is uniform on [ -1, 1 ]
	nmbs =list(range(1,range_len))
	distr_x = []
	distr_y = []

	for nm in nmbs:
		distr_x.append(float(nm / float(range_len)))
		distr_x.append(float(-(nm / float(range_len))))

	return distr_x

def generate_sample():
	distr_x = generate_distribution(100)
	#for x_instance in distr_x:
		#y_instance = target_fn(x_instance)
		#distr_y.append(y_instance)
	
	sample_1 = choice(distr_x)
	sample_2 = choice(distr_x)

	#print sample_1
	return sample_1,sample_2

	#print str(distr_y)


if __name__ == '__main__':
  #x_range = generate_distribution(100)
  foo,bar = generate_sample()
  e,r = model_1(foo,bar)
  print foo
  print bar
  print e 
  print r
  #print x_range


# training set has two examples and the learning
# algorithm tries to minize the mean squared error.

# Assume that we have two learning models
# consisting of all hypothesis in the form of:

# h(x) = ax + b

# h(x) = b