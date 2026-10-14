# =============================================================================
# ag_chess.rpy  --  BOARD MEETING   (Arcade Original #5)
# =============================================================================
# Chess, dressed as the meeting nobody in the lab can get out of. Four people
# will sit across the table from you, and the only thing on the agenda is you.
#
# WHY THIS IS ON THE SHELF
#   The other five originals are all about the next ten seconds. This one is
#   about the next ten minutes, and it is the only cabinet with a real opponent
#   rather than a rule. Containment Sweep asks you to deduce against a board
#   that does not care; Board Meeting asks you to deduce against something that
#   is deducing back.
#
# WHAT IS ACTUALLY IN HERE
#   A complete chess engine. Not a move-picker with a lookup table -- a real
#   0x88 board with legal castling, en passant, promotion, the fifty-move rule,
#   threefold repetition and insufficient-material draws, under an alpha-beta
#   search with a transposition table, killers, history, null-move pruning,
#   late move reductions and a quiescence search. Move generation is verified
#   against the standard perft positions (start / Kiwipete / positions 3-5) to
#   depth 4-5, exactly.
#
# THE ONE STRUCTURAL TRICK: A SEARCH THAT CAN BE PAUSED
#   A chess search takes seconds. A frame takes sixteen milliseconds. The whole
#   search -- alpha-beta, quiescence, all of it -- is therefore written as
#   PYTHON GENERATORS wired together with `yield from`: every node yields every
#   few hundred nodes, and the cabinet advances the search for a slice of a
#   millisecond budget each frame and hands the frame straight back. The engine
#   resumes mid-recursion on the next frame with its entire tree intact. That is
#   why the opponent can think for four seconds without the cabinet dropping a
#   single frame, and why none of this needed a thread.
#
# THE FOUR OPPONENTS  (the variant card picks one)
#   CASUAL       shallow, deliberately noisy, no clock. Thinks out loud -- its
#                assessment of the position is on the panel, which makes it a
#                teaching opponent as much as an easy one.
#   COMPETITIVE  a full search on a real budget, a little noise. 30 s per move.
#   GRANDMASTER  the deepest search this cabinet can afford, no noise, opening
#                book, and it will take a draw off you rather than lose. 30 s
#                per move -- the same window as COMPETITIVE, by design.
#   ADAPTIVE     builds a model OF YOU while you play and moves its own strength
#                and style to match. No clock. The model is on the panel so you
#                can watch it read you, and it is thrown away when the game ends
#                -- nothing about it survives into the next game or the session.
#
#   Honest note on GRANDMASTER: it is the strongest opponent that fits in a
#   Python search inside a 60Hz displayable -- roughly depth 6-8 in the
#   middlegame with a full quiescence. That is a very strong club player, not
#   literally Carlsen. Nothing in Matsu'Py can be literally Carlsen.
#
# ART
#   game/addons/Arcade/sprites/chess_sheet.png -- 6 columns (pawn, rook, knight,
#   bishop, queen, king) x 4 rows, where rows 2 and 4 are the REFLECTIONS of
#   rows 1 and 3. Only the two piece rows are used on the board; the reflections
#   are used on the box art. Sprites are drawn at 1.3x with a blurred silhouette
#   under them -- measured against the alternative (a contrasting halo), the
#   shadow alone reads better on both square colours because both piece sets
#   already carry their own rim shading.
# =============================================================================

