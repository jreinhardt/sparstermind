#!/usr/bin/env python
#The MIT License (MIT)
#
#Copyright (c) 2013 <jreinhardt@ist-dein-freund.de>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE

import numpy as np
import cvxopt as cvx
from cvxopt.solvers import lp, options

options['LPX_K_MSGLEV'] = 0

def basis_pursuit(A,y):
	m,n = A.shape

	c = cvx.matrix([1. if i < m else 0. for i in range(m+n)])

	#assemble G block by block as a ndarray and convert then
	G = np.zeros((2*m,m+n))
	G[:m,:m] = - np.eye(m)
	G[m:2*m,:m] = - np.eye(m)
	G[:m,m:] = A
	G[m:2*m,m:] = -A
	G = cvx.matrix(G)

	h = cvx.matrix((+y).tolist()+(-y).tolist())

	sol = lp(c,G,h,solver='glpk')

	return np.array(sol['x'])[-n:]

n = 3
m = 100

k = 5*n*int(np.log(m))

#measurement vectors
measure = np.random.randint(0,2,size=(k,m)).astype('float')

#record measurements
y = np.zeros((k,)).astype('float')
res = None
print "Think of up to 3 numbers between 0 and 99, and assign them arbitrary scores"
for i in range(k):
		print "What is the total score of your numbers on this list:"
		print measure[i,:].nonzero()
		y[i] = float(raw_input('>'))
		if i > 3*n:
				res = basis_pursuit(measure[:i,:],y[:i])
				if len(res.nonzero()[0]) <= n:
						break

res = basis_pursuit(measure[:i,:],y[:i])
print i
print 'These are your numbers:', res.nonzero()[0]
print 'These are the scores:  ', res[res.nonzero()[0]].ravel()
