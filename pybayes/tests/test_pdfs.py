# Copyright (c) 2010 Matej Laitl <matej@laitl.cz>
# Distributed under the terms of the GNU General Public License v2 or any
# later version of the license, at your option.

"""Tests for pdfs"""

import unittest as ut

import numpy as np

import pybayes as pb


class TestPdf(ut.TestCase):
    """Test abstract class Pdf"""

    def setUp(self):
        self.pdf = pb.Pdf()

    def test_init(self):
        self.assertEqual(type(self.pdf), pb.Pdf)

    def test_abstract_methods(self):
        return  # TODO: this test fails due to bug in cython [1]
                # [1] http://trac.cython.org/cython_trac/ticket/583
        self.assertRaises(NotImplementedError, self.pdf.shape)
        self.assertRaises(NotImplementedError, self.pdf.mean)
        self.assertRaises(NotImplementedError, self.pdf.variance)
        self.assertRaises(NotImplementedError, self.pdf.eval_log, 0.)
        self.assertRaises(NotImplementedError, self.pdf.sample)


class TestGaussPdf(ut.TestCase):
    """Test Gaussian pdf"""

    def setUp(self):
        self.mean = np.array([1., 3., 9.])
        self.covariance = np.array([
            [1., 0., 0.],
            [0., 2., 0.],
            [0., 0., 3.]
        ])
        self.variance = np.array([1., 2., 3.])  # diagonal elements of covariance
        self.shape = (3,)  # shape of random variable (and mean)
        self.gauss = pb.GaussPdf(self.mean, self.covariance)

    def test_init(self):
        self.assertEqual(type(self.gauss), pb.GaussPdf)

    def test_invalid_init(self):
        constructor = pb.GaussPdf

        # invalid mean and variance shape
        self.assertRaises(ValueError, constructor, np.array([[1], [2]]), self.covariance)
        self.assertRaises(ValueError, constructor, self.mean, np.array([1., 2., 3.,]))

        # non-rectangular variance, incompatible mean and variance, non-symmetric variance
        self.assertRaises(ValueError, constructor, self.mean, np.array([
            [1., 2.],
            [3., 4.],
            [5., 6.]
        ]))
        self.assertRaises(ValueError, constructor, self.mean, np.array([
            [1., 2.],
            [3., 4.]
        ]))
        self.assertRaises(ValueError, constructor, np.array([1, 2]), np.array([
            [1, 2],
            [3, 4]
        ]))

        # TODO: non positive-definite variance

    def test_shape(self):
        self.assertEqual(self.gauss.shape(), self.shape)

    def test_mean(self):
        self.assertTrue(np.all(self.gauss.mean() == self.mean))

    def test_variance(self):
        self.assertTrue(np.all(self.gauss.variance() == self.variance))

    #def test_eval_log(self):  # TODO
        #x = [
            #self.mean,
            #np.array([0., 0., 0.])
        #]
        #exp = [
            #np.array([1, 2, 3]),  # TODO
            #np.array([1, 2, 3])  # TODO
        #]
        #for i in xrange(len(x)):
            #print "GaussPdf.eval_log(" + str(x[i]) + ") =", self.gauss.eval_log(x[i]), "(expected", str(exp[i]) + ")"

    def test_sample(self):
        # we cannost test values, just test right dimension and shape
        x = self.gauss.sample()
        self.assertEqual(x.ndim, 1)
        self.assertEqual(x.shape[0], self.mean.shape[0])

        # single dimension
        #normal = pb.pdfs.GaussPdf(np.array([0.]), np.array([[1.]]))
        #values = []
        #for i in xrange(0, 100):
            #values.extend(normal.sample())
        #print values
