# =============================================================================
# misc_variables.rpy  --  all Mika lost-record definitions in one place
#
# WHAT THIS FILE IS
#   Every sprite, character, background, BGM and SFX alias the Mika record needs.
#   It is the record's local equivalent of mod_assets/def_*.rpy: nothing here is
#   used outside game/lost_records/Mika.
#
#   Everything is namespaced `mika_` (or `monikayoung`) so the record can define
#   its own park, house, bells and music without colliding with ENTER M's.
#
# CONTENTS, IN ORDER
#   1. monikayoung sprites  -- im.Composite kid-Monika poses (KidMonika/)
#   2. mm                   -- the "Mika" speaker, with her own Sayori textbox
#   3. mika_splash_warning  -- ParameterizedText used by the credits card
#   4. audio.mika_*         -- BGM and SFX aliases (mod_assets/bgm, mod_assets/sfx)
#   5. mika_bg_*            -- backgrounds (mod_assets/bg)
#
# RELATED FILES
#   mod_assets/MPT/*_layeredimage.rpy  -- the Monika Pose Toolkit sprite defs
#   ch_mika.rpy / ch_mika_rewrite.rpy  -- the two tellings of the record
# =============================================================================
# char definitions

image monikayoung 1a = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/a.png")
image monikayoung 1b = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/b.png")
image monikayoung 1c = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/c.png")
image monikayoung 1d = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/d.png")
image monikayoung 1e = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/e.png")
image monikayoung 1f = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/f.png")
image monikayoung 1g = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/g.png")
image monikayoung 1h = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/h.png")
image monikayoung 1i = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/i.png")
image monikayoung 1j = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/j.png")
image monikayoung 1k = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/k.png")
image monikayoung 1l = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/l.png")
image monikayoung 1m = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/m.png")
image monikayoung 1n = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/n.png")
image monikayoung 1o = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/o.png")
image monikayoung 1p = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/p.png")
image monikayoung 1q = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/q.png")
image monikayoung 1r = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/r.png")

image monikayoung 2a = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/a.png")
image monikayoung 2b = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/b.png")
image monikayoung 2c = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/c.png")
image monikayoung 2d = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/d.png")
image monikayoung 2e = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/e.png")
image monikayoung 2f = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/f.png")
image monikayoung 2g = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/g.png")
image monikayoung 2h = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/h.png")
image monikayoung 2i = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/i.png")
image monikayoung 2j = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/j.png")
image monikayoung 2k = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/k.png")
image monikayoung 2l = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/l.png")
image monikayoung 2m = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/m.png")
image monikayoung 2n = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/n.png")
image monikayoung 2o = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/o.png")
image monikayoung 2p = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/p.png")
image monikayoung 2q = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/q.png")
image monikayoung 2r = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/r.png")

image monikayoung 3a = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/a.png")
image monikayoung 3b = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/b.png")
image monikayoung 3c = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/c.png")
image monikayoung 3d = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/d.png")
image monikayoung 3e = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/e.png")
image monikayoung 3f = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/f.png")
image monikayoung 3g = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/g.png")
image monikayoung 3h = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/h.png")
image monikayoung 3i = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/i.png")
image monikayoung 3j = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/j.png")
image monikayoung 3k = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/k.png")
image monikayoung 3l = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/l.png")
image monikayoung 3m = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/m.png")
image monikayoung 3n = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/n.png")
image monikayoung 3o = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/o.png")
image monikayoung 3p = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/p.png")
image monikayoung 3q = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/q.png")
image monikayoung 3r = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/1l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/2r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/r.png")

image monikayoung 4a = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/a.png")
image monikayoung 4b = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/b.png")
image monikayoung 4c = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/c.png")
image monikayoung 4d = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/d.png")
image monikayoung 4e = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/e.png")
image monikayoung 4f = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/f.png")
image monikayoung 4g = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/g.png")
image monikayoung 4h = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/h.png")
image monikayoung 4i = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/i.png")
image monikayoung 4j = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/j.png")
image monikayoung 4k = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/k.png")
image monikayoung 4l = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/l.png")
image monikayoung 4m = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/m.png")
image monikayoung 4n = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/n.png")
image monikayoung 4o = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/o.png")
image monikayoung 4p = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/p.png")
image monikayoung 4q = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/q.png")
image monikayoung 4r = im.Composite((960, 960), (0, 0), "lost_records/Mika/mod_assets/KidMonika/2l.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/1r.png", (0, 0), "lost_records/Mika/mod_assets/KidMonika/r.png")

define mm = DynamicCharacter('m_name2', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", window_background=Image("lost_records/Mika/mod_assets/gui/textbox_sayori.png", xalign=0.5, yalign=1.0), who_outlines=[ (3, "#686362") ])
default m_name2 = "Mika"

image mika_splash_warning = ParameterizedText(xalign=0.5, yalign=0.5)


# custom bgm
define -50 audio.mika_a2 = "<loop 16.444>lost_records/Mika/mod_assets/bgm/a2.ogg"
define -50 audio.mika_away = "<loop 7.982>lost_records/Mika/mod_assets/bgm/away.ogg"
define -50 audio.mika_ye = "lost_records/Mika/mod_assets/bgm/ye.ogg"


# custom sfx
define -50 audio.mika_footsteps = "lost_records/Mika/mod_assets/sfx/footsteps.ogg"
define -50 audio.mika_night = "lost_records/Mika/mod_assets/sfx/night.ogg"
define -50 audio.mika_bell = "lost_records/Mika/mod_assets/sfx/schoolbell.ogg"
define -50 audio.mika_laugh = "lost_records/Mika/mod_assets/sfx/laugh.ogg"
define -50 audio.mika_pound = "<from 0.69>sfx/monikapound.ogg"


# custom bg
image mika_bg_park = "lost_records/Mika/mod_assets/bg/park.png"
image mika_bg_parknight = "lost_records/Mika/mod_assets/bg/parknight.png"
image mika_bg_house = "lost_records/Mika/mod_assets/bg/house.png"
image mika_bg_stairs = "lost_records/Mika/mod_assets/bg/stairs.png"
