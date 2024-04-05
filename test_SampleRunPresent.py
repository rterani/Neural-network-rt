"""Testing for Asst Five"""
#
# DO NOT MODIFY THIS CODE
#


import os


def test_sample_run_present():
    """Confirm that student uploaded a sample run."""
    assert os.path.isfile("samplerun"), \
        "Did you commit and push a file called samplerun?"
