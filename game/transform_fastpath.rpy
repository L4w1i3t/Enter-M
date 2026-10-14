# =============================================================================
# TRANSFORM FAST PATH -- the engine's transform state copy, minus the walk
# =============================================================================
# Every shader uniform any file registers becomes a transform PROPERTY, and
# this project registers a lot of them: 534 properties, 467 of them uniforms
# (measured Oct 9 2026). Two engine methods walk ALL of them on every call:
#
#   TransformState.take_state   -- copies every property, one getattr each.
#   TransformState.diff         -- compares every property, two getattrs each.
#
# They run whenever a transform is replaced or an ATL block (re)starts, which
# in a fight means every strike: ~35 new transforms in one frame. Profiled in
# Matsuda's fight, take_state cost 113us a call and diff 154us, and a strike
# frame spent ~9ms in them -- the hitch the player sees on every hit.
#
# THE FAST PATH IS THE SAME COMPUTATION. A property can only differ from the
# class default where one of the two states' instance dicts holds it; every
# other property reads the class attribute on both sides, so copying it
# re-stores the default and comparing it compares the default to itself. So:
#   take_state copies only keys present in either dict (the rest still read
#     the class default, exactly as the copied values would have);
#   diff walks the SAME property set in the SAME order -- so its result dict
#     comes out in the same order -- but skips a key both dicts lack before
#     doing two getattrs. The four diff4 (position) properties, which fall
#     back to inherited values, keep the original full treatment.
# Every other line of both methods is the engine's, verbatim.
#
# IT INSTALLS ONLY OVER THE ENGINE CODE IT WAS WRITTEN AGAINST. The two
# originals' bytecode is fingerprinted (Matsu'Py 8.6.0, Python 3.12) and if
# either has changed, nothing is patched and the engine's own methods run --
# a newer engine may have fixed this differently, or changed what the methods
# must do. It was verified by running both versions side by side on every real
# call through Matsuda's fight and the opening of Chapter 0.5 (see
# docs/history/2026-10-09-stress-test-and-low-detail.md);
# TRANSFORM_FASTPATH_SHADOW below re-arms that check.
# =============================================================================

