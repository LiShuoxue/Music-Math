# note_parser
# Author:   Bingqi Li   <bqli@pku.edu.cn>
#           Shuoxue Li  <1620480103.qq.com>

"""
Generate dictionaries which map notes to state index.
"""

import json


def pitch2index(pitch, io:int, eo:int):
    # Rest
    if pitch == "R":
        return 12 * (eo - io) + 1
    shift = 0
    procind = 0
    # normal pitch
    while pitch[procind] in ["b","#"]: #"e.g. bC; #G; ##F; bbG"
        shift += {"b":-1,"#":1}[pitch[procind]]
        procind += 1
    shift += {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}[pitch[procind]]
    res = shift + 12 * (int(pitch[-1]) - io)
    if res < 0 or res > 12 * (eo - io):
        return -1
    return res

def timing2index(timing, d:dict):
    res = d.get(timing)
    if res == None: res = -1
    return res

def note2index(note, io, eo, d:dict, lentd):
    l = note.split("@")
    i1 = pitch2index(l[0], io, eo)
    i2 = timing2index(l[1], d)
    # Anomalous Input
    if i1 == -1 or i2 == -1: 
        return -1
    else: 
        return i1 * lentd + i2

def index2pitch(index, io):
    d = {
        0: "C", 1: "#C", 2: "D", 3: "bE",
        4: "E", 5: "F", 6: "#F", 7: "G",
        8: "bA", 9: "A", 10: "bB", 11: "B"
    }
    ro, pind = index // 12, index % 12
    return d[pind] + str(ro + io)

def index2timing(index, dinv:dict): return dinv[index]

def index2note(index:int, io:int, dinv:dict, lentd:int):
    pind, tind = index // lentd, index % lentd
    pitch = index2pitch(pind, io)
    timing = index2timing(tind, dinv)
    return pitch + "@" + timing


if __name__ == "__main__":

    io = 4; eo = 6 #valid pitch from C4 to C6
    pitch_dict, note_dict = {}, {}
    pinv_dict, ninv_dict = {}, {}
    timing_dict = {
        "1":0, "2p":1, "2":2, "4p":3,
        "4":4, "8p":5, "8":6, "16p":7,
        "16":8
        }
    tinv_dict = {
        0:"1", 1:"2p", 2:"2", 3:"4p",
        4:"4", 5:"8p", 6:"8", 7:"16p",
        8:"16"
        }
    lentd = 9

    # Pitches
    for i in range(io, eo+1):
        for j in range(7):
            for k in range(5):
                pitch = ["","b","bb","#","##"][k] + ["C","D","E","F","G","A","B"][j] + str(i)
                if pitch2index(pitch, io, eo) != -1:
                    pitch_dict["%s"%pitch] = pitch2index(pitch, io, eo)
    if pitch2index("R", io, eo) != -1:
        pitch_dict["%s"%"R"] = pitch2index("R", io, eo)


    # Notes
    for i in range(io, eo+1):
        for j in range(7):
            for k in range(5):
                for l in timing_dict.keys():
                    pitch = ["","b","bb","#","##"][k] + ["C","D","E","F","G","A","B"][j] + str(i)
                    timing = l
                    note = pitch + "@" + timing
                    if note2index(note, io, eo, timing_dict, lentd) != -1:
                        note_dict["%s"%note] = note2index(note, io, eo, timing_dict, lentd)
    for l in timing_dict.keys():
        timing = l
        note = "R@" + timing
        if note2index(note, io, eo, timing_dict, lentd) != -1:
            note_dict["%s"%note] = note2index(note, io, eo, timing_dict, lentd)
    
    for ind in range(12 * (eo - io) + 2): pinv_dict[ind] = index2pitch(ind, io)
    for ind in range((12 * (eo - io) + 2) * lentd): ninv_dict[ind] = index2note(ind, io, tinv_dict, lentd)

    open("pitch.json", "w").write(json.dumps(pitch_dict, indent=4))
    open("timing.json", "w").write(json.dumps(timing_dict, indent=4))
    open("notes.json", "w").write(json.dumps(note_dict, indent=4))
    open("pitch_inv.json", "w").write(json.dumps(pinv_dict, indent=4))
    open("timing_inv.json", "w").write(json.dumps(tinv_dict, indent=4))
    open("notes_inv.json", "w").write(json.dumps(ninv_dict, indent=4))
