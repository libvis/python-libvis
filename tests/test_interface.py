import numpy as np

from libvis.interface import preprocess_value, add_serializer
from libvis import VisObject
from libvis import ref


def test_preprocess_visobject():
    x = VisObject(1)
    value, type_ = preprocess_value(x)
    assert type_ == 'Object'
    assert value == ref(x)

def test_preprocess_numpy():
    x = np.array([1, 2, 3])
    value, type_ = preprocess_value(x)
    assert type_ == 'raw'
    assert value == x.tolist()

def test_add_serializer():
    def ser(x):
        return 'kaka'+str(x)

    x = VisObject(1)
    add_serializer(type(x), ser)
    value, type_ = preprocess_value(x)
    assert type_ == 'Object'
    assert value == ser(x)

    x = np.array([1, 2, 3])
    add_serializer(type(x), ser)
    value, type_ = preprocess_value(x)
    assert type_ == 'ndarray'
    assert value == ser(x)
