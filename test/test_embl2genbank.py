from bioconvert import bioconvert_data
from easydev import TempFile, md5
import pytest
from bioconvert.embl2genbank import EMBL2GENBANK



@pytest.mark.parametrize("method", EMBL2GENBANK.available_methods)
def test_conv(method):
    infile = bioconvert_data("JB409847.embl")

    with TempFile(suffix=".gbk") as tempfile:
        converter = EMBL2GENBANK(infile, tempfile.name)
        converter(method=method)

        # Check that the output is correct with a checksum
        if method == "biopython":
            assert md5(tempfile.name) == "cdd34902975a68e58ad5f105b44ff495"
        elif method == "squizz":
            pass
            # TODO
            # embl input is not understood by squizz if generated by biopython
            #     assert md5(tempfile.name) == "????"
        else:
            raise NotImplementedError

