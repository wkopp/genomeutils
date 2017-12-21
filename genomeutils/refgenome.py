import os
import sys
import tarfile
import re
import pandas as pd
if sys.version_info[0] < 3:
    from urllib import urlcleanup, urlretrieve
else:
    from urllib.request import urlcleanup, urlretrieve


def downloadRefGenome(refgenome='hg19', output='./datapath/hg19.fa',
                      skipRandom=True):
    """ This function downloads a copy of hg19 as a single fasta file
    in case it is absent. If the 'output' file already exists, nothing will
    be done.

    Note: The function only downloads the normal chromosomes ans skips the
    random chromosomes.

    Parameters
    -----------
    refgenome : str
        Ref. genome name
    output : str
        Location of the ref. genome
    skipRandom : bool
        Skips random chromosomes, if set true. (Default: skipRandom=True)
    """

    if os.path.exists(output):
        return

    urlpath = 'http://hgdownload.cse.ucsc.edu/goldenPath/{}/bigZips/chromFa.tar.gz'.format(refgenome)
    tmpfile = "{}.tmp".format(output)

    # From the md5sum.txt we extract the
    print("Downloading {}".format(urlpath))
    urlcleanup()
    urlretrieve(urlpath.format(refgenome), tmpfile)

    print("Unpack genome into {}.fa".format(refgenome))
    with open(output, 'wb') as ofile:
        with tarfile.open(tmpfile, 'r:gz') as archive:
            for tarinfo in archive:
                if skipRandom and re.search(tarinfo.name, '_'):
                    # random chromosomes
                    # skip this file
                    continue

                ofile.write(archive.extractfile(tarinfo.name).read())

    os.unlink(tmpfile)
    print("Done.")


def getGenomeSize(refgenome='hg19', outputdir='./', skipRandom=True):
    """ Get genome size."""

    outputfile = os.path.join(outputdir, '{}.chrom.sizes'.format(refgenome))
    if not os.path.exists(outputfile):

        urlpath = 'http://hgdownload.cse.ucsc.edu/goldenPath/{}/bigZips/{}.chrom.sizes'.format(refgenome, refgenome)

        # From the md5sum.txt we extract the
        print("Downloading {}".format(urlpath))
        urlcleanup()
        urlretrieve(urlpath.format(refgenome), outputfile)

    content = pd.read_csv(outputfile, sep='\t', names=['chr', 'length'],
                          index_col='chr')
    if skipRandom:
        fltr = [True if len(name.split('_')) <= 1 else False for name in content.index]
        content = content[fltr]
    return content.to_dict()['length']
