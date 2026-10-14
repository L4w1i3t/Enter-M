# ENTER M -- additional ordinary story slots for larger ensembles.
#
# One through six retain their existing positions and motion. Seven/eight cast
# members use the same motion families with narrower spacing and a wider shot.
# Every transform has its own ATL source location so Autofocus can identify
# copied/restored transforms after save/load. Keep these declarations explicit.
# Backgrounds retain the six-panel cap and existing neighbour grouping.

transform t71:
    tcommon(91, 0.58)
transform t72:
    tcommon(274, 0.58)
transform t73:
    tcommon(457, 0.58)
transform t74:
    tcommon(640, 0.58)
transform t75:
    tcommon(823, 0.58)
transform t76:
    tcommon(1006, 0.58)
transform t77:
    tcommon(1189, 0.58)
transform t81:
    tcommon(80, 0.54)
transform t82:
    tcommon(240, 0.54)
transform t83:
    tcommon(400, 0.54)
transform t84:
    tcommon(560, 0.54)
transform t85:
    tcommon(720, 0.54)
transform t86:
    tcommon(880, 0.54)
transform t87:
    tcommon(1040, 0.54)
transform t88:
    tcommon(1200, 0.54)

transform i71:
    tinstant(91, 0.58)
transform i72:
    tinstant(274, 0.58)
transform i73:
    tinstant(457, 0.58)
transform i74:
    tinstant(640, 0.58)
transform i75:
    tinstant(823, 0.58)
transform i76:
    tinstant(1006, 0.58)
transform i77:
    tinstant(1189, 0.58)
transform i81:
    tinstant(80, 0.54)
transform i82:
    tinstant(240, 0.54)
transform i83:
    tinstant(400, 0.54)
transform i84:
    tinstant(560, 0.54)
transform i85:
    tinstant(720, 0.54)
transform i86:
    tinstant(880, 0.54)
transform i87:
    tinstant(1040, 0.54)
transform i88:
    tinstant(1200, 0.54)

transform f71:
    focus(91, 0.58)
transform f72:
    focus(274, 0.58)
transform f73:
    focus(457, 0.58)
transform f74:
    focus(640, 0.58)
transform f75:
    focus(823, 0.58)
transform f76:
    focus(1006, 0.58)
transform f77:
    focus(1189, 0.58)
transform f81:
    focus(80, 0.54)
transform f82:
    focus(240, 0.54)
transform f83:
    focus(400, 0.54)
transform f84:
    focus(560, 0.54)
transform f85:
    focus(720, 0.54)
transform f86:
    focus(880, 0.54)
transform f87:
    focus(1040, 0.54)
transform f88:
    focus(1200, 0.54)

transform h71:
    hop(91, 0.58)
transform h72:
    hop(274, 0.58)
transform h73:
    hop(457, 0.58)
transform h74:
    hop(640, 0.58)
transform h75:
    hop(823, 0.58)
transform h76:
    hop(1006, 0.58)
transform h77:
    hop(1189, 0.58)
transform h81:
    hop(80, 0.54)
transform h82:
    hop(240, 0.54)
transform h83:
    hop(400, 0.54)
transform h84:
    hop(560, 0.54)
transform h85:
    hop(720, 0.54)
transform h86:
    hop(880, 0.54)
transform h87:
    hop(1040, 0.54)
transform h88:
    hop(1200, 0.54)

transform hf71:
    hopfocus(91, 0.58)
transform hf72:
    hopfocus(274, 0.58)
transform hf73:
    hopfocus(457, 0.58)
transform hf74:
    hopfocus(640, 0.58)
transform hf75:
    hopfocus(823, 0.58)
transform hf76:
    hopfocus(1006, 0.58)
transform hf77:
    hopfocus(1189, 0.58)
transform hf81:
    hopfocus(80, 0.54)
transform hf82:
    hopfocus(240, 0.54)
transform hf83:
    hopfocus(400, 0.54)
transform hf84:
    hopfocus(560, 0.54)
transform hf85:
    hopfocus(720, 0.54)
transform hf86:
    hopfocus(880, 0.54)
transform hf87:
    hopfocus(1040, 0.54)
transform hf88:
    hopfocus(1200, 0.54)

transform l71:
    leftin(91, 0.58)
transform l72:
    leftin(274, 0.58)
transform l73:
    leftin(457, 0.58)
transform l74:
    leftin(640, 0.58)
transform l75:
    leftin(823, 0.58)
transform l76:
    leftin(1006, 0.58)
transform l77:
    leftin(1189, 0.58)
transform l81:
    leftin(80, 0.54)
transform l82:
    leftin(240, 0.54)
transform l83:
    leftin(400, 0.54)
transform l84:
    leftin(560, 0.54)
transform l85:
    leftin(720, 0.54)
transform l86:
    leftin(880, 0.54)
transform l87:
    leftin(1040, 0.54)
transform l88:
    leftin(1200, 0.54)

transform lf71:
    leftfocus(91, 0.58)
transform lf72:
    leftfocus(274, 0.58)
transform lf73:
    leftfocus(457, 0.58)
transform lf74:
    leftfocus(640, 0.58)
transform lf75:
    leftfocus(823, 0.58)
transform lf76:
    leftfocus(1006, 0.58)
transform lf77:
    leftfocus(1189, 0.58)
transform lf81:
    leftfocus(80, 0.54)
transform lf82:
    leftfocus(240, 0.54)
transform lf83:
    leftfocus(400, 0.54)
transform lf84:
    leftfocus(560, 0.54)
transform lf85:
    leftfocus(720, 0.54)
transform lf86:
    leftfocus(880, 0.54)
transform lf87:
    leftfocus(1040, 0.54)
transform lf88:
    leftfocus(1200, 0.54)

# Extend the lookups before Autofocus installs defaults at init 999 and the
# story framing seam is installed at init 1000. Existing entries stay intact.
init 998 python:
    _autofocus_slots += (
        "71", "72", "73", "74", "75", "76", "77",
        "81", "82", "83", "84", "85", "86", "87", "88")
    ENTER_M_PANEL_SLOT_X.update({
        "71": 91, "72": 274, "73": 457, "74": 640,
        "75": 823, "76": 1006, "77": 1189,
        "81": 80, "82": 240, "83": 400, "84": 560,
        "85": 720, "86": 880, "87": 1040, "88": 1200,
    })

