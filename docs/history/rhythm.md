# Asarhythm revisions, September 2026

Historical summary consolidated September 25. The
[current mode guide](../minigames/README.md) identifies the runtime sources.

- September 11: initial rhythm-mode/Arcade integration, chart editor, story-act
  flow, additional song work, and FNF-style presentation polish.
- September 12: concert-art production, redraw experiments, stage/icon work,
  chart editing tools, and several baseline/runtime QA passes. These records
  include intermediate visual approaches; they are not an instruction to
  replace the installed original whole-body singers.
- September 13–14: song selection, modifiers, stage effects, ending sequences,
  and wipes. Source owns the actual record/reward and practice/autoplay rules.
- September 16: song-select chrome/autoplay, original-art polish, Matsuda
  repairs, repeat-note triggering, then the explicit two-beat idle correction.
  The two-beat correction supersedes earlier beat-cadence descriptions.

Current `asahina_rhythm_motion.SingerFrames` samples idle against the supplied
song beat over a two-beat cycle. A changed note event restarts a sung gesture,
including repeated arrows; ticks of the same sustain keep the event. The
module's stance offsets register whole drawings without regenerating their
anatomy or resizing each pose independently.

The old task reports' test counts and frame captures belong to their original
run. Dummy-audio GL2 captures do not establish audible sync, human input feel,
normal-speed continuous playback, or a packaged build. Original prompts and
art retained elsewhere remain provenance. Missing historical build inputs are
not recreated from a report's assertion that they once existed.
