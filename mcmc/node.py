#!/usr/bin/env python

from __future__ import division
from scipy import special, stats
import random, math
from math import pi

DEFAULT_SAMPLE_STDDEV = .2

def sample_generator(*nodes, **kwds):
    print 'Starting the sampler'
    if 'output_rate' in kwds:
        output_rate = kwds['output_rate']
    else:
        output_rate = 500
    i = 0
    while True:
        i += 1
        if i%output_rate == 0:
            print 'Yielding the %dth sample' % i
        sample = dict()
        for node in nodes:
            sample[node.name] = node.sample()
        yield sample


class Constant(object):
    def __init__(self, value, name=''):
        self.value = value
        self.name = name
        self.children = []


class MetropolisNode(object):
    def __init__(self, value, name, observed):
        self.value = value
        self.name = name
        self.observed = observed
        self.children = []
        self.sample_stddev = DEFAULT_SAMPLE_STDDEV

    def generate_candidate(self, prev_value, stddev):
        return random.normalvariate(mu=prev_value, sigma=stddev)

    def sample(self):
        if self.observed:
            return self.value
        cand = self.generate_candidate(self.value, self.sample_stddev)
        if self.outside_support(cand):
            return self.value
        old_log_lh = self.loglikelihood()
        old_value = self.value
        self.value = cand
        new_log_lh = self.loglikelihood()

        u = math.log(random.uniform(0, 1))
        if u > (new_log_lh - old_log_lh):
            self.value = old_value

        return self.value

    def loglikelihood(self):
        log_lh = self.logconditional()
        for child in self.children:
                log_lh += child.logconditional()
        return log_lh

    def logconditional(self):
        raise NotImplementedError()

    def outside_support(self, candidate):
        raise NotImplementedError()

    def density_function(self):
        raise NotImplementedError()


class NormalNode(MetropolisNode):
    def __init__(self, initial_value, name='', mean=None, var=None,
            observed=False):
        super(NormalNode, self).__init__(initial_value, name, observed)
        self.mean = mean
        mean.children.append(self)
        self.var = var
        var.children.append(self)

    def logconditional(self):
        var = self.var.value
        mean = self.mean.value
        if var == 0:
            if self.value == self.mean:
                return float('inf')
            else:
                return -float('inf')
        return -1/2 * (math.log(2*pi*var) + .5/var * (self.value - mean)**2)

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return False

    def density_function(self):
        mean = self.mean.value
        var = self.var.value
        return lambda x: stats.norm.pdf(x, loc=mean, scale=math.sqrt(var))


class NormalNodeNonNegative(MetropolisNode):
    def __init__(self, initial_value, name='', mean=None, var=None,
            observed=False):
        super(NormalNodeNonNegative, self).__init__(initial_value, name,
                observed)
        self.mean = mean
        mean.children.append(self)
        self.var = var
        var.children.append(self)

    def logconditional(self):
        var = self.var.value
        mean = self.mean.value
        if var == 0:
            if self.value == self.mean:
                return float('inf')
            else:
                return -float('inf')
        return -1/2 * (math.log(2*pi*var) + .5/var * (self.value - mean)**2)

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return candidate <= 0

    def density_function(self):
        mean = self.mean.value
        var = self.var.value
        return lambda x: stats.norm.pdf(x, loc=mean, scale=math.sqrt(var))
    

class GammaNode(MetropolisNode):
    def __init__(self, initial_value, name='', shape=None, inv_scale=None,
            observed=False):
        super(GammaNode, self).__init__(initial_value, name, observed)
        self.shape = shape
        shape.children.append(self)
        self.inv_scale = inv_scale
        inv_scale.children.append(self)

    def logconditional(self):
        shape = self.shape.value
        inv_scale = self.inv_scale.value
        return (shape * math.log(inv_scale) - special.gammaln(shape) +
                (shape - 1) * math.log(self.value) - inv_scale * self.value)

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return candidate <= 0

    def density_function(self):
        shape = self.shape.value
        scale = 1/self.inv_scale.value
        return lambda x: stats.gamma.pdf(x, shape, scale=scale)


class InvGammaNode(MetropolisNode):
    def __init__(self, initial_value, name='', shape=None, scale=None,
            observed=False):
        super(InvGammaNode, self).__init__(initial_value, name, observed)
        self.shape = shape
        shape.children.append(self)
        self.scale = scale
        scale.children.append(self)

    def logconditional(self):
        shape = self.shape.value
        scale = self.scale.value
        return (shape * math.log(scale) - special.gammaln(shape) -
                (shape + 1) * math.log(self.value) - scale / self.value)

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return candidate <= 0

    def density_function(self):
        shape = self.shape.value
        scale = self.scale.value
        return lambda x: stats.invgamma.pdf(x, shape, scale=scale)


class PoissonNode(MetropolisNode):
    def __init__(self, initial_value, name='', lamda=None, observed=False):
        super(PoissonNode, self).__init__(initial_value, name, observed)
        self.lamda = lamda
        lamda.children.append(self)
    
    def logconditional(self):
        return (self.value * math.log(self.lamda.value) - self.lamda.value -
                special.gammaln(self.value + 1))

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return (type(candidate) != int or candidate < 0)
    
    def generate_candidate(self, pv, s):
        return int(round(super(PoissonNode, self).generate_candidate(pv, s)))

    def density_function(self):
        lamda = self.lamda.value
        return lambda x: stats.poisson.pmf(x, lamda)


