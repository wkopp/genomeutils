from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from collections import defaultdict


def sequencesFromFasta(fasta):
    """ Obtain fasta-formated sequences from a fasta file.

    Parameters
    -----------
    fasta : str
        Filename of the fastafile

    Returns
        List of Biostring sequences
    """

    h = open(fasta)
    gen = SeqIO.parse(h, "fasta")
    seqs = [item for item in gen]

    return seqs


def sequencesForRegions(regions, refgenome):
    """ Obtain fasta-formated sequences for a given bedfile and a ref. genome.

    Parameters
    -----------
    bedfile : str
        Filename of the bedfile
    refgenome : str
        Location of the ref. genome

    Returns
        List of Biostring sequences
    """

    # genome, e.g. hg19.fa
    h = open(refgenome)
    genome = SeqIO.to_dict(SeqIO.parse(h, "fasta"))

    # remove all random chromosomes
    regions = regions[regions.chr.apply(
                      lambda el: False if len(el.split("_")) > 1 else True)]

    # extract a list of sequences in fasta format
    seqs = list()
    for row in regions.iterrows():
        id_ = row[1].chr+":"+str(row[1].start)+"-"+str(row[1].end)
        seqs.append(SeqRecord(
            genome[row[1].chr].seq[row[1].start:row[1].end],
            id=id_, name='', description=''))

    return seqs


def writeSequences(seqs, filename):
    """ Obtain fasta-formated sequences for a given bedfile and a ref. genome.

    Parameters
    -----------
    seqs : list
        List of Biostring sequences
    filename : str
        Filename of the fasta output file
    """

    SeqIO.write(seqs, filename, "fasta")


LETTERMAP = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'a': 0, 'c': 1, 'g': 2, 't': 3}

NMAP = defaultdict(lambda: -1)
NMAP.update(LETTERMAP)


def dna2ind(seq):
    """ Transforms a nucleotide sequence into an int8 array.

    In this array, we use the mapping
    {'A':0, 'C':1, 'G':2, 'T':3}
    """

    if isinstance(seq, str):
        return map(lambda x: NMAP[x], seq)
    elif isinstance(seq, SeqRecord):
        return map(lambda x: NMAP[x], str(seq.seq))
    else:
        raise Exception('dna2ind: Format is not supported')
