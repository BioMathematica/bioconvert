# -*- coding: utf-8 -*-

###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Authors: see CONTRIBUTORS.rst                                           #
# Copyright © 2018  Institut Pasteur, Paris and CNRS.                     #
# See the COPYRIGHT file for details                                      #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
###########################################################################

"""Convert :term:`Fastq` format to :term:`Fastq` formats"""
from bioconvert import ConvBase
import colorlog

from bioconvert.core.base import ConvArg
from bioconvert.core.decorators import requires

_log = colorlog.getLogger(__name__)


__all__ = ["Fasta2Fastq"]


class Fasta2Fastq(ConvBase):
    """

    """
    input_ext = ['.fa', '.fas', '.fasta']
    output_ext = ['.fastq', 'fq']
    _default_method = "pysam"

    def __init__(self, infile, outfile):
        """
        :param str infile: The path to the input FASTA file
        :param str outfile: The path to the output FASTQ file
        """
        super().__init__(infile, outfile)

    @requires(python_library="pysam")
    def _method_pysam(self, quality_file=None, *args, **kwargs):
        from pysam import FastxFile
        if quality_file is None:
            _log.warning("No quality file provided. Please use --quality-file")
            with open(self.outfile, 'w') as fastq_out:
                for seq in FastxFile(self.infile):
                    fastq_out.write("@{0} {1}\n{2}\n+\n{3}\n".format(seq.name,
                                                                 seq.comment,
                                                                 seq.sequence,
                                                                 len(seq.sequence) * "I"))
        else: # length must be equal and identifiers sorted similarly
            with open(self.outfile, "w") as fastq_out:
                for seq, qual in zip(FastxFile(self.infile), FastxFile(quality_file)):
                    assert seq.name == qual.name
                    fastq_out.write("@{0} {1}\n{2}\n+\n{3}\n".format(seq.name,
                                                                 seq.comment,
                                                                 seq.sequence,
                                                                 qual.sequence))


    @classmethod
    def get_additional_arguments(cls):
        yield ConvArg(
            names="--quality-file",
            nargs="?",
            default=None,
            type=ConvArg.file,
            help="The path to the quality file.",
        )