class BetaNode(MetropolisNode):
    def __init__(self, initial_value, name='', alpha=None, beta=None,
            observed=False):
        super(BetaNode, self).__init__(initial_value, name, observed)
        self.alpha = alpha
        alpha.children.append(self)
        self.beta = beta
        beta.children.append(self)

    def logconditional(self):
        alpha = self.alpha.value
        beta = self.beta.value
        return (special.gammaln(alpha+beta) - special.gammaln(alpha) -
                special.gammaln(beta) + (alpha-1) * math.log(self.value) +
                (beta-1) * math.log(1-self.value))

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return 1 < candidate or candidate < 0

    def density_function(self):
        alpha = self.alpha.value
        beta = self.beta.value
        return lambda x: stats.beta.pdf(x, alpha, beta)


class BernoulliNode(MetropolisNode):
    def __init__(self, initial_value, name='', p=None, observed=False):
        super(BernoulliNode, self).__init__(initial_value, name, observed)
        self.p = p
        p.children.append(self)

    def logconditional(self):
        if self.value == 1:
            return math.log(self.p.value)
        else:
            return math.log(1-self.p.value)

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return candidate not in [0,1]

    def sample(self):
        if self.observed:
            return self.value
        self.value = 1
        p = self.loglikelihood()
        self.value = 0
        q = self.loglikelihood()
        u = math.log(random.uniform(0, 1))
        sum = log_sum(p, q)
        if u < p - sum:
            self.value = 1
        return self.value


class FixedConditionalBernoulliNode(MetropolisNode):
    def __init__(self, initial_value, name='', parents=None, p=None,
            observed=False):
        """This defines a Bernoulli whose p value depends only on whether or
        not its parents have true or false as their values.  p should be a
        dictionary of the form {(0, 1) : p} for each case, with the order
        of the values in the dictionary matching the order of the list of
        parents."""
        super(FixedConditionalBernoulliNode, self).__init__(initial_value,
                name, observed)
        self.parents = parents
        for parent in self.parents:
            parent.children.append(self)
        self.p = p

    def logconditional(self):
        case = []
        for parent in self.parents:
            case.append(parent.value)
        case = tuple(case)
        p = self.p[case].value
        if self.value == 1:
            return math.log(p)
        else:
            return math.log(1-p)

    def outside_support(self, candidate):
        return candidate not in [0,1]

    def sample(self):
        if self.observed:
            return self.value
        self.value = 1
        p = self.loglikelihood()
        self.value = 0
        q = self.loglikelihood()
        u = math.log(random.uniform(0, 1))
        sum = log_sum(p, q)
        if u < p - sum:
            self.value = 1
        return self.value


class BinomialNode(MetropolisNode):
    def __init__(self, initial_value, name='', n=None, p=None, observed=False):
        super(BinomialNode, self).__init__(initial_value, name, observed)
        self.n = n
        n.children.append(self)
        self.p = p
        p.children.append(self)

    def logconditional(self):
        n = self.n.value
        p = self.p.value
        return (special.gammaln(n+1) - special.gammaln(self.value+1) -
                special.gammaln(n-self.value+1) + self.value * math.log(p) +
                (n-self.value) * math.log(1-p))

    def outside_support(self, candidate):
        if candidate is None:
            return True
        return 0 > candidate or candidate > self.n.value
    
    def sample(self):
        '''This is wrong!!!  This only samples from the parents, not the 
        complete conditional.'''
        raise NotImplementedError('My binomial sampling is broken!')
        if self.observed:
            return self.value
        self.value = 0
        for i in range(self.n.value):
            u = random.uniform(0, 1)
            if u < self.p.value:
                self.value += 1
        return self.value


class FunctionNode(MetropolisNode):
    """Nodes that derive from this class simply combine other nodes in various
    ways, like adding, or selecting, or whatever.  Generally these function
    nodes will be created to replace the parameter to one node, so they should
    only have one child."""

    def logconditional(self):
        if len(self.children) != 1:
            raise ValueError('Something is not connected right...')
        return self.children[0].logconditional()


class SelectorNode(FunctionNode):
    def __init__(self, choices, selector):
        self.choices = choices
        self.selector = selector
        self.children = []
        for choice in self.choices:
            choice.children.append(self)
        selector.children.append(self)

    @property
    def value(self):
        return self.choices[self.selector.value].value
    

class AdderNode(FunctionNode):
    def __init__(self, parents):
        self.parents = parents
        self.children = []
        for parent in parents:
            parent.children.append(self)

    @property
    def value(self):
        return sum([p.value for p in self.parents])


class MultiplierNode(FunctionNode):
    def __init__(self, parents):
        self.parents = parents
        self.children = []
        for parent in parents:
            parent.children.append(self)

    @property
    def value(self):
        value = 1
        for p in self.parents:
            value *= p.value
        return value


class ExponentNode(FunctionNode):
    def __init__(self, base, exponent):
        self.base = base
        base.children.append(self)
        self.exponent = exponent
        exponent.children.append(self)
        self.children = []

    @property
    def value(self):
        return self.base.value**self.exponent.value


def log_sum(logx, logy):
    if logy > logx:
        logx, logy = logy, logx
    if logx == -float('inf'):
        return logx
    neg_diff = logy - logx
    if neg_diff < -50:
        return logx
    return logx + math.log(1+math.exp(neg_diff))


def main():
    pass


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
