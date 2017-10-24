import os
import pytest
from easydev import TempFile, md5

from bioconvert import bioconvert_data
from fasta2phylip import FASTA2PHYLIP

skiptravis = pytest.mark.skipif("TRAVIS_PYTHON_VERSION" in os.environ
                                and os.environ['TRAVIS_PYTHON_VERSION'].startswith("2"), reason="On travis")


@skiptravis
def test_conv():
    infile = bioconvert_data("fa2phy.fasta")
    outfile = bioconvert_data("fa2phy_desired_output.phylip")
    with TempFile(suffix=".phylip") as tempfile:
        convert = FASTA2PHYLIP(infile, tempfile.name)
        convert()

        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(outfile)
