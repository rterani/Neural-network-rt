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
        RMSE.Taxicab
    except TypeError:
        pytest.fail("Is the Taxicab class defined?")


def test_Taxicab_as_child_class():
    my_obj = RMSE.Taxicab()
    assert isinstance(my_obj, RMSE.RMSE), \
        "Is Taxicab inherited from RMSE?"


def test_Taxicab_no_entries():
    errors = RMSE.Taxicab()
    assert errors.error == 0, \
        "Taxicab should return an error of 0 if no entries have been added."


def test_Taxicab_add():
    errors = RMSE.Taxicab()
    errors = errors + ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors = errors + ((.2, .1, .8, .1), (0, 0, 1, 0))
    errors = errors + ((.5, .5, .1, .7), (0, 0, 0, 1))
    final_errors = errors + ((.2, .6, .1, .9), (0, 0, 0, 1))
    assert math.isclose(final_errors.error, 1.2124355652982142), \
        ("Taxicab error property is not returning the correct value after "
         "entries have been added using +")
    assert final_errors is not errors, \
        ("__add__ method should create and return a new object.")


def test_Taxicab_iadd_present():
    errors = RMSE.Taxicab()
    try:
        errors.__iadd__(((.1, .7, .3, .9), (0, 1, 0, 0)))
    except:
        pytest.fail("Error calling __iadd__ for Taxicab object. Is "
                    "__iadd__ implemented?")


def test_Taxicab_iadd():
    errors = RMSE.Taxicab()
    stat_errors = errors
    errors += ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors += ((.2, .1, .8, .1), (0, 0, 1, 0))
    errors += ((.5, .5, .1, .7), (0, 0, 0, 1))
    errors += ((.2, .6, .1, .9), (0, 0, 0, 1))
    assert math.isclose(errors.error, 1.2124355652982142), \
        ("Taxicab error property is not returning the correct value after "
         "entries have been added using +=")
    assert stat_errors is errors, \
        ("__iadd__ method should not create a new object.")

def test_Taxicab_reset():
    errors = RMSE.Taxicab()
    errors = errors + ((.1, .7, .3, .9), (0, 1, 0, 0))
    errors.reset()
    assert errors.error == 0, \
        ("Taxicab error property should return zero after reset.")

def test_Taxicab_no_overwrite():
    assert RMSE.Taxicab.__iadd__ is RMSE.RMSE.__iadd__, \
        "Taxicab should not overwrite RMSE.__iadd__."
    assert RMSE.Taxicab.__add__ is RMSE.RMSE.__add__, \
        "Taxicab should not overwrite RMSE.__iadd__."
