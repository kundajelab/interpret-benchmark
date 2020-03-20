from __future__ import division, print_function
from collections import namedtuple


MotifHit = namedtuple('MotifHit', ['motifid', 'seqid', 'start', 'end',
                                   'onposstrand', 'score', 'pval',
                                   'qval', 'matchedseq'])


def motifhit_to_str(motifhit):
    return (motifhit.motifid+"_"+"pos-"+str(motifhit.onposstrand)
            +"_"+str(motifhit.start)+"-"+str(motifhit.end)
            +"_"+str(motifhit.score)
            +"_"+str(motifhit.pval)
            +"_"+str(motifhit.qval)
            +"_"+str(motifhit.matchedseq))


def motifhit_from_str(motifstring, seqid):
    (motifid, strandinfo, startendinfo,
     scorestr, pvalstr, qvalstr, matchedseq) = motifstring.split("_") 
    onposstrandstr = strandinfo.split("-")[1]
    assert onposstrandstr in ["True", "False"]
    onposstrand = onposstrandstr=="True"
    startstr, endstr = startendinfo.split("-")
    start = int(startstr)
    end = int(endstr)
    score = float(scorestr)
    pval = float(pvalstr)
    qval = float(qvalstr)
    return MotifHit(motifid=motifid, seqid=seqid,
                    start=start, end=end, onposstrand=onposstrand,
                    score=score, pval=pval, qval=qval,
                    matchedseq=matchedseq) 
