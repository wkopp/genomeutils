import pandas as pd


def readBed(bedfile, trunc=None, usecols=[0, 1, 2],
            names=["chr", "start", "end"], sortBy=None):
    """ Read content of a bedfile as pandas dataframe. """

    # currently I am only interested in using cols 1-3
    bed = pd.read_csv(bedfile, sep="\t", header=None, usecols=usecols,
                      names=names)

    if isinstance(sortBy, str):
        bed.sort_values(sortBy, ascending=False, inplace=True)

    if isinstance(trunc, int):
        if trunc < 0:
            raise Exception('readBed: trunc must be greater than zero.')

        bed.start = (bed.end - bed.start)//2 + bed.start - trunc
        bed.end = bed.start + 2*trunc

    return bed
