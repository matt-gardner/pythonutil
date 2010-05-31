#!/usr/bin/env python

from evilplot import Plot, Points, Density, Function

def plotmixing(samples, param_name, filename=None):
    p = Plot(title='%s mixing plot' % param_name)
    points = Points([(i,s[param_name]) for i,s in enumerate(samples)],
            style='lines')
    points.linewidth=1
    p.append(points)
    p.show()
    if filename:
        p.write(filename)

def plotposterior(samples, param_name, min=None, max=None, prior=None,
        filename=None):
    p = Plot(title='Posterior of %s' % param_name)
    density = Density([s[param_name] for s in samples], title='Posterior')
    p.append(density)
    if prior:
        priord = Function(prior, title='Prior')
        p.append(priord)
    if min is not None:
        p.xmin = min
    if max is not None:
        p.xmax = max
    p.show()
    if filename:
        p.write(filename)


# vim: et sw=4 sts=4
