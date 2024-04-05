import pytest
import math

#
# DO NOT MODIFY THIS CODE
#
try:
    import RMSE
except ImportError:
    pytest.fail("Cannot import RMSE. Is RMSE.py present?")


def test_RMSE():
    try:
        RMSE.Euclidean
    except TypeError:
        pytest.fail("Is the Euclidean class defined?")


def test_Euclidean_as_child_class():
    my_obj = RMSE.Euclidean()
    assert isinstance(my_obj, RMSE.RMSE), \
        "Is Euclidean inherited from RMSE?"


def test_Euclidean_no_entries():
    errors = RMSE.Euclidean()
    assert errors.error == 0, \
        "Euclidean should return an error of 0 if no entries have been added."


def test_Euclidean_add():
    errors = RMSE.Euclidean()
    errors = errors + ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors = errors + ((.2, .1, .8, .1), (0, 0, 1, 0))
    errors = errors + ((.5, .5, .1, .7), (0, 0, 0, 1))
    final_errors = errors + ((.2, .6, .1, .9), (0, 0, 0, 1))
    assert math.isclose(final_errors.error, 0.7280109889280518), \
        ("Euclidean error property is not returning the correct value after "
         "entries have been added using +")
    assert final_errors is not errors, \
        ("__add__ method should create and return a new object.")


def test_Euclidean_iadd_present():
    errors = RMSE.Euclidean()
    try:
        errors.__iadd__(((.1, .7, .3, .9), (0, 1, 0, 0)))
    except:
        pytest.fail("Error calling __iadd__ for Euclidean object. Is "
                    "__iadd__ implemented?")


def test_Euclidean_iadd():
    errors = RMSE.Euclidean()
    stat_errors = errors
    errors += ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors += ((.2, .1, .8, .1), (0, 0, 1, 0))
    errors += ((.5, .5, .1, .7), (0, 0, 0, 1))
    errors += ((.2, .6, .1, .9), (0, 0, 0, 1))
    assert math.isclose(errors.error, 0.7280109889280518), \
        ("Euclidean error property is not returning the correct value after "
         "entries have been added using +=")
    assert stat_errors is errors, \
        ("__iadd__ method should not create a new object.")

def test_Euclidean_reset():
    errors = RMSE.Euclidean()
    errors = errors + ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors.reset()
    assert errors.error == 0, \
        ("Euclidean error property should return zero after reset.")

def test_Euclidean_no_overwrite():
    assert RMSE.Euclidean.__iadd__ is RMSE.RMSE.__iadd__, \
        "Euclidean should not overwrite RMSE.__iadd__."
    assert RMSE.Euclidean.__add__ is RMSE.RMSE.__add__, \
        "Euclidean should not overwrite RMSE.__iadd__."
