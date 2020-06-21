import numpy as np

from libvis.interface import preprocess_value, add_serializer
from libvis.interface import reset_IFC
from libvis import VisObject
from libvis import ref


def test_preprocess_visobject():
    x = VisObject(1)
    value, type_ = preprocess_value(x)
    assert type_ == 'VisVar'
    assert value == ref(x)

def test_preprocess_numpy():
    x = np.array([1, 2, 3])
    value, type_ = preprocess_value(x)
    assert type_ == 'raw'
    assert value == x.tolist()

def test_add_serializer():
    def ser(x):
        return 'kaka'+str(x)
    try:

        x = VisObject(1)
        add_serializer(type(x), ser)
        value, type_ = preprocess_value(x)
        assert type_ == 'VisVar'
        assert value == ser(x)

        assert value == ser(x)

        x = np.array([1, 2, 3])
        add_serializer(type(x), ser)
        value, type_ = preprocess_value(x)
        assert type_ == 'ndarray'
        assert value == ser(x)

    finally:
        reset_IFC()
