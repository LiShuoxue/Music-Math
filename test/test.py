import json
import numpy as np
from chaintmat import ChainTmat

spacedict = json.load(open("notes.json", "r")) # 导入状态空间映射(音符 -> 索引值)
invspacedict = json.load(open("notes_inv.json", "r"))
inv = invspacedict

def file2chain(fname): return [spacedict[x] for x in open(fname, "r").read().split()]
def chain2file(chain, fname): f=open(fname, "w"); f.write("\n".join([inv[str(x)] for x in chain])); f.close()

mm = ChainTmat(dim=len(invspacedict))

if __name__ == "__main__":
    nfile = input("Number of input score file: ")
    for x in range(int(nfile)):
        mm.append(file2chain(input("({}/{}) Filname: ".format(x+1, nfile))))
    mm.chain2tmat()
    tmat = mm.matrix
    matdir = input("Direction of transfer matrix file: ")
    matfile = open(matdir, "w")
    for x in range(len(invspacedict)):
        for y in range(len(invspacedict)):
            if tmat[x][y] != 0:
                matfile.write("P({} -> {}) = {}\n".format(
                    invspacedict[str(x)], invspacedict[str(y)], tmat[x][y]))
    matfile.close()
    mlen = input("Maximum number of notes in random music: ")
    chain = mm.tmat2chain(maxlength=int(mlen))
    outfile = input("Direction of output score file: ")
    chain2file(chain, outfile)
