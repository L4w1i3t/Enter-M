PHONE EMOJI  --  drop-in color emoji for the in-story phone
============================================================

Matsu'Py 8.1.1 cannot render color-emoji FONTS, so the phone renders emoji as
small PNG images instead. To add an emoji:

1. Drop a PNG in game/assets/emoji/.
2. Name it by the emoji's Unicode codepoint(s), lowercase hex, joined by "-".
   This is the Twemoji filename convention, so Twemoji/OpenMoji asset packs
   work as-is.

       👍   thumbs up            -> 1f44d.png
       😂   tears of joy         -> 1f602.png
       ❤    red heart            -> 2764.png      (drop the FE0F selector)
       🔥   fire                 -> 1f525.png
       👍🏽  thumbs up + skin tone -> 1f44d-1f3fd.png
       👨‍👩‍👧 family (ZWJ sequence) -> 1f468-200d-1f469-200d-1f467.png

   Tip: Twemoji's published PNGs are already named this way -- grab the ones you
   need from https://github.com/jdecked/twemoji (72x72 PNG/ folder) or any
   CC-licensed emoji set and drop them in.

3. In a story script, just type the literal emoji in the message text:

       $ _msgs = [ phone_msg("them", "nice work 👍🔥") ]
       call phone_text_conversation("Monika", _msgs, append=True)

   phone_emojify() automatically swaps each emoji that has a PNG in that asset
   folder for the image. Emoji with no PNG yet stay as plain text (so you'll see a missing-glyph
   box -- that's your cue to add the PNG). The 👍 thumbs-up reaction
   (phone_thumb(...)) uses 1f44d.png when present, else its hand-drawn fallback.

Notes
-----
- Images are auto-discovered on launch AND on hot-reload, so dropping a new PNG
  while the game runs makes it appear without a full restart.
- Inline emoji are scaled to PHONE_EMOJI_PX (24 px) in message bubbles; the
  thumbs-up reaction renders a bit larger. Source PNGs of ~72 px look crispest.
- This folder only needs the emoji you actually use in scripts -- not the whole
  set.