init -999 python:

    import hashlib as _tfp_hashlib

    TRANSFORM_FASTPATH_FINGERPRINTS = {
        "take_state": "6e60cd36647370591880304a72cdb4952b42d3d6",
        "diff": "2f03ba3db92512d5e6bd0160160ae3766742be05",
    }

    # Developer check: run the original next to the fast path on every call
    # and record any disagreement in TRANSFORM_FASTPATH_MISMATCHES. Slow; for
    # verification only.
    TRANSFORM_FASTPATH_SHADOW = False
    TRANSFORM_FASTPATH_MISMATCHES = []
    TRANSFORM_FASTPATH_CHECKED = [0, 0]     # take_state, diff calls compared
    TRANSFORM_FASTPATH_ACTIVE = False

    def _tfp_install():
        import renpy.display.transform as T

        TS = T.TransformState

        # A script reload re-runs this block over an already-patched class.
        if getattr(TS.take_state, "_em_fast", False):
            return True

        for name, want in TRANSFORM_FASTPATH_FINGERPRINTS.items():
            code = getattr(TS, name).__code__.co_code
            if _tfp_hashlib.sha1(code).hexdigest() != want:
                return False

        orig_take_state = TS.take_state
        orig_diff = TS.diff

        def take_state(self, ts):
            d = self.__dict__
            td = ts.__dict__
            ap = T.all_properties

            # Keys this state holds that ts does not: they take ts's value,
            # which is the class default (or a texture uniform's None).
            for k in [k for k in d if k in ap and k not in td]:
                d[k] = getattr(ts, k)

            # Keys ts holds. getattr(ts, k) is td[k] for every property kind,
            # texture uniforms included (their descriptor reads the dict).
            for k, v in td.items():
                if k in ap:
                    d[k] = v

            # --- verbatim from the engine below this line ---
            self.last_angle = ts.last_angle
            self.radius_sign = ts.radius_sign
            self.relative_anchor_radius_sign = ts.relative_anchor_radius_sign
            self.absolute_anchor_radius_sign = ts.absolute_anchor_radius_sign
            self.last_absolute_anchorangle = ts.last_absolute_anchorangle
            self.last_relative_anchorangle = ts.last_relative_anchorangle
            self.last_events = ts.last_events

            self.available_width = ts.available_width
            self.available_height = ts.available_height

            if self.perspective is None:
                self.xpos = None
                self.ypos = None
                self.xanchor = None
                self.yanchor = None

            (self.inherited_xpos, self.inherited_ypos, self.inherited_xanchor,
                self.inherited_yanchor, _tfp_a, _tfp_b, _tfp_c) = ts.get_placement()

            self.xoffset = ts.xoffset
            self.yoffset = ts.yoffset
            self.subpixel = ts.subpixel

        def diff(self, newts):
            rv = {}
            sd = self.__dict__
            nd = newts.__dict__

            for prop in T.diff2_properties:
                if prop not in sd and prop not in nd:
                    continue

                new = getattr(newts, prop)
                old = getattr(self, prop)

                if new != old:
                    rv[prop] = (old, new)

            # --- verbatim from the engine below this line ---
            for prop in T.diff4_properties:
                new = getattr(newts, prop)
                old = getattr(self, prop)

                if new is None:
                    new = getattr(newts, "inherited_" + prop)
                if old is None:
                    old = getattr(self, "inherited_" + prop)

                if new != old:
                    rv[prop] = (old, new)

            return rv

        def _same(a, b):
            if a is b:
                return True
            try:
                return bool(a == b)
            except Exception:
                return False

        def take_state_shadow(self, ts):
            ref = TS.__new__(TS)
            ref.__dict__.update(self.__dict__)
            orig_take_state(ref, ts)
            take_state(self, ts)
            TRANSFORM_FASTPATH_CHECKED[0] += 1
            if len(TRANSFORM_FASTPATH_MISMATCHES) < 200:
                for k in T.all_properties:
                    if not _same(getattr(ref, k), getattr(self, k)):
                        TRANSFORM_FASTPATH_MISMATCHES.append(("take_state", k))
                for k in ("inherited_xpos", "inherited_ypos", "inherited_xanchor",
                          "inherited_yanchor", "xoffset", "yoffset", "subpixel",
                          "last_angle", "available_width", "available_height"):
                    if not _same(getattr(ref, k, None), getattr(self, k, None)):
                        TRANSFORM_FASTPATH_MISMATCHES.append(("take_state", k))

        def diff_shadow(self, newts):
            a = orig_diff(self, newts)
            b = diff(self, newts)
            TRANSFORM_FASTPATH_CHECKED[1] += 1
            if len(TRANSFORM_FASTPATH_MISMATCHES) < 200:
                if list(a.keys()) != list(b.keys()):
                    TRANSFORM_FASTPATH_MISMATCHES.append(("diff-keys", sorted(set(a) ^ set(b))[:6]))
                else:
                    for k in a:
                        if not (_same(a[k][0], b[k][0]) and _same(a[k][1], b[k][1])):
                            TRANSFORM_FASTPATH_MISMATCHES.append(("diff-value", k))
            return a

        # A reload keeps this patch on the class but empties the store, and
        # init -1400 engine code calls it before this block redefines the flag.
        def take_state_entry(self, ts):
            if globals().get("TRANSFORM_FASTPATH_SHADOW"):
                return take_state_shadow(self, ts)
            return take_state(self, ts)

        def diff_entry(self, newts):
            if globals().get("TRANSFORM_FASTPATH_SHADOW"):
                return diff_shadow(self, newts)
            return diff(self, newts)

        take_state_entry._em_fast = True
        take_state_entry._em_orig = orig_take_state
        diff_entry._em_fast = True
        diff_entry._em_orig = orig_diff

        TS.take_state = take_state_entry
        TS.diff = diff_entry
        return True

    TRANSFORM_FASTPATH_ACTIVE = _tfp_install()