init python:
    import math
    import random
    import time

    # =========================================================================
    # LOOK
    # =========================================================================
    AGC_ACCENT = "#8fa8ff"          # cold institutional blue
    AGC_LIGHT = "#d7cfc0"           # light square: warm bone
    AGC_DARK = "#4a4266"            # dark square: violet slate
    AGC_MARK = "#e0c05e"            # last move
    AGC_SEL = "#8fe0b0"             # your selection
    # Where you may move to. ONE marker colour cannot read on both squares --
    # a mid mint sits too close in value to the bone light square -- so the
    # marker is toned to the square it lands on and keeps the hue for the
    # language.
    AGC_MOVE_ON_LIGHT = "#1a6b45"
    AGC_MOVE_ON_DARK = "#a6f2c8"
    AGC_THREAT = "#e0455e"          # check

    AGC_CELL = 64
    AGC_BX = 80                     # board is a FIXED size at every difficulty,
    AGC_BY = 122                    # so nothing on screen has to move for it
    AGC_BW = AGC_CELL * 8
    AGC_ZOOM = 1.3

    AGC_PX = 632                    # right-hand column of plates
    AGC_PW = 588

    AGC_SHEET = "addons/Arcade/sprites/chess_sheet.png"

    # =========================================================================
    # RULES CONSTANTS
    # Everything an init python block defines lands in the global store, so
    # every name here is prefixed. Piece codes are `type | (colour << 3)`, which
    # makes `p & 7` the type and `p >> 3` the colour with no table lookup.
    # =========================================================================
    AGC_PAWN, AGC_KNIGHT, AGC_BISHOP = 1, 2, 3
    AGC_ROOK, AGC_QUEEN, AGC_KING = 4, 5, 6
    AGC_WHITE, AGC_BLACK = 0, 1

    AGC_WP, AGC_WN, AGC_WB, AGC_WR, AGC_WQ, AGC_WK = 1, 2, 3, 4, 5, 6
    AGC_BP, AGC_BN, AGC_BB, AGC_BR, AGC_BQ, AGC_BK = 9, 10, 11, 12, 13, 14

    # The 64 playable squares of the 128-entry 0x88 board. Everything off the
    # board fails `sq & 0x88`, including the negative results of a downward
    # offset -- the largest offset in play is 33, and every value in [-33, -1]
    # has bit 7 set under Python's arbitrary-precision two's complement.
    AGC_SQ64 = [r * 16 + f for r in range(8) for f in range(8)]

    AGC_ND = (33, 31, 18, 14, -33, -31, -18, -14)       # knight
    AGC_BD = (17, 15, -17, -15)                          # bishop
    AGC_RD = (16, 1, -16, -1)                            # rook
    AGC_KD = (17, 16, 15, 1, -1, -15, -16, -17)          # king / queen

    AGC_VALUE = [0, 100, 320, 330, 500, 900, 0, 0,
                    0, 100, 320, 330, 500, 900, 0, 0]
    AGC_PHASE_OF = [0, 0, 1, 1, 2, 4, 0, 0,
                    0, 0, 1, 1, 2, 4, 0, 0]
    AGC_PHASE_TOTAL = 24

    AGC_MATE = 30000
    AGC_INF = 40000

    AGC_C_WK, AGC_C_WQ, AGC_C_BK, AGC_C_BQ = 1, 2, 4, 8

    # --- piece-square tables (printed rank 8 first, from White's side) --------
    AGC_T_P = [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0]
    AGC_T_P_EG = [
        0, 0, 0, 0, 0, 0, 0, 0,
        90, 90, 90, 90, 90, 90, 90, 90,
        60, 60, 60, 60, 60, 60, 60, 60,
        35, 35, 35, 35, 35, 35, 35, 35,
        20, 20, 20, 20, 20, 20, 20, 20,
        10, 10, 10, 10, 10, 10, 10, 10,
        5, 5, 5, 5, 5, 5, 5, 5,
        0, 0, 0, 0, 0, 0, 0, 0]
    AGC_T_N = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50]
    AGC_T_B = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20]
    AGC_T_R = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0]
    AGC_T_Q = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20]
    AGC_T_K = [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20]
    AGC_T_K_EG = [
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -30, 0, 0, 0, 0, -30, -30,
        -50, -30, -30, -30, -30, -30, -30, -50]

    # AGC_MGV[piece][square] and AGC_EGV[...] fold material INTO the table and
    # pre-sign it for colour, so make/unmake maintains the whole positional
    # score with two adds per moved piece and eval never walks the board.
    AGC_MGV = [[0] * 128 for _i in range(16)]
    AGC_EGV = [[0] * 128 for _i in range(16)]
    _agc_mg_by = {AGC_PAWN: AGC_T_P, AGC_KNIGHT: AGC_T_N, AGC_BISHOP: AGC_T_B,
                    AGC_ROOK: AGC_T_R, AGC_QUEEN: AGC_T_Q, AGC_KING: AGC_T_K}
    _agc_eg_by = {AGC_PAWN: AGC_T_P_EG, AGC_KNIGHT: AGC_T_N,
                    AGC_BISHOP: AGC_T_B, AGC_ROOK: AGC_T_R, AGC_QUEEN: AGC_T_Q,
                    AGC_KING: AGC_T_K_EG}
    for _pt in range(1, 7):
        for _sq in AGC_SQ64:
            _wi = (7 - (_sq >> 4)) * 8 + (_sq & 7)   # White reads it as printed
            _bi = (_sq >> 4) * 8 + (_sq & 7)         # Black reads it mirrored
            AGC_MGV[_pt][_sq] = AGC_VALUE[_pt] + _agc_mg_by[_pt][_wi]
            AGC_EGV[_pt][_sq] = AGC_VALUE[_pt] + _agc_eg_by[_pt][_wi]
            AGC_MGV[_pt | 8][_sq] = -(AGC_VALUE[_pt] + _agc_mg_by[_pt][_bi])
            AGC_EGV[_pt | 8][_sq] = -(AGC_VALUE[_pt] + _agc_eg_by[_pt][_bi])

    # Castling rights are cleared by TOUCHING a square, from either end: this
    # one table handles "the rook moved", "the king moved" and "the rook was
    # captured where it stood" in a single AND per move.
    AGC_CMASK = [15] * 128
    AGC_CMASK[0] = 15 & ~AGC_C_WQ
    AGC_CMASK[4] = 15 & ~(AGC_C_WK | AGC_C_WQ)
    AGC_CMASK[7] = 15 & ~AGC_C_WK
    AGC_CMASK[112] = 15 & ~AGC_C_BQ
    AGC_CMASK[116] = 15 & ~(AGC_C_BK | AGC_C_BQ)
    AGC_CMASK[119] = 15 & ~AGC_C_BK

    # Its own Random so seeding/consuming the shared `random` stream elsewhere
    # can never shift the hash keys mid-session.
    _agc_zr = random.Random(0xC4E55)
    AGC_ZP = [[_agc_zr.getrandbits(64) for _i in range(128)] for _j in range(16)]
    AGC_ZSIDE = _agc_zr.getrandbits(64)
    AGC_ZCASTLE = [_agc_zr.getrandbits(64) for _i in range(16)]
    AGC_ZEP = [_agc_zr.getrandbits(64) for _i in range(8)]

    AGC_PASSED = (0, 8, 14, 26, 46, 80, 130, 0)

    def agc_sqname(sq):
        return "abcdefgh"[sq & 7] + "12345678"[sq >> 4]

    def agc_uci(mv):
        s = agc_sqname(mv & 0xFF) + agc_sqname((mv >> 8) & 0xFF)
        p = (mv >> 16) & 0xFF
        return s + " nbrq"[p - 1] if p else s


    # =========================================================================
    # THE BOARD
    # Rules only. No search, no drawing, no Matsu'Py.
    # =========================================================================
    class AGCBoard(object):

        START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        def __init__(self, fen=None):
            self.set_fen(fen or AGCBoard.START)

        # ---- setup ----------------------------------------------------------

        def set_fen(self, fen):
            self.b = [0] * 128
            parts = fen.split()
            codes = {"P": AGC_WP, "N": AGC_WN, "B": AGC_WB, "R": AGC_WR,
                        "Q": AGC_WQ, "K": AGC_WK, "p": AGC_BP, "n": AGC_BN,
                        "b": AGC_BB, "r": AGC_BR, "q": AGC_BQ, "k": AGC_BK}
            for ri, row in enumerate(parts[0].split("/")):
                rank = 7 - ri
                f = 0
                for ch in row:
                    if ch.isdigit():
                        f += int(ch)
                    else:
                        self.b[rank * 16 + f] = codes[ch]
                        f += 1
            self.stm = AGC_WHITE if parts[1] == "w" else AGC_BLACK
            self.castle = 0
            for ch, bit in (("K", AGC_C_WK), ("Q", AGC_C_WQ),
                            ("k", AGC_C_BK), ("q", AGC_C_BQ)):
                if ch in parts[2]:
                    self.castle |= bit
            self.ep = -1
            if len(parts) > 3 and parts[3] != "-":
                self.ep = ("abcdefgh".index(parts[3][0])
                            + (int(parts[3][1]) - 1) * 16)
            self.half = int(parts[4]) if len(parts) > 4 else 0
            self._resync()

        def _resync(self):
            self.ksq = [-1, -1]
            self.count = [0] * 16
            self.mg = 0
            self.eg = 0
            self.phase = 0
            z = 0
            pz = 0
            for sq in AGC_SQ64:
                p = self.b[sq]
                if not p:
                    continue
                self.count[p] += 1
                self.mg += AGC_MGV[p][sq]
                self.eg += AGC_EGV[p][sq]
                self.phase += AGC_PHASE_OF[p]
                z ^= AGC_ZP[p][sq]
                if (p & 7) == AGC_PAWN:
                    pz ^= AGC_ZP[p][sq]
                elif (p & 7) == AGC_KING:
                    self.ksq[p >> 3] = sq
            z ^= AGC_ZCASTLE[self.castle]
            if self.ep >= 0:
                z ^= AGC_ZEP[self.ep & 7]
            if self.stm:
                z ^= AGC_ZSIDE
            self.zob = z
            self.pz = pz
            self.undo = []
            self.path = []

        # ---- attacks --------------------------------------------------------

        def attacked(self, sq, by):
            """Is `sq` attacked by side `by`? Radiates OUT from the square
            looking for the piece that could be standing there, which is one
            scan instead of a move generation for the whole side."""
            b = self.b
            opp = by << 3
            if by == AGC_WHITE:
                t = sq - 17
                if not (t & 0x88) and b[t] == AGC_WP:
                    return True
                t = sq - 15
                if not (t & 0x88) and b[t] == AGC_WP:
                    return True
            else:
                t = sq + 17
                if not (t & 0x88) and b[t] == AGC_BP:
                    return True
                t = sq + 15
                if not (t & 0x88) and b[t] == AGC_BP:
                    return True
            n = AGC_KNIGHT | opp
            for d in AGC_ND:
                t = sq + d
                if not (t & 0x88) and b[t] == n:
                    return True
            k = AGC_KING | opp
            for d in AGC_KD:
                t = sq + d
                if not (t & 0x88) and b[t] == k:
                    return True
            bp = AGC_BISHOP | opp
            qp = AGC_QUEEN | opp
            for d in AGC_BD:
                t = sq + d
                while not (t & 0x88):
                    pc = b[t]
                    if pc:
                        if pc == bp or pc == qp:
                            return True
                        break
                    t += d
            rp = AGC_ROOK | opp
            for d in AGC_RD:
                t = sq + d
                while not (t & 0x88):
                    pc = b[t]
                    if pc:
                        if pc == rp or pc == qp:
                            return True
                        break
                    t += d
            return False

        def in_check(self, side=None):
            if side is None:
                side = self.stm
            return self.attacked(self.ksq[side], side ^ 1)

        # ---- move generation ------------------------------------------------

        def gen(self):
            """Every pseudo-legal move for the side to move. Legality (does this
            leave my own king en prise) is settled by make(), which unmakes and
            reports False -- one attacked() call on the moves that survive
            instead of pin detection on all of them."""
            b = self.b
            us = self.stm
            them = us ^ 1
            moves = []
            add = moves.append
            for frm in AGC_SQ64:
                p = b[frm]
                if not p or (p >> 3) != us:
                    continue
                pt = p & 7
                if pt == AGC_PAWN:
                    if us == AGC_WHITE:
                        step, start, last, caps = 16, 1, 6, (15, 17)
                    else:
                        step, start, last, caps = -16, 6, 1, (-15, -17)
                    to = frm + step
                    if not (to & 0x88) and not b[to]:
                        if (frm >> 4) == last:
                            base = frm | (to << 8)
                            add(base | (AGC_QUEEN << 16))
                            add(base | (AGC_ROOK << 16))
                            add(base | (AGC_BISHOP << 16))
                            add(base | (AGC_KNIGHT << 16))
                        else:
                            add(frm | (to << 8))
                            if (frm >> 4) == start and not b[to + step]:
                                add(frm | ((to + step) << 8))
                    for d in caps:
                        to = frm + d
                        if to & 0x88:
                            continue
                        tp = b[to]
                        if (tp and (tp >> 3) == them) or to == self.ep:
                            if (frm >> 4) == last:
                                base = frm | (to << 8)
                                add(base | (AGC_QUEEN << 16))
                                add(base | (AGC_ROOK << 16))
                                add(base | (AGC_BISHOP << 16))
                                add(base | (AGC_KNIGHT << 16))
                            else:
                                add(frm | (to << 8))
                    continue
                if pt == AGC_KNIGHT or pt == AGC_KING:
                    for d in (AGC_ND if pt == AGC_KNIGHT else AGC_KD):
                        to = frm + d
                        if to & 0x88:
                            continue
                        tp = b[to]
                        if not tp or (tp >> 3) == them:
                            add(frm | (to << 8))
                else:
                    if pt == AGC_BISHOP:
                        dirs = AGC_BD
                    elif pt == AGC_ROOK:
                        dirs = AGC_RD
                    else:
                        dirs = AGC_KD
                    for d in dirs:
                        to = frm + d
                        while not (to & 0x88):
                            tp = b[to]
                            if not tp:
                                add(frm | (to << 8))
                                to += d
                                continue
                            if (tp >> 3) == them:
                                add(frm | (to << 8))
                            break
            # Castling: rights, a clear path, and a king that is not in check
            # now, will not pass through check, and does not land in it.
            if us == AGC_WHITE:
                if ((self.castle & AGC_C_WK) and not b[5] and not b[6]
                        and not self.attacked(4, AGC_BLACK)
                        and not self.attacked(5, AGC_BLACK)
                        and not self.attacked(6, AGC_BLACK)):
                    add(4 | (6 << 8))
                if ((self.castle & AGC_C_WQ) and not b[3] and not b[2]
                        and not b[1] and not self.attacked(4, AGC_BLACK)
                        and not self.attacked(3, AGC_BLACK)
                        and not self.attacked(2, AGC_BLACK)):
                    add(4 | (2 << 8))
            else:
                if ((self.castle & AGC_C_BK) and not b[117] and not b[118]
                        and not self.attacked(116, AGC_WHITE)
                        and not self.attacked(117, AGC_WHITE)
                        and not self.attacked(118, AGC_WHITE)):
                    add(116 | (118 << 8))
                if ((self.castle & AGC_C_BQ) and not b[115] and not b[114]
                        and not b[113] and not self.attacked(116, AGC_WHITE)
                        and not self.attacked(115, AGC_WHITE)
                        and not self.attacked(114, AGC_WHITE)):
                    add(116 | (114 << 8))
            return moves

        def gen_captures(self):
            """Captures and queen promotions -- the quiescence move set."""
            b = self.b
            us = self.stm
            them = us ^ 1
            moves = []
            add = moves.append
            for frm in AGC_SQ64:
                p = b[frm]
                if not p or (p >> 3) != us:
                    continue
                pt = p & 7
                if pt == AGC_PAWN:
                    if us == AGC_WHITE:
                        step, last, caps = 16, 6, (15, 17)
                    else:
                        step, last, caps = -16, 1, (-15, -17)
                    if (frm >> 4) == last:
                        to = frm + step
                        if not (to & 0x88) and not b[to]:
                            add(frm | (to << 8) | (AGC_QUEEN << 16))
                    for d in caps:
                        to = frm + d
                        if to & 0x88:
                            continue
                        tp = b[to]
                        if (tp and (tp >> 3) == them) or to == self.ep:
                            if (frm >> 4) == last:
                                add(frm | (to << 8) | (AGC_QUEEN << 16))
                            else:
                                add(frm | (to << 8))
                    continue
                if pt == AGC_KNIGHT or pt == AGC_KING:
                    for d in (AGC_ND if pt == AGC_KNIGHT else AGC_KD):
                        to = frm + d
                        if to & 0x88:
                            continue
                        tp = b[to]
                        if tp and (tp >> 3) == them:
                            add(frm | (to << 8))
                else:
                    if pt == AGC_BISHOP:
                        dirs = AGC_BD
                    elif pt == AGC_ROOK:
                        dirs = AGC_RD
                    else:
                        dirs = AGC_KD
                    for d in dirs:
                        to = frm + d
                        while not (to & 0x88):
                            tp = b[to]
                            if tp:
                                if (tp >> 3) == them:
                                    add(frm | (to << 8))
                                break
                            to += d
            return moves

        def legal_moves(self):
            out = []
            for mv in self.gen():
                if self.make(mv):
                    self.unmake()
                    out.append(mv)
            return out

        # ---- make / unmake --------------------------------------------------

        def make(self, mv):
            """Play `mv`. Returns False -- already unmade -- if it was illegal.

            Keeps the hash, the pawn-only hash, the tapered score and the phase
            in step incrementally; the undo record carries every one of them so
            unmake() is a straight restore and never recomputes anything."""
            b = self.b
            frm = mv & 0xFF
            to = (mv >> 8) & 0xFF
            promo = (mv >> 16) & 0xFF
            p = b[frm]
            pt = p & 7
            us = p >> 3
            them = us ^ 1
            cap = b[to]
            capsq = to
            # En passant: the victim is not standing on the destination, so it
            # has to be found before the undo record is written.
            if not cap and pt == AGC_PAWN and to == self.ep:
                capsq = to - 16 if us == AGC_WHITE else to + 16
                cap = b[capsq]

            self.undo.append((mv, cap, capsq if cap else -1, self.castle,
                                self.ep, self.half, self.zob, self.mg, self.eg,
                                self.phase, self.pz))
            self.path.append(self.zob)
            pz = self.pz

            z = self.zob ^ AGC_ZCASTLE[self.castle]
            if self.ep >= 0:
                z ^= AGC_ZEP[self.ep & 7]

            if cap:
                b[capsq] = 0
                self.count[cap] -= 1
                self.mg -= AGC_MGV[cap][capsq]
                self.eg -= AGC_EGV[cap][capsq]
                self.phase -= AGC_PHASE_OF[cap]
                z ^= AGC_ZP[cap][capsq]
                if (cap & 7) == AGC_PAWN:
                    pz ^= AGC_ZP[cap][capsq]

            b[frm] = 0
            self.mg -= AGC_MGV[p][frm]
            self.eg -= AGC_EGV[p][frm]
            z ^= AGC_ZP[p][frm]
            if pt == AGC_PAWN:
                pz ^= AGC_ZP[p][frm]

            if promo:
                np = promo | (us << 3)
                b[to] = np
                self.count[p] -= 1
                self.count[np] += 1
                self.phase += AGC_PHASE_OF[np]
                self.mg += AGC_MGV[np][to]
                self.eg += AGC_EGV[np][to]
                z ^= AGC_ZP[np][to]
            else:
                b[to] = p
                self.mg += AGC_MGV[p][to]
                self.eg += AGC_EGV[p][to]
                z ^= AGC_ZP[p][to]
                if pt == AGC_PAWN:
                    pz ^= AGC_ZP[p][to]

            self.ep = -1
            if pt == AGC_PAWN:
                self.half = 0
                if to - frm == 32:
                    self.ep = frm + 16
                elif frm - to == 32:
                    self.ep = frm - 16
            elif cap:
                self.half = 0
            else:
                self.half += 1

            if pt == AGC_KING:
                self.ksq[us] = to
                d = to - frm
                if d == 2 or d == -2:
                    if d == 2:
                        rf, rt = frm + 3, frm + 1
                    else:
                        rf, rt = frm - 4, frm - 1
                    rook = b[rf]
                    b[rf] = 0
                    b[rt] = rook
                    self.mg += AGC_MGV[rook][rt] - AGC_MGV[rook][rf]
                    self.eg += AGC_EGV[rook][rt] - AGC_EGV[rook][rf]
                    z ^= AGC_ZP[rook][rf] ^ AGC_ZP[rook][rt]

            self.castle &= AGC_CMASK[frm] & AGC_CMASK[to]
            z ^= AGC_ZCASTLE[self.castle]
            if self.ep >= 0:
                z ^= AGC_ZEP[self.ep & 7]
            self.zob = z ^ AGC_ZSIDE
            self.pz = pz
            self.stm = them

            if self.attacked(self.ksq[us], them):
                self.unmake()
                return False
            return True

        def unmake(self):
            (mv, cap, capsq, castle, ep, half, zob, mg, eg, phase,
                pz) = self.undo.pop()
            self.path.pop()
            b = self.b
            frm = mv & 0xFF
            to = (mv >> 8) & 0xFF
            p = b[to]
            us = p >> 3

            if (mv >> 16) & 0xFF:
                self.count[p] -= 1
                p = AGC_PAWN | (us << 3)
                self.count[p] += 1
            b[frm] = p
            b[to] = 0
            if cap:
                b[capsq] = cap
                self.count[cap] += 1

            if (p & 7) == AGC_KING:
                self.ksq[us] = frm
                d = to - frm
                if d == 2 or d == -2:
                    if d == 2:
                        rf, rt = frm + 3, frm + 1
                    else:
                        rf, rt = frm - 4, frm - 1
                    b[rf] = b[rt]
                    b[rt] = 0

            self.castle = castle
            self.ep = ep
            self.half = half
            self.zob = zob
            self.pz = pz
            self.mg = mg
            self.eg = eg
            self.phase = phase
            self.stm = us

        def clone(self):
            """A detached copy of this position for the search to work in.

            THIS IS NOT AN OPTIMISATION, IT IS A CORRECTNESS REQUIREMENT. The
            search makes and unmakes thousands of moves on whatever board it is
            handed, and it is SUSPENDED MID-TREE between frames -- so a search
            sharing the game's board leaves it sitting in some position six
            plies down whenever its slice runs out, and that is the position
            draw() then paints. It shows up as a one-frame flash of pieces on
            the wrong squares just after you move (longer at the harder
            settings, where the search runs for hundreds of frames).

            `path` comes along so repetition detection inside the tree still
            sees the real game history; `undo` starts empty because the copy has
            nothing of its own to take back yet.
            """
            other = AGCBoard.__new__(AGCBoard)
            other.b = list(self.b)
            other.stm = self.stm
            other.castle = self.castle
            other.ep = self.ep
            other.half = self.half
            other.ksq = list(self.ksq)
            other.count = list(self.count)
            other.mg = self.mg
            other.eg = self.eg
            other.phase = self.phase
            other.zob = self.zob
            other.pz = self.pz
            other.undo = []
            other.path = list(self.path)
            return other

        def make_null(self):
            self.undo.append((0, 0, -1, self.castle, self.ep, self.half,
                                self.zob, self.mg, self.eg, self.phase, self.pz))
            self.path.append(self.zob)
            z = self.zob
            if self.ep >= 0:
                z ^= AGC_ZEP[self.ep & 7]
            self.ep = -1
            self.zob = z ^ AGC_ZSIDE
            self.stm ^= 1

        def unmake_null(self):
            (_m, _c, _cs, castle, ep, half, zob, mg, eg, phase,
                pz) = self.undo.pop()
            self.path.pop()
            self.castle = castle
            self.ep = ep
            self.half = half
            self.zob = zob
            self.pz = pz
            self.mg = mg
            self.eg = eg
            self.phase = phase
            self.stm ^= 1

        # ---- terminal states ------------------------------------------------

        def insufficient(self):
            """Bare kings, king and one minor, or two same-coloured bishops:
            positions in which no legal sequence of moves can mate."""
            c = self.count
            if c[AGC_WP] or c[AGC_BP] or c[AGC_WR] or c[AGC_BR] \
                    or c[AGC_WQ] or c[AGC_BQ]:
                return False
            minors = (c[AGC_WN] + c[AGC_WB] + c[AGC_BN] + c[AGC_BB])
            if minors <= 1:
                return True
            if minors == 2 and c[AGC_WB] == 1 and c[AGC_BB] == 1:
                sqs = [sq for sq in AGC_SQ64
                        if self.b[sq] == AGC_WB or self.b[sq] == AGC_BB]
                if len(sqs) == 2:
                    a = ((sqs[0] >> 4) + (sqs[0] & 7)) & 1
                    b2 = ((sqs[1] >> 4) + (sqs[1] & 7)) & 1
                    return a == b2
            return False

        def repetitions(self):
            """How many times the CURRENT position has already stood on the
            board this game. Only positions since the last irreversible move can
            match, so the walk is bounded by the halfmove clock."""
            z = self.zob
            path = self.path
            n = 0
            i = len(path) - 2
            limit = len(path) - self.half
            if limit < 0:
                limit = 0
            while i >= limit:
                if path[i] == z:
                    n += 1
                i -= 2
            return n

        # ---- notation -------------------------------------------------------

        def san(self, mv):
            """Standard algebraic notation, resolved against this position --
            so it has to be asked BEFORE the move is played."""
            frm = mv & 0xFF
            to = (mv >> 8) & 0xFF
            promo = (mv >> 16) & 0xFF
            p = self.b[frm]
            pt = p & 7
            cap = self.b[to] or (pt == AGC_PAWN and to == self.ep)

            if pt == AGC_KING and (to - frm == 2 or frm - to == 2):
                out = "O-O" if to > frm else "O-O-O"
            elif pt == AGC_PAWN:
                out = (("abcdefgh"[frm & 7] + "x") if cap else "") \
                    + agc_sqname(to)
                if promo:
                    out += "=" + " NBRQ"[promo - 1]
            else:
                mark = ""
                others = [m for m in self.legal_moves()
                            if ((m >> 8) & 0xFF) == to and (m & 0xFF) != frm
                            and self.b[m & 0xFF] == p]
                if others:
                    if all((o & 7) != (frm & 7) for o in others):
                        mark = "abcdefgh"[frm & 7]
                    elif all(((o >> 4) & 7) != (frm >> 4) for o in others):
                        mark = "12345678"[frm >> 4]
                    else:
                        mark = agc_sqname(frm)
                out = " NBRQK"[pt - 1] + mark + ("x" if cap else "") \
                    + agc_sqname(to)

            if self.make(mv):
                if self.in_check():
                    out += "#" if not self.legal_moves() else "+"
                self.unmake()
            return out


    # =========================================================================
    # THE SEARCH
    # Generators throughout. Each node yields every few hundred nodes and the
    # recursion is stitched with `yield from`, so AGChess can advance the search
    # for a millisecond budget per frame and resume mid-tree on the next one.
    # =========================================================================
    class AGCEngine(object):

        def __init__(self, bd):
            self.bd = bd
            self.tt = {}
            self.pawn_cache = {}
            self.killers = [[0, 0] for _i in range(80)]
            self.hist = [0] * 2048
            self.nodes = 0
            self.stop = False
            self.max_depth = 32
            self.root_scores = []
            self.best = 0
            self.best_score = 0
            self.depth_done = 0

        # ---- evaluation -----------------------------------------------------

        def pawn_term(self):
            """Doubled / isolated / passed pawns, memoised on a pawn-only hash.
            Pawn structure survives most moves, so however many leaves ask for
            this it is actually computed a handful of times per search."""
            got = self.pawn_cache.get(self.bd.pz)
            if got is not None:
                return got
            b = self.bd.b
            wlow = [8] * 8
            bhigh = [-1] * 8
            wn = [0] * 8
            bn = [0] * 8
            wsq = []
            bsq = []
            for sq in AGC_SQ64:
                p = b[sq]
                if p == AGC_WP:
                    f = sq & 7
                    r = sq >> 4
                    wn[f] += 1
                    if r < wlow[f]:
                        wlow[f] = r
                    wsq.append((f, r))
                elif p == AGC_BP:
                    f = sq & 7
                    r = sq >> 4
                    bn[f] += 1
                    if r > bhigh[f]:
                        bhigh[f] = r
                    bsq.append((f, r))
            s = 0
            for f in range(8):
                if wn[f] > 1:
                    s -= 14 * (wn[f] - 1)
                if bn[f] > 1:
                    s += 14 * (bn[f] - 1)
            for f, r in wsq:
                if (f == 0 or not wn[f - 1]) and (f == 7 or not wn[f + 1]):
                    s -= 16
                if (bhigh[f] <= r and (f == 0 or bhigh[f - 1] <= r)
                        and (f == 7 or bhigh[f + 1] <= r)):
                    s += AGC_PASSED[r]
            for f, r in bsq:
                if (f == 0 or not bn[f - 1]) and (f == 7 or not bn[f + 1]):
                    s += 16
                if (wlow[f] >= r and (f == 0 or wlow[f - 1] >= r)
                        and (f == 7 or wlow[f + 1] >= r)):
                    s -= AGC_PASSED[7 - r]
            if len(self.pawn_cache) > 20000:
                self.pawn_cache.clear()
            self.pawn_cache[self.bd.pz] = s
            return s

        def evaluate(self):
            """Centipawns, from the side to move's point of view."""
            bd = self.bd
            mg = bd.mg
            eg = bd.eg
            c = bd.count
            if c[AGC_WB] > 1:
                mg += 28
                eg += 42
            if c[AGC_BB] > 1:
                mg -= 28
                eg -= 42
            ps = self.pawn_term()
            mg += ps
            eg += (ps * 3) // 2
            ph = bd.phase
            if ph > AGC_PHASE_TOTAL:
                ph = AGC_PHASE_TOTAL
            s = ((mg * ph + eg * (AGC_PHASE_TOTAL - ph))
                    // AGC_PHASE_TOTAL)
            return s if bd.stm == AGC_WHITE else -s

        # ---- quiescence -----------------------------------------------------

        def qs(self, alpha, beta, ply):
            """Search on to a quiet position. Without this the engine happily
            'wins' a queen on the last ply of every line and never sees the
            recapture."""
            self.nodes += 1
            # Yield often enough that one resumption is a fraction of a frame:
            # at this engine's ~85k nodes/sec, 256 nodes is about 3ms, so the
            # cabinet can never overshoot its slice by more than that.
            if not (self.nodes & 255):
                yield
                if self.stop:
                    return alpha
            stand = self.evaluate()
            if stand >= beta:
                return beta
            if stand > alpha:
                alpha = stand
            if ply > 48:
                return alpha

            bd = self.bd
            b = bd.b
            scored = []
            for mv in bd.gen_captures():
                gain = AGC_VALUE[b[(mv >> 8) & 0xFF]]
                # Delta pruning: winning even this much material would not
                # bring the position up to alpha, so the line cannot matter.
                if not ((mv >> 16) & 0xFF) and stand + gain + 180 < alpha:
                    continue
                scored.append((gain * 16 - AGC_VALUE[b[mv & 0xFF]], mv))
            scored.sort(reverse=True)

            for _s, mv in scored:
                if not bd.make(mv):
                    continue
                s = yield from self.qs(-beta, -alpha, ply + 1)
                bd.unmake()
                if self.stop:
                    return alpha
                s = -s
                if s >= beta:
                    return beta
                if s > alpha:
                    alpha = s
            return alpha

        # ---- alpha-beta -----------------------------------------------------

        def ab(self, depth, alpha, beta, ply, null_ok):
            self.nodes += 1
            if not (self.nodes & 127):
                yield
                if self.stop:
                    return 0

            bd = self.bd
            # A repetition or a dead fifty-move counter INSIDE the tree is a
            # draw, which is what stops the engine shuffling in a won position.
            if ply and (bd.half >= 100 or bd.repetitions()):
                return 0

            alpha0 = alpha
            key = bd.zob
            entry = self.tt.get(key)
            ttmove = 0
            if entry is not None:
                e_depth, e_flag, e_score, e_mv = entry
                ttmove = e_mv
                if ply and e_depth >= depth:
                    if e_flag == 0:
                        return e_score
                    if e_flag == 1:
                        if e_score > alpha:
                            alpha = e_score
                    elif e_score < beta:
                        beta = e_score
                    if alpha >= beta:
                        return e_score

            in_chk = bd.in_check()
            if in_chk:
                depth += 1
            if depth <= 0:
                s = yield from self.qs(alpha, beta, ply)
                return s

            # Null move: give the opponent a free move and see if the position
            # still holds. Off in check and in near-pawn-only endings, where
            # passing is not the concession the heuristic assumes.
            if (null_ok and not in_chk and depth >= 3 and bd.phase > 3
                    and beta < AGC_MATE - 200):
                bd.make_null()
                s = yield from self.ab(depth - 3, -beta, -beta + 1, ply + 1,
                                        False)
                bd.unmake_null()
                if self.stop:
                    return 0
                if -s >= beta:
                    return beta

            b = bd.b
            k1, k2 = self.killers[ply] if ply < 80 else (0, 0)
            hist = self.hist
            scored = []
            for mv in bd.gen():
                if mv == ttmove:
                    scored.append((1 << 24, mv))
                    continue
                to = (mv >> 8) & 0xFF
                vic = b[to]
                if vic:
                    scored.append(((1 << 22) + AGC_VALUE[vic] * 16
                                    - AGC_VALUE[b[mv & 0xFF]], mv))
                elif (mv >> 16) & 0xFF:
                    scored.append(((1 << 22) + 800, mv))
                elif mv == k1:
                    scored.append(((1 << 21) + 2, mv))
                elif mv == k2:
                    scored.append(((1 << 21) + 1, mv))
                else:
                    scored.append((hist[(b[mv & 0xFF] << 7) | to], mv))
            scored.sort(reverse=True)

            best = -AGC_INF
            bestmv = 0
            legal = 0
            seval = None
            for _s, mv in scored:
                to = (mv >> 8) & 0xFF
                quiet = (not b[to]) and not ((mv >> 16) & 0xFF)

                # Futility: this close to the horizon, a quiet move in a
                # position already far below alpha will not rescue it. Never on
                # the first move, in check, or anywhere near a mate score.
                if (quiet and legal and depth <= 2 and not in_chk
                        and alpha > -AGC_MATE + 200
                        and beta < AGC_MATE - 200):
                    if seval is None:
                        seval = self.evaluate()
                    if seval + 90 + 110 * depth <= alpha:
                        continue

                if not bd.make(mv):
                    continue
                legal += 1

                if legal == 1:
                    s = yield from self.ab(depth - 1, -beta, -alpha, ply + 1,
                                            True)
                    s = -s
                else:
                    # Late move reduction: a quiet move this far down a
                    # well-ordered list is rarely the best one, so look at it
                    # shallowly and only pay full price if it surprises us.
                    red = 0
                    if (depth >= 3 and legal > 3 and quiet and not in_chk
                            and not bd.in_check()):
                        red = 1 if legal < 9 else 2
                        if red > depth - 2:
                            red = depth - 2
                    s = yield from self.ab(depth - 1 - red, -alpha - 1, -alpha,
                                            ply + 1, True)
                    s = -s
                    if s > alpha and (red or s < beta):
                        s = yield from self.ab(depth - 1, -beta, -alpha,
                                                ply + 1, True)
                        s = -s
                bd.unmake()
                if self.stop:
                    return 0

                if s > best:
                    best = s
                    bestmv = mv
                    if s > alpha:
                        alpha = s
                        if alpha >= beta:
                            # Only quiet cutoffs are worth remembering; a
                            # capture that cuts off is already ordered first.
                            if quiet:
                                if ply < 80 and mv != k1:
                                    self.killers[ply] = [mv, k1]
                                hist[(b[mv & 0xFF] << 7) | to] += depth * depth
                            break

            if not legal:
                return (-AGC_MATE + ply) if in_chk else 0

            # Mate scores are relative to this ply and would be wrong when read
            # back at another one, so they are simply not stored.
            if -AGC_MATE + 200 < best < AGC_MATE - 200:
                if len(self.tt) > 300000:
                    self.tt.clear()
                flag = 0 if alpha0 < best < beta else (1 if best >= beta else 2)
                self.tt[key] = (depth, flag, best, bestmv)
            return best

        # ---- the driver -----------------------------------------------------

        def think(self, moves=None):
            """Iterative deepening. root_scores ends up holding every root move
            scored by the DEEPEST COMPLETED iteration -- an aborted iteration is
            thrown away whole, so the engine never plays a half-searched move,
            and the difficulty layer always has a full ranking to sample."""
            bd = self.bd
            self.nodes = 0
            self.stop = False
            self.depth_done = 0
            order = list(moves) if moves else bd.legal_moves()
            if not order:
                self.best = 0
                self.root_scores = []
                return
            self.best = order[0]
            self.best_score = 0
            self.root_scores = [(0, m) for m in order]

            for depth in range(1, self.max_depth + 1):
                scores = []
                alpha = -AGC_INF
                first = True
                for mv in order:
                    if not bd.make(mv):
                        continue
                    if first:
                        s = yield from self.ab(depth - 1, -AGC_INF, AGC_INF,
                                                1, True)
                        s = -s
                    else:
                        # Principal variation search: prove the rest are worse
                        # with a null window and only pay full price when one
                        # is not.
                        s = yield from self.ab(depth - 1, -alpha - 1, -alpha,
                                                1, True)
                        s = -s
                        if s > alpha and not self.stop:
                            s = yield from self.ab(depth - 1, -AGC_INF, -alpha,
                                                    1, True)
                            s = -s
                    bd.unmake()
                    if self.stop:
                        break
                    first = False
                    scores.append((s, mv))
                    if s > alpha:
                        alpha = s
                if self.stop or len(scores) != len(order):
                    break
                scores.sort(key=lambda t: -t[0])
                self.root_scores = scores
                self.best = scores[0][1]
                self.best_score = scores[0][0]
                self.depth_done = depth
                order = [m for _s, m in scores]
                if abs(self.best_score) > AGC_MATE - 200:
                    break


    # =========================================================================
    # THE OPPONENTS
    # =========================================================================
    # budget  : SECONDS OF COMPUTE, accumulated across frames. Real time is
    #           roughly budget / AGC_SLICE frames -- a 2.4s budget at a 9ms
    #           slice is about 270 frames, i.e. four and a half seconds of the
    #           opponent visibly thinking.
    # noise   : centipawns of random offset added to every root score before the
    #           move is chosen. This is the whole weakening mechanism, and it is
    #           an honest one: the engine really does misjudge, rather than
    #           finding the best move and then throwing it away.
    # depth   : hard ceiling on iterative deepening, for CASUAL only.
    # clock   : seconds allowed for each of YOUR moves. 0 = untimed.
    AGC_SLICE = 0.009               # search time bought per frame
    AGC_LEVELS = {
        "casual": {
            "name": "CASUAL", "who": "THE INTERN",
            "note": "the intern  //  no clock  //  it thinks out loud",
            "budget": 0.10, "depth": 2, "noise": 110, "clock": 0,
            "book": False, "mult": 1.0, "minthink": 0.45,
        },
        "competitive": {
            "name": "COMPETITIVE", "who": "THE DEPARTMENT HEAD",
            "note": "the department head  //  30 s a move  //  opening book",
            "budget": 0.75, "depth": 32, "noise": 26, "clock": 30,
            "book": True, "mult": 2.0, "minthink": 0.8,
        },
        "grandmaster": {
            "name": "GRANDMASTER", "who": "THE CHAIR",
            "note": "the chair  //  30 s a move  //  nothing held back",
            "budget": 2.40, "depth": 32, "noise": 0, "clock": 30,
            "book": True, "mult": 3.5, "minthink": 1.0,
        },
        "adaptive": {
            "name": "ADAPTIVE", "who": "THE MODEL",
            "note": "the model  //  no clock  //  it reads you as you play",
            "budget": 0.60, "depth": 32, "noise": 60, "clock": 0,
            "book": True, "mult": 2.4, "minthink": 0.7,
        },
    }
    AGC_ORDER = ["casual", "competitive", "grandmaster", "adaptive"]

    # What the model calls itself at each strength. Purely a readout -- the
    # dial underneath is continuous.
    AGC_TIERS = [(0.20, "INTERN"), (0.42, "ANALYST"), (0.62, "SENIOR"),
                    (0.82, "DEPARTMENT HEAD"), (1.01, "THE CHAIR")]

    # A small book, keyed by the whole move sequence in UCI. Every hit is
    # checked against the legal move list before it is played, so a typo in
    # here costs a book move and nothing else.
    AGC_BOOK = {
        "": ["e2e4", "d2d4", "c2c4", "g1f3"],
        "e2e4": ["e7e5", "c7c5", "e7e6", "c7c6", "g8f6"],
        "e2e4 e7e5": ["g1f3"],
        "e2e4 e7e5 g1f3": ["b8c6", "g8f6"],
        "e2e4 e7e5 g1f3 b8c6": ["f1b5", "f1c4"],
        "e2e4 e7e5 g1f3 b8c6 f1b5": ["a7a6"],
        "e2e4 e7e5 g1f3 b8c6 f1c4": ["f8c5", "g8f6"],
        "e2e4 e7e5 f1c4": ["g8f6", "f8c5"],
        "e2e4 c7c5": ["g1f3"],
        "e2e4 c7c5 g1f3": ["d7d6", "b8c6", "e7e6"],
        "e2e4 c7c5 g1f3 d7d6": ["d2d4"],
        "e2e4 e7e6": ["d2d4"],
        "e2e4 e7e6 d2d4": ["d7d5"],
        "e2e4 c7c6": ["d2d4"],
        "e2e4 c7c6 d2d4": ["d7d5"],
        "e2e4 d7d5": ["e4d5"],
        "e2e4 d7d5 e4d5": ["d8d5", "g8f6"],
        "e2e4 g8f6": ["e4e5"],
        "e2e4 g8f6 e4e5": ["f6d5"],
        "e2e4 d7d6": ["d2d4"],
        "e2e4 g7g6": ["d2d4"],
        "d2d4": ["g8f6", "d7d5"],
        "d2d4 g8f6": ["c2c4"],
        "d2d4 g8f6 c2c4": ["e7e6", "g7g6"],
        "d2d4 d7d5": ["c2c4"],
        "d2d4 d7d5 c2c4": ["e7e6", "c7c6"],
        "d2d4 e7e6": ["c2c4"],
        "d2d4 g7g6": ["e2e4"],
        "d2d4 f7f5": ["g2g3"],
        "c2c4": ["e7e5", "g8f6", "c7c5"],
        "g1f3": ["g8f6", "d7d5"],
        "g1f3 g8f6": ["c2c4"],
    }


    class AGCModel(object):
        """The ADAPTIVE opponent's read on you.

        Two dials, both moved only by things that actually happened in THIS
        game, and both thrown away with the game object:

        STRENGTH -- how hard it plays. Driven by which way the position is
            running and by how much ground your last move gave up. It chases
            you in both directions on purpose: a beginner should not be ground
            down by a machine, and a strong player should not be able to coast.

        STYLE -- how it plays. Reads your aggression (how much of your play is
            captures and checks) and which wing you commit pieces to, then tilts
            its own root scoring: it trades and castles against a brawler, and
            it walks at your king when you are being quiet.
        """

        def __init__(self):
            self.level = 0.42          # 0..1, the strength dial
            self.aggr = 0.22        # rolling share of forcing moves
            self.moves = 0
            self.side = 0.0         # -1 queenside .. +1 kingside
            self.loss = 0.0         # rolling ground given up, in centipawns
            self.last_edge = None

        def tier(self):
            for cut, name in AGC_TIERS:
                if self.level < cut:
                    return name
            return "THE CHAIR"

        def style(self):
            if self.aggr > 0.34:
                return "AGGRESSIVE"
            if self.aggr < 0.15:
                return "CAUTIOUS"
            return "BALANCED"

        def focus(self):
            if self.side > 0.18:
                return "KINGSIDE"
            if self.side < -0.18:
                return "QUEENSIDE"
            return "THE CENTRE"

        def watch_move(self, bd, mv, was_capture, gave_check):
            """Called with the player's move, before it is played."""
            self.moves += 1
            forcing = 1.0 if (was_capture or gave_check) else 0.0
            self.aggr += (forcing - self.aggr) * 0.18
            f = (mv >> 8) & 7
            wing = 1.0 if f >= 5 else (-1.0 if f <= 2 else 0.0)
            self.side += (wing - self.side) * 0.14

        def watch_position(self, edge):
            """Called with the engine's own assessment after the player has
            moved, in centipawns from YOUR point of view.

            `edge` moving against you over one move is the cheapest honest proxy
            for 'that move cost you something' the cabinet can get without
            running a second search, and it costs nothing -- the engine was
            going to search this position anyway."""
            if self.last_edge is not None:
                drop = self.last_edge - edge
                if drop > 40:
                    self.loss += (min(drop, 400) - self.loss) * 0.3
                else:
                    self.loss += (0.0 - self.loss) * 0.2
                # Chase the game: if you are ahead it works harder, and if
                # it is running away with the game it eases off. Steps are
                # small on purpose -- measured against a random opponent, a
                # coarser dial oscillated for three hundred plies instead of
                # settling anywhere.
                if edge > 110:
                    self.level += 0.055
                elif -700 < edge < -260:
                    # Only while the game is still a game. Past that it stops
                    # easing and finishes, rather than declining to convert.
                    self.level -= 0.045
                # ...and chase the player: accurate moves pull it up.
                if drop > 130:
                    self.level -= 0.03
                elif drop < 25:
                    self.level += 0.028
                # The floor is well above nothing: an opponent that cannot
                # convert a won position is not an easy opponent, it is a
                # broken one.
                self.level = ag_clamp(self.level, 0.15, 1.0)
            self.last_edge = edge

        def budget(self):
            return 0.10 + 2.15 * (self.level ** 1.6)

        def noise(self):
            return int(round(120 * (1.0 - self.level) ** 1.5))

        def move_bonus(self, bd, mv):
            """The style tilt, applied to root scores only -- never inside the
            tree, where it would poison the search's own judgment."""
            to = (mv >> 8) & 0xFF
            bonus = 0
            if self.aggr > 0.34:
                # Brawler across the table: trade, and get the king off the file.
                if bd.b[to]:
                    bonus += 16
                p = bd.b[mv & 0xFF]
                if (p & 7) == AGC_KING and abs(to - (mv & 0xFF)) == 2:
                    bonus += 30
            elif self.aggr < 0.15:
                # Quiet across the table: walk at them.
                k = bd.ksq[AGC_WHITE]
                d = max(abs((to >> 4) - (k >> 4)), abs((to & 7) - (k & 7)))
                bonus += max(0, 22 - d * 4)
            if self.side > 0.18:
                bonus += 8 if (to & 7) <= 3 else 0
            elif self.side < -0.18:
                bonus += 8 if (to & 7) >= 4 else 0
            return bonus


    # =========================================================================
    # SPRITES
    # One cached displayable per piece code, plus a blurred silhouette that goes
    # down first. Both live in AGCanvas' displayable cache, so twelve renders a
    # frame carry all thirty-two men.
    # =========================================================================
    # (x, y, w, h) into chess_sheet.png -- tight bounds, measured off the alpha.
    AGC_SRC = {
        AGC_WP: (18, 18, 19, 28), AGC_WR: (42, 13, 21, 33),
        AGC_WN: (68, 12, 25, 34), AGC_WB: (100, 11, 20, 35),
        AGC_WQ: (128, 6, 21, 40), AGC_WK: (158, 3, 21, 43),
        AGC_BP: (19, 93, 18, 28), AGC_BR: (42, 88, 21, 33),
        AGC_BN: (69, 86, 24, 35), AGC_BB: (101, 85, 19, 36),
        AGC_BQ: (128, 82, 20, 39), AGC_BK: (158, 78, 21, 43),
    }
    # The reflection rows, used only by the box art.
    AGC_SRC_REF = {
        AGC_WN: (70, 47, 20, 30), AGC_WK: (160, 47, 17, 30),
        AGC_BN: (71, 123, 19, 29), AGC_BK: (160, 122, 17, 30),
    }

    def agc_piece(code, zoom=None):
        z = AGC_ZOOM if zoom is None else zoom
        rect = AGC_SRC[code]
        return Transform(Transform(AGC_SHEET, crop=rect), zoom=z)

    def agc_piece_shadow(code, zoom=None):
        """A blurred black silhouette of the sprite, dropped underneath it.

        mesh_pad is not decoration. `blur` flattens the child into a render of
        the child's OWN size and blurs inside it (accelerator.pyx), so with no
        room to spread the shadow gets cut off square at the sprite's bounding
        box. The two-value form pads right and bottom only, which leaves the
        content at the origin -- padding left/top would displace the sprite by
        exactly that much and put every shadow in the wrong place.
        """
        z = AGC_ZOOM if zoom is None else zoom
        rect = AGC_SRC[code]
        return Transform(Transform(AGC_SHEET, crop=rect), zoom=z,
                            matrixcolor=TintMatrix("#000000"), alpha=0.42,
                            blur=2.0, mesh_pad=(6, 6))

    def agc_disc(color, r, alpha=1.0):
        """A properly antialiased filled circle, built once and cached.

        Deliberately not the panel shader. enter_m.arcade_panel derives its
        rounded-rect half-size from the quad it is handed, so asking it for a
        circle of radius r puts the shape's edge exactly ON the quad edge and
        its whole 1.25px antialiasing band outside it, where it is clipped --
        which is why the move dots had flat 50%-alpha sides. Coverage is
        computed here at 4x4 subsamples per pixel and emitted as runs of equal
        alpha: one cached displayable, and the edge is right.
        """
        d = int(math.ceil(r * 2))
        parts = []
        for y in range(d):
            run_a = -1
            run_x = 0
            for x in range(d + 1):
                a = -1
                if x < d:
                    cov = 0
                    for sy in range(4):
                        sub_y = y + (sy + 0.5) * 0.25 - r
                        for sx in range(4):
                            sub_x = x + (sx + 0.5) * 0.25 - r
                            if sub_x * sub_x + sub_y * sub_y <= r * r:
                                cov += 1
                    a = int(round(255.0 * alpha * cov / 16.0))
                if a != run_a:
                    if run_a > 0:
                        parts.append(Transform(
                            Solid(color + "%02x" % run_a,
                                xysize=(x - run_x, 1)),
                            pos=(run_x, y)))
                    run_a = a
                    run_x = x
        return Fixed(*parts, xysize=(d, d))

    def agc_size(code, zoom=None):
        z = AGC_ZOOM if zoom is None else zoom
        rect = AGC_SRC[code]
        return (rect[2] * z, rect[3] * z)


    # =========================================================================
    # THE CABINET
    # =========================================================================
    class AGChess(AGGame):
        """Board Meeting: chess against four increasingly unreasonable people.

        You are White and you are at the bottom of the board, always. The
        opponent lives in self.eng; every rule question goes to self.bd.
        """

        KIND = "chess"
        TITLE = "BOARD MEETING"
        ACCENT = AGC_ACCENT
        MOUSE = True                # right-click cancels a selection, not pause
        CONTROLS = [
            ("CLICK a piece, CLICK a square", "move  (or drag it)"),
            ("RIGHT CLICK", "put the piece back"),
            ("ARROWS + Z", "the same, without a mouse"),
            ("X", "cancel"),
            ("ESC", "pause  //  Q while paused resigns"),
        ]

        # play states
        S_PLAY, S_THINK, S_PROMO, S_END = 0, 1, 2, 3

        def __init__(self, variant=None):
            super(AGChess, self).__init__(variant)

            key = variant if variant in AGC_LEVELS else "competitive"
            self.level_id = key
            self.lv = AGC_LEVELS[key]
            self.model = AGCModel() if key == "adaptive" else None

            self.bd = AGCBoard()
            # The engine works in its own copy of the position, replaced at the
            # start of every search -- see AGCBoard.clone() for why.
            self.eng = AGCEngine(self.bd.clone())
            self.human = AGC_WHITE

            self.state = AGChess.S_PLAY
            self.sel = -1               # selected square, or -1
            self.targets = {}           # destination square -> [moves]
            self.legal = self.bd.legal_moves()
            self.hover = -1
            self.cursor = 4             # keyboard cursor, starts on e1
            self.drag = None            # (from_square, mouse_x, mouse_y)
            self.promo = None           # (from, to, [moves])

            self.history = []           # SAN, one per ply
            self.uci = []               # UCI, for the book
            self.taken = [[], []]       # [captured by white, captured by black]
            self.last = (-1, -1)
            self.anim = None            # (piece, from, to, ticks) opponent slide

            self.clock = self.lv["clock"] * 60      # ticks left on your move
            self.clock_max = max(1, self.lv["clock"] * 60)
            self.warned = False

            self.search = None
            self.book_move = 0
            self.budget = self.lv["budget"]
            self.noise = self.lv["noise"]
            self.compute = 0.0
            self.think_ticks = 0
            self.frame = 0
            self._pumped = -1
            self.edge = 0               # engine's read, from YOUR point of view
            self.edge_known = False
            self.depth_shown = 0

            self.note = ""
            self.note_ticks = 0
            self.ending = 0
            self.won = None             # True / False / None(draw)
            self.end_head = ""
            self.end_line = ""
            self.moves_played = 0

        # ---- geometry -------------------------------------------------------

        def sq_xy(self, sq):
            """Top-left pixel of a square. White is at the bottom, so rank 8 is
            drawn first and the rank index is flipped."""
            return (AGC_BX + (sq & 7) * AGC_CELL,
                    AGC_BY + (7 - (sq >> 4)) * AGC_CELL)

        def xy_sq(self, px, py):
            if not (AGC_BX <= px < AGC_BX + AGC_BW
                    and AGC_BY <= py < AGC_BY + AGC_BW):
                return -1
            f = int((px - AGC_BX) // AGC_CELL)
            r = 7 - int((py - AGC_BY) // AGC_CELL)
            return r * 16 + f

        # ---- turn plumbing --------------------------------------------------

        def _say(self, text, ticks=150):
            self.note = text
            self.note_ticks = ticks

        def _refresh_targets(self):
            self.targets = {}
            if self.sel < 0:
                return
            for mv in self.legal:
                if (mv & 0xFF) == self.sel:
                    self.targets.setdefault((mv >> 8) & 0xFF, []).append(mv)

        def _select(self, sq):
            p = self.bd.b[sq]
            if p and (p >> 3) == self.human:
                self.sel = sq
                self._refresh_targets()
                if self.targets:
                    ag_se("ui_move", 0.5)
                else:
                    ag_se("deny", 0.35)
                return True
            return False

        def _try_move(self, to):
            """Play the selected piece to `to`, opening the promotion picker if
            the move is ambiguous only in what the pawn becomes."""
            opts = self.targets.get(to)
            if not opts:
                return False
            if len(opts) > 1:
                self.promo = (self.sel, to, opts)
                self.state = AGChess.S_PROMO
                ag_se("ui_move", 0.6)
                return True
            self._play(opts[0])
            return True

        def _play(self, mv):
            """Commit a move for whichever side is to move, and hand the turn
            over. Everything that has to happen exactly once per move -- the
            notation, the capture trays, the model's reading of you, the
            terminal checks -- happens here."""
            bd = self.bd
            frm = mv & 0xFF
            to = (mv >> 8) & 0xFF
            mover = bd.stm
            victim = bd.b[to]
            if not victim and (bd.b[frm] & 7) == AGC_PAWN and to == bd.ep:
                victim = bd.b[to - 16 if mover == AGC_WHITE else to + 16]

            text = bd.san(mv)
            if mover == self.human and self.model is not None:
                self.model.watch_move(bd, mv, bool(victim), text.endswith("+")
                                        or text.endswith("#"))

            if not bd.make(mv):
                ag_se("deny")
                return
            self.history.append(text)
            self.uci.append(agc_uci(mv))
            if victim:
                self.taken[mover].append(victim)
            self.last = (frm, to)
            self.sel = -1
            self.targets = {}
            self.moves_played += 1

            if victim:
                ag_se("smash", 0.65)
            elif (mv >> 16) & 0xFF:
                ag_se("bonus", 0.8)
            else:
                ag_se("lock", 0.55)

            if mover != self.human:
                self.anim = [bd.b[to], frm, to, 0]

            self.legal = bd.legal_moves()
            if bd.in_check():
                ag_se("level", 0.55)
                self._say("CHECK", 110)

            if self._terminal():
                return

            if bd.stm == self.human:
                self.state = AGChess.S_PLAY
                self.clock = self.lv["clock"] * 60
                self.warned = False
            else:
                self._begin_think()

        def _terminal(self):
            """Every way the game can be over, checked in the order the rules
            check them. Returns True if it is."""
            bd = self.bd
            if not self.legal:
                if bd.in_check():
                    self._finish_game(bd.stm != self.human,
                                        "CHECKMATE",
                                        "the motion carries" if bd.stm != self.human
                                        else "you are out of order")
                else:
                    self._finish_game(None, "STALEMATE",
                                        "no legal move, no check -- adjourned")
                return True
            if bd.half >= 100:
                self._finish_game(None, "FIFTY-MOVE DRAW",
                                    "fifty moves, nothing taken, nothing pushed")
                return True
            if bd.repetitions() >= 2:
                self._finish_game(None, "THREEFOLD REPETITION",
                                    "the same position, three times")
                return True
            if bd.insufficient():
                self._finish_game(None, "INSUFFICIENT MATERIAL",
                                    "nothing left on the table to mate with")
                return True
            return False

        def _finish_game(self, won, headline, line):
            self.won = won
            self.end_head = headline
            self.end_line = line
            self.state = AGChess.S_END
            self.ending = 1
            self._say(headline, 600)
            self.search = None
            if won is True:
                ag_se("clear")
            elif won is False:
                ag_se("over", 0.85)
            else:
                ag_se("ui_ok", 0.7)

        # ---- the opponent ---------------------------------------------------

        def _book_move(self):
            if not self.lv["book"]:
                return 0
            if self.model is not None and self.model.level < 0.3:
                return 0
            picks = AGC_BOOK.get(" ".join(self.uci))
            if not picks:
                return 0
            legal = dict((agc_uci(m), m) for m in self.legal)
            usable = [legal[u] for u in picks if u in legal]
            return random.choice(usable) if usable else 0

        def _begin_think(self):
            self.state = AGChess.S_THINK
            self.think_ticks = 0
            self.compute = 0.0
            self.depth_shown = 0

            mv = self._book_move()
            if mv:
                # Still pause on it: an instant book reply reads as a bug.
                self.search = None
                self.book_move = mv
                return
            self.book_move = 0

            if self.model is not None:
                self.eng.max_depth = 32
                self.budget = self.model.budget()
                self.noise = self.model.noise()
            else:
                self.eng.max_depth = self.lv["depth"]
                self.budget = self.lv["budget"]
                self.noise = self.lv["noise"]
            # A fresh copy per search. Moves are plain from/to ints, so the
            # legal list generated on the game board is valid on the copy.
            self.eng.bd = self.bd.clone()
            self.search = self.eng.think(list(self.legal))

        def _pump(self):
            """Advance the search for one frame's worth of milliseconds. Called
            at most once per RENDERED frame (see step), so a machine dropping
            frames gives the opponent less thinking time rather than stalling
            the whole cabinet trying to catch up."""
            if self.search is None:
                return
            # perf_counter, not time.time: on Windows time.time() ticks in
            # ~15ms steps, which is coarser than the whole slice being measured.
            t0 = time.perf_counter()
            deadline = t0 + AGC_SLICE
            try:
                while time.perf_counter() < deadline:
                    next(self.search)
            except StopIteration:
                self.compute += time.perf_counter() - t0
                self.search = None
                self.depth_shown = self.eng.depth_done
                return
            except Exception:
                self.search = None
                return
            self.compute += time.perf_counter() - t0
            self.depth_shown = self.eng.depth_done
            if self.compute >= self.budget:
                self.eng.stop = True
                try:
                    while True:
                        next(self.search)
                except StopIteration:
                    pass
                except Exception:
                    pass
                self.search = None
                self.depth_shown = self.eng.depth_done

        def _choose(self):
            """Turn the engine's ranking into the move this opponent plays.

            Weakening is done by disturbing the judgment, not the choice: a
            random offset goes onto every root score and the best of the
            disturbed list is played. A casual opponent therefore hangs a piece
            the way a person does -- because it misread the position -- rather
            than by finding the right move and discarding it.
            """
            scores = self.eng.root_scores
            if not scores:
                return random.choice(self.legal) if self.legal else 0

            # The engine's own view of the position, in YOUR favour, which is
            # what the panel shows and what the adaptive model reads.
            self.edge = -scores[0][0]
            self.edge_known = True
            if self.model is not None:
                self.model.watch_position(self.edge)

            noise = self.noise
            best_mv = scores[0][1]
            best_val = None
            for s, mv in scores:
                v = float(s)
                if noise:
                    v += random.gauss(0.0, noise)
                if self.model is not None:
                    v += self.model.move_bonus(self.bd, mv)
                if best_val is None or v > best_val:
                    best_val = v
                    best_mv = mv
            # Never talk itself out of a mate it has actually found.
            if scores[0][0] > AGC_MATE - 200:
                best_mv = scores[0][1]
            return best_mv

        # ---- input ----------------------------------------------------------

        def on_event(self, ev, x, y):
            try:
                import pygame_sdl2 as pg
            except Exception:
                return
            if ev.type == pg.MOUSEMOTION:
                self.hover = self.xy_sq(x, y)
                if self.drag is not None:
                    self.drag = (self.drag[0], x, y)
                return
            if self.state == AGChess.S_END:
                return

            if ev.type == pg.MOUSEBUTTONDOWN:
                button = getattr(ev, "button", 1)
                if button == 3:
                    self._cancel()
                    return
                if button != 1:
                    return
                if self.state == AGChess.S_PROMO:
                    self._promo_click(x, y)
                    return
                if self.state != AGChess.S_PLAY:
                    return
                sq = self.xy_sq(x, y)
                if sq < 0:
                    return
                self.cursor = sq
                if self.sel >= 0 and sq in self.targets:
                    self._try_move(sq)
                    return
                if self._select(sq):
                    self.drag = (sq, x, y)
                else:
                    self.sel = -1
                    self.targets = {}
                return

            if ev.type == pg.MOUSEBUTTONUP and getattr(ev, "button", 1) == 1:
                if self.drag is None:
                    return
                frm = self.drag[0]
                self.drag = None
                sq = self.xy_sq(x, y)
                # Released somewhere else: that was a drag. Released where it
                # started: that was a click, so the piece stays selected.
                if sq >= 0 and sq != frm and self.state == AGChess.S_PLAY:
                    if sq in self.targets:
                        self._try_move(sq)
                    else:
                        ag_se("deny", 0.35)

        def _cancel(self):
            if self.state == AGChess.S_PROMO:
                self.state = AGChess.S_PLAY
                self.promo = None
                ag_se("ui_no", 0.5)
                return
            if self.sel >= 0 or self.drag is not None:
                self.sel = -1
                self.targets = {}
                self.drag = None
                ag_se("ui_no", 0.4)

        def _promo_click(self, x, y):
            if not self.promo:
                return
            for i, (rect, mv) in enumerate(self._promo_boxes()):
                bx, by, bw, bh = rect
                if bx <= x < bx + bw and by <= y < by + bh:
                    self.promo = None
                    self.state = AGChess.S_PLAY
                    self._play(mv)
                    return

        def _promo_boxes(self):
            """The four choices, stacked into the board from the promotion
            square and folded back if that would run off the edge."""
            if not self.promo:
                return []
            _frm, to, opts = self.promo
            order = [AGC_QUEEN, AGC_ROOK, AGC_BISHOP, AGC_KNIGHT]
            by_type = {}
            for mv in opts:
                by_type[(mv >> 16) & 0xFF] = mv
            px, py = self.sq_xy(to)
            down = (to >> 4) == 7          # promoting at the top: grow downward
            out = []
            for i, t in enumerate(order):
                if t not in by_type:
                    continue
                oy = py + (i * AGC_CELL if down else -i * AGC_CELL)
                out.append(((px, oy, AGC_CELL, AGC_CELL), by_type[t]))
            return out

        def _read_keys(self, keys):
            if keys is None:
                return
            if self.state == AGChess.S_END:
                return
            moved = False
            f = self.cursor & 7
            r = self.cursor >> 4
            if self.tapped(keys, "left", AGC_K_LEFT1, AGC_K_LEFT2):
                f = max(0, f - 1)
                moved = True
            if self.tapped(keys, "right", AGC_K_RIGHT1, AGC_K_RIGHT2):
                f = min(7, f + 1)
                moved = True
            if self.tapped(keys, "up", AGC_K_UP1, AGC_K_UP2):
                r = min(7, r + 1)
                moved = True
            if self.tapped(keys, "down", AGC_K_DOWN1, AGC_K_DOWN2):
                r = max(0, r - 1)
                moved = True
            if moved:
                self.cursor = r * 16 + f
                self.hover = -1
                ag_se("ui_move", 0.25)

            ok = self.tapped(keys, "ok", AGC_K_OK1, AGC_K_OK2)
            cancel = self.tapped(keys, "no", AGC_K_NO1, AGC_K_NO2)
            if cancel:
                self._cancel()
                return
            if not ok:
                return
            if self.state == AGChess.S_PROMO:
                boxes = self._promo_boxes()
                for rect, mv in boxes:
                    if self.xy_sq(rect[0] + 2, rect[1] + 2) == self.cursor:
                        self.promo = None
                        self.state = AGChess.S_PLAY
                        self._play(mv)
                        return
                return
            if self.state != AGChess.S_PLAY:
                return
            if self.sel >= 0 and self.cursor in self.targets:
                self._try_move(self.cursor)
            elif not self._select(self.cursor):
                self.sel = -1
                self.targets = {}

        # ---- simulation -----------------------------------------------------

        def step(self):
            if self.result is not None:
                return
            keys = self.poll()

            if self.note_ticks > 0:
                self.note_ticks -= 1

            if self.state == AGChess.S_END:
                self.ending += 1
                if self.ending > 190:
                    self._end_run()
                return

            self._read_keys(keys)

            if self.anim is not None:
                self.anim[3] += 1
                if self.anim[3] > 11:
                    self.anim = None

            if self.state == AGChess.S_THINK:
                self.think_ticks += 1
                # One pump per RENDERED frame. AGStage may run several
                # simulation ticks to catch up after a hitch, and pumping the
                # search on each of them would spend a whole frame's budget
                # several times over and hitch again.
                if self._pumped != self.frame:
                    self._pumped = self.frame
                    self._pump()
                done = (self.search is None
                        and self.think_ticks >= self.lv["minthink"] * 60)
                if done:
                    if self.book_move:
                        mv = self.book_move
                        self.book_move = 0
                    else:
                        mv = self._choose()
                    if mv:
                        self._play(mv)
                    else:
                        self._terminal()
                return

            if self.state == AGChess.S_PLAY and self.lv["clock"]:
                self.clock -= 1
                if self.clock == 600:
                    ag_se("ui_no", 0.5)
                if self.clock <= 0:
                    self.clock = 0
                    self._finish_game(False, "TIME",
                                        "the floor moved on without you")

        def _end_run(self):
            if self.won is True:
                self.finish("win")
            elif self.won is False:
                self.finish("loss")
            else:
                self.finish("draw")

        # ---- drawing --------------------------------------------------------

        def draw(self, c):
            self.frame += 1
            self._draw_board(c)
            self._draw_pieces(c)
            if self.state == AGChess.S_PROMO:
                self._draw_promo(c)
            self._draw_hud(c)
            self._draw_panels(c)
            if self.state == AGChess.S_END:
                self._draw_end(c)

        def _draw_board(self, c):
            c.panel(AGC_BX - 16, AGC_BY - 16, AGC_BW + 32, AGC_BW + 32,
                    top="#161038ea", bottom="#0b0720f2", radius=16,
                    border=1.5, bcolor=(AGC_ACCENT + "55"))

            sel_targets = self.targets if self.state == AGChess.S_PLAY else {}
            check_sq = -1
            if self.bd.in_check():
                check_sq = self.bd.ksq[self.bd.stm]

            for sq in AGC_SQ64:
                px, py = self.sq_xy(sq)
                light = (((sq >> 4) + (sq & 7)) & 1) == 1
                col = AGC_LIGHT if light else AGC_DARK
                if sq == self.last[0] or sq == self.last[1]:
                    col = ag_mix(col, AGC_MARK, 0.42)
                if sq == self.sel:
                    col = ag_mix(col, AGC_SEL, 0.5)
                if sq == check_sq:
                    col = ag_mix(col, AGC_THREAT, 0.55)
                c.rect(col, px, py, AGC_CELL, AGC_CELL)

                # Coordinates live in the corners of the edge squares, inked
                # against the square they sit on rather than on a border rail.
                ink = "#0000004d" if light else "#ffffff40"
                if (sq >> 4) == 0:
                    c.text("abcdefgh"[sq & 7], px + AGC_CELL - 6,
                            py + AGC_CELL - 17, size=12, color=ink,
                            outline=None, anchor=(1.0, 0.0), bold=True)
                if (sq & 7) == 0:
                    c.text("12345678"[sq >> 4], px + 5, py + 3, size=12,
                            color=ink, outline=None, bold=True)

            # Where the selected piece may go: a dot on an empty square, a
            # ring on an occupied one, which is the reading every chess UI
            # uses. Both are toned to the square underneath them.
            for to in sel_targets:
                px, py = self.sq_xy(to)
                light = (((to >> 4) + (to & 7)) & 1) == 1
                mcol = AGC_MOVE_ON_LIGHT if light else AGC_MOVE_ON_DARK
                if self.bd.b[to] or ((self.bd.b[self.sel] & 7) == AGC_PAWN
                                    and to == self.bd.ep):
                    c.frame(mcol + "ee", px + 3, py + 3, AGC_CELL - 6,
                            AGC_CELL - 6, 4)
                else:
                    c.disp(("agcdot", mcol, 10),
                            lambda mcol=mcol: agc_disc(mcol, 10, 0.86),
                            px + AGC_CELL / 2.0, py + AGC_CELL / 2.0,
                            64, 64, anchor=(0.5, 0.5))

            if self.hover >= 0 and self.state == AGChess.S_PLAY:
                px, py = self.sq_xy(self.hover)
                c.frame("#ffffff33", px, py, AGC_CELL, AGC_CELL, 2)
            if self.hover < 0 and self.state == AGChess.S_PLAY:
                px, py = self.sq_xy(self.cursor)
                pulse = 0.55 + 0.45 * math.sin(self.tick * 0.16)
                c.frame("%s%02x" % (AGC_ACCENT, int(220 * pulse)),
                        px, py, AGC_CELL, AGC_CELL, 2)

        def _piece_at(self, c, code, px, py, zoom=None):
            """Drop a man onto the square, standing on its base rather than
            centred: a king and a pawn share a floor line, not a midpoint."""
            z = AGC_ZOOM if zoom is None else zoom
            w, h = agc_size(code, z)
            x = px + (AGC_CELL - w) / 2.0
            y = py + AGC_CELL - 6 - h
            c.disp(("agcsh", code, z), lambda: agc_piece_shadow(code, z),
                    x + 1, y + 3, 160, 160)
            c.disp(("agcp", code, z), lambda: agc_piece(code, z), x, y, 160, 160)

        def _draw_pieces(self, c):
            b = self.bd.b
            dragging = self.drag[0] if self.drag is not None else -1
            anim_to = self.anim[2] if self.anim is not None else -1
            for sq in AGC_SQ64:
                code = b[sq]
                if not code or sq == dragging or sq == anim_to:
                    continue
                px, py = self.sq_xy(sq)
                self._piece_at(c, code, px, py)

            # The opponent's move slides in, so a piece that appeared somewhere
            # while you were looking elsewhere is still legible after the fact.
            if self.anim is not None:
                code, frm, to, t = self.anim
                k = ag_clamp(t / 11.0, 0.0, 1.0)
                k = 1.0 - (1.0 - k) * (1.0 - k)
                fx, fy = self.sq_xy(frm)
                tx, ty = self.sq_xy(to)
                self._piece_at(c, code, fx + (tx - fx) * k,
                                fy + (ty - fy) * k)

            if self.drag is not None:
                code = b[self.drag[0]]
                if code:
                    w, h = agc_size(code)
                    self._piece_at(c, code, self.drag[1] - AGC_CELL / 2.0,
                                    self.drag[2] - AGC_CELL / 2.0)

        def _draw_promo(self, c):
            boxes = self._promo_boxes()
            if not boxes:
                return
            x0 = boxes[0][0][0]
            ys = [r[1] for r, _m in boxes]
            top = min(ys)
            c.rect("#0a0713aa", AGC_BX, AGC_BY, AGC_BW, AGC_BW)
            c.panel(x0 - 6, top - 6, AGC_CELL + 12,
                    AGC_CELL * len(boxes) + 12, top="#241b46f6",
                    bottom="#120c24fa", radius=12, border=1.5,
                    bcolor=(AGC_ACCENT + "cc"))
            for rect, mv in boxes:
                bx, by, _bw, _bh = rect
                c.rect("#ffffff10", bx, by, AGC_CELL, AGC_CELL)
                self._piece_at(c, ((mv >> 16) & 0xFF) | (self.human << 3),
                                bx, by)
            c.text("PROMOTE TO", x0 + AGC_CELL / 2.0, top - 26, size=12,
                    color=AGC_ACCENT, bold=True, kerning=2.0, anchor=(0.5, 0.0))

        # ---- HUD ------------------------------------------------------------

        def _material(self):
            """Your material edge in pawns, from the capture trays."""
            mine = sum(AGC_VALUE[p] for p in self.taken[self.human])
            theirs = sum(AGC_VALUE[p] for p in self.taken[self.human ^ 1])
            return (mine - theirs) // 100

        def _draw_hud(self, c):
            c.header("BOARD MEETING",
                        "MATSUCOM  //  %s" % self.lv["name"], AGC_ACCENT)
            edge = self._material()
            c.stat_row([
                ("SCORE", ag_num(self.score), AG_DIM),
                ("MOVE", str(len(self.history) // 2 + 1), AG_DIM),
                ("MATERIAL", ("+%d" % edge) if edge > 0 else str(edge),
                    ("#4fbf7a" if edge > 0 else
                    ("#e0455e" if edge < 0 else AG_INK))),
            ])

            # A caption under the board. Safe to anchor to the board here, and
            # only here: unlike the sweep's floors this board is the same size
            # at every difficulty, so nothing about it moves.
            cx = AGC_BX + AGC_BW / 2.0
            if self.note_ticks > 0 and self.state != AGChess.S_END:
                c.text(self.note, cx, AGC_BY + AGC_BW + 16, size=20,
                        color=AGC_MARK, font=AG_FONT, bold=True,
                        anchor=(0.5, 0.0))
            elif self.state == AGChess.S_THINK:
                dots = "." * (1 + (self.tick // 20) % 3)
                c.text("%s is thinking%s" % (self.lv["who"].lower(), dots),
                        cx, AGC_BY + AGC_BW + 18, size=15, color=AG_FAINT,
                        anchor=(0.5, 0.0))
            elif self.state == AGChess.S_PLAY:
                c.text("your move", cx, AGC_BY + AGC_BW + 18, size=15,
                        color=AG_FAINT, anchor=(0.5, 0.0))

            c.legend("CLICK OR DRAG TO MOVE   //   RIGHT CLICK CANCELS   "
                        "//   ESC PAUSE")

        def _plate(self, c, y, h, title):
            c.panel(AGC_PX, y, AGC_PW, h, top="#1b1440ea",
                    bottom="#0d0824f2", radius=14, border=1.0,
                    bcolor="#ffffff14")
            c.text(title, AGC_PX + 20, y + 14, size=12, color=AGC_ACCENT,
                    bold=True, kerning=3.0)

        def _draw_panels(self, c):
            self._plate(c, 110, 104, "ACROSS THE TABLE")
            c.text(self.lv["who"], AGC_PX + 20, 144, size=27, color=AG_INK,
                    font=AG_FONT, bold=True)
            c.text(self.lv["name"], AGC_PX + AGC_PW - 20, 150, size=13,
                    color=AGC_ACCENT, bold=True, kerning=2.0, anchor=(1.0, 0.0))

            if self.state == AGChess.S_THINK:
                frac = ag_clamp(self.compute / max(self.budget, 0.01), 0.0, 1.0)
                c.bar(AGC_PX + 20, 180, AGC_PW - 40, 6, frac, AGC_ACCENT)
                c.text("SEARCHING   DEPTH %d" % max(self.depth_shown, 1),
                        AGC_PX + 20, 192, size=11, color=AG_FAINT, kerning=1.5)
            else:
                c.rect("#ffffff10", AGC_PX + 20, 180, AGC_PW - 40, 6)
                c.text("WAITING ON YOU", AGC_PX + 20, 192, size=11,
                        color=AG_FAINT, kerning=1.5)

            if self.model is not None:
                self._draw_model(c)
            elif self.lv["clock"]:
                self._draw_clock(c)
            else:
                self._draw_assessment(c)

            self._draw_taken(c)
            self._draw_minutes(c)

        def _draw_clock(self, c):
            self._plate(c, 226, 88, "FLOOR TIME")
            left = self.clock / 60.0
            hot = self.clock <= 600 and self.state == AGChess.S_PLAY
            col = AGC_THREAT if hot else AG_INK
            if hot:
                pulse = 0.6 + 0.4 * math.sin(self.tick * 0.35)
                col = ag_mix("#5a2a3a", AGC_THREAT, pulse)
            c.text("%d:%02d" % (int(left) // 60, int(left) % 60),
                    AGC_PX + 20, 258, size=34, color=col, font=AG_FONT_UI,
                    bold=True)
            c.text("PER MOVE  %ds" % self.lv["clock"],
                    AGC_PX + AGC_PW - 20, 264, size=12, color=AG_FAINT,
                    kerning=1.5, anchor=(1.0, 0.0))
            c.bar(AGC_PX + 20, 296, AGC_PW - 40, 6,
                    self.clock / float(self.clock_max),
                    AGC_THREAT if hot else AGC_ACCENT)

        def _draw_assessment(self, c):
            """CASUAL only: the intern says what it thinks out loud. Cheap to
            show -- it is the number the engine already computed -- and it
            turns the easy opponent into a teaching one."""
            self._plate(c, 226, 88, "IT THINKS")
            if not self.edge_known:
                c.text("no opinion yet", AGC_PX + 20, 262, size=17,
                        color=AG_FAINT)
                return
            e = ag_clamp(self.edge / 100.0, -9.9, 9.9)
            if abs(e) < 0.4:
                word = "dead level"
                col = AG_INK
            elif e > 0:
                word = "you are better" if e < 2.5 else "you are winning"
                col = "#4fbf7a"
            else:
                word = "it is better" if e > -2.5 else "it is winning"
                col = "#e0455e"
            c.text(word, AGC_PX + 20, 260, size=22, color=col, font=AG_FONT,
                    bold=True)
            c.text("%+.1f" % e, AGC_PX + AGC_PW - 20, 262, size=22, color=col,
                    font=AG_FONT_UI, bold=True, anchor=(1.0, 0.0))
            # A bar centred on level, running your way to the right.
            bx = AGC_PX + 20
            bw = AGC_PW - 40
            c.rect("#ffffff10", bx, 296, bw, 6)
            half = bw / 2.0
            k = ag_clamp(e / 8.0, -1.0, 1.0) * half
            if k >= 0:
                c.rect("#4fbf7a", bx + half, 296, max(2, k), 6)
            else:
                c.rect("#e0455e", bx + half + k, 296, max(2, -k), 6)
            c.rect("#ffffff44", bx + half - 1, 293, 2, 12)

        def _draw_model(self, c):
            self._plate(c, 226, 88, "READ ON YOU")
            m = self.model
            c.text(m.tier(), AGC_PX + 20, 260, size=22, color=AG_INK,
                    font=AG_FONT, bold=True)
            c.text("%s  //  %s" % (m.style(), m.focus()),
                    AGC_PX + AGC_PW - 20, 264, size=13, color=AGC_ACCENT,
                    bold=True, kerning=1.5, anchor=(1.0, 0.0))
            c.bar(AGC_PX + 20, 296, AGC_PW - 40, 6, m.level, AGC_ACCENT)

        def _draw_taken(self, c):
            self._plate(c, 326, 92, "TABLED")
            edge = self._material()
            for row, side in ((0, self.human), (1, self.human ^ 1)):
                y = 358 + row * 28
                men = sorted(self.taken[side],
                                key=lambda p: -AGC_VALUE[p])[:14]
                x = AGC_PX + 20
                for code in men:
                    w, _h = agc_size(code, 0.62)
                    c.disp(("agcp", code, 0.62),
                            lambda code=code: agc_piece(code, 0.62),
                            x, y, 96, 96)
                    x += w * 0.72 + 2
                if not men:
                    c.text("--", AGC_PX + 20, y + 6, size=14, color=AG_FAINT)
            if edge:
                c.text(("+%d" % edge) if edge > 0 else str(edge),
                        AGC_PX + AGC_PW - 20, 360, size=22,
                        color=("#4fbf7a" if edge > 0 else "#e0455e"),
                        font=AG_FONT_UI, bold=True, anchor=(1.0, 0.0))

        def _draw_minutes(self, c):
            self._plate(c, 430, 230, "MINUTES")
            rows = 11
            pairs = []
            for i in range(0, len(self.history), 2):
                pairs.append((i // 2 + 1, self.history[i],
                                self.history[i + 1]
                                if i + 1 < len(self.history) else ""))
            shown = pairs[-rows:]
            y = 464
            if not shown:
                c.text("nothing minuted yet", AGC_PX + 20, y, size=14,
                        color=AG_FAINT)
                return
            for n, w, bl in shown:
                c.text("%2d." % n, AGC_PX + 22, y, size=14, color=AG_FAINT,
                        font=AG_FONT_UI)
                c.text(w, AGC_PX + 70, y, size=15, color=AG_INK,
                        font=AG_FONT_UI)
                if bl:
                    c.text(bl, AGC_PX + 190, y, size=15, color=AG_DIM,
                            font=AG_FONT_UI)
                y += 16
            # Second column for a long game, so the minutes never run out of
            # plate before the game runs out of moves.
            if len(pairs) > rows:
                older = pairs[max(0, len(pairs) - rows * 2):len(pairs) - rows]
                y = 464
                for n, w, bl in older:
                    c.text("%2d." % n, AGC_PX + 310, y, size=14,
                            color="#4c4470", font=AG_FONT_UI)
                    c.text(w, AGC_PX + 358, y, size=15, color="#8a82a8",
                            font=AG_FONT_UI)
                    if bl:
                        c.text(bl, AGC_PX + 470, y, size=15, color="#6f668c",
                                font=AG_FONT_UI)
                    y += 16

        def _draw_end(self, c):
            a = ag_clamp(self.ending / 30.0, 0.0, 1.0)
            if self.won is True:
                wash, col, head = "#04120c", "#4fbf7a", "MOTION CARRIED"
            elif self.won is False:
                wash, col, head = "#12040c", "#e0455e", "MOTION DENIED"
            else:
                wash, col, head = "#0a0a16", AGC_ACCENT, "ADJOURNED"
            c.rect(wash + "%02x" % int(150 * a), 0, 0, AG_W, AG_H)
            c.text(head, AG_W / 2, AG_H / 2 - 42, size=52, color=col,
                    font=AG_FONT, bold=True, anchor=(0.5, 0.5), alpha=a)
            c.text(self.note, AG_W / 2, AG_H / 2 + 8, size=22, color=AG_INK,
                    anchor=(0.5, 0.5), alpha=a)
            c.text(self.end_line, AG_W / 2, AG_H / 2 + 44, size=16,
                    color=AG_DIM, anchor=(0.5, 0.5), alpha=a)

        # ---- results --------------------------------------------------------

        def _score_run(self, kind):
            lv = self.lv
            mult = lv["mult"]
            if self.model is not None:
                # Adaptive is worth what it ended up being worth.
                mult = 1.0 + 2.6 * self.model.level
            if kind == "win":
                base = 1200
            elif kind == "draw":
                base = 420
            elif kind == "quit":
                base = 0
            else:
                base = 90
            edge = self._material()
            bonus = max(0, edge) * 25
            # A short win is a cleaner win.
            if kind == "win":
                bonus += max(0, 60 - self.moves_played) * 8
            return int(round((base + bonus) * mult))

        def finish(self, kind):
            self.score = self._score_run(kind)
            super(AGChess, self).finish(kind)

        def record(self):
            if self.score:
                self.new_record = ag_set_best("chess_score", self.score)
                ag_set_best("chess_score_" + self.level_id, self.score)
            if self.won is True:
                ag_set_best("chess_win_" + self.level_id, 1)

        def outcome(self, kind):
            if kind == "quit":
                return "RESIGNED"
            if kind == "win":
                return "MOTION CARRIED"
            if kind == "draw":
                return "ADJOURNED"
            if self.end_head == "TIME":
                return "TIME FORFEIT"
            return "MOTION DENIED"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            if kind == "win":
                return "#4fbf7a"
            if kind == "draw":
                return AGC_ACCENT
            return "#e0455e"

        def rows(self, kind):
            out = [("OPPONENT", self.lv["who"]),
                    ("RESULT", self.end_head or "-"),
                    ("MOVES", str(len(self.history) // 2 + (
                        1 if len(self.history) % 2 else 0))),
                    ("MATERIAL", "%+d" % self._material()),
                    ("SCORE", ag_num(self.score))]
            if self.model is not None:
                out.insert(1, ("IT SETTLED AT", self.model.tier()))
            best = ag_best("chess_score_" + self.level_id)
            if best:
                out.append(("BEST HERE", ag_num(max(best, self.score))))
            return out


    # Key codes, resolved once. Same shape as the sweep's block: a machine with
    # no pygame_sdl2 gets -1s and simply has no keyboard controls rather than
    # failing to import the cabinet at all.
    try:
        import pygame_sdl2 as _agc_pg
        AGC_K_LEFT1, AGC_K_LEFT2 = _agc_pg.K_LEFT, _agc_pg.K_a
        AGC_K_RIGHT1, AGC_K_RIGHT2 = _agc_pg.K_RIGHT, _agc_pg.K_d
        AGC_K_UP1, AGC_K_UP2 = _agc_pg.K_UP, _agc_pg.K_w
        AGC_K_DOWN1, AGC_K_DOWN2 = _agc_pg.K_DOWN, _agc_pg.K_s
        AGC_K_OK1, AGC_K_OK2 = _agc_pg.K_z, _agc_pg.K_RETURN
        AGC_K_NO1, AGC_K_NO2 = _agc_pg.K_x, _agc_pg.K_BACKSPACE
    except Exception:
        AGC_K_LEFT1 = AGC_K_LEFT2 = AGC_K_RIGHT1 = AGC_K_RIGHT2 = -1
        AGC_K_UP1 = AGC_K_UP2 = AGC_K_DOWN1 = AGC_K_DOWN2 = -1
        AGC_K_OK1 = AGC_K_OK2 = AGC_K_NO1 = AGC_K_NO2 = -1


    def ag_chess_cover():
        """Box art: a corner of the board with the two kings and a knight,
        drawn from the same sheet the cabinet plays with -- including the
        sheet's own reflection frames, which is what the bottom row is for."""
        parts = ag_cover_base(AGC_ACCENT)
        cell = 62
        ox, oy = 16, 18
        for r in range(3):
            for f in range(5):
                light = ((r + f) & 1) == 1
                parts.append(Transform(
                    Solid(AGC_LIGHT if light else AGC_DARK,
                            xysize=(cell, cell)),
                    pos=(ox + f * cell, oy + r * cell)))
        men = [(AGC_BK, 1, 0), (AGC_WN, 3, 1), (AGC_WK, 2, 2)]
        for code, f, r in men:
            x, y, w, h = AGC_SRC[code]
            z = 1.55
            px = ox + f * cell + (cell - w * z) / 2.0
            py = oy + r * cell + cell - 6 - h * z
            parts.append(Transform(
                Transform(AGC_SHEET, crop=(x, y, w, h)), zoom=z,
                matrixcolor=TintMatrix("#000000"), alpha=0.4,
                pos=(px + 2, py + 4)))
            parts.append(Transform(Transform(AGC_SHEET, crop=(x, y, w, h)),
                                    zoom=z, pos=(px, py)))
            ref = AGC_SRC_REF.get(code)
            if ref:
                parts.append(Transform(
                    Transform(AGC_SHEET, crop=ref), zoom=z, alpha=0.30,
                    pos=(px, py + h * z)))
        parts += ag_cover_title("FOUR OPPONENTS", "BOARD MEETING", AGC_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "chess", AGChess,
        title="Board Meeting",
        accent=AGC_ACCENT,
        blurb="Chess against four people who all want this over with. Pick "
                "the one you deserve: an intern who thinks out loud, a "
                "professional on a clock, a grandmaster on the same clock, or a "
                "model that reads you while you play and forgets you when you "
                "leave.",
        controls=AGChess.CONTROLS,
        music=audio.quiz,
        cover=ag_chess_cover,
        variant_prompt="Pick your opponent.",
        variants=[(vid, AGC_LEVELS[vid]["name"], AGC_LEVELS[vid]["note"])
                    for vid in AGC_ORDER],
    )
