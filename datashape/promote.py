from __future__ import absolute_import

import numpy as np
import datashape


__all__ = ['promote', 'optionify']


def promote(lhs, rhs):
    """Promote two scalar dshapes to a possibly larger, but compatible type.

    Examples
    --------
    >>> from datashape import int32, int64, Option
    >>> x = Option(int32)
    >>> y = int64
    >>> promote(x, y)
    ?int64
    >>> promote(int64, int64)
    ctype("int64")

    Notes
    ----
    This uses ``numpy.result_type`` for type promotion logic.  See the numpy
    documentation at
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.result_type.html
    """
    if lhs == rhs:
        return lhs
    else:
        left, right = getattr(lhs, 'ty', lhs), getattr(rhs, 'ty', rhs)
        dtype = np.result_type(datashape.to_numpy_dtype(left),
                               datashape.to_numpy_dtype(right))
        return optionify(lhs, rhs, datashape.CType.from_numpy_dtype(dtype))


def optionify(lhs, rhs, dshape):
    """Check whether a binary operation's dshape came from
    :class:`~datashape.coretypes.Option` typed operands and construct an
    :class:`~datashape.coretypes.Option` type accordingly.

    Examples
    --------
    >>> from datashape import int32, int64, Option
    >>> x = Option(int32)
    >>> x
    ?int32
    >>> y = int64
    >>> y
    ctype("int64")
    >>> optionify(x, y, int64)
    ?int64
    """
    if hasattr(dshape.measure, 'ty'):
        return dshape
    if hasattr(lhs, 'ty') or hasattr(rhs, 'ty'):
        return datashape.Option(dshape)
    return dshape
