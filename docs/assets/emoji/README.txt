Phone emoji — source checked 2026-09-25

The phone renders installed emoji as inline PNGs. Implementation:
game/addons/Phone System/phone_model_construct.rpy (scan and text rewriting),
plus text.rpy (message bubbles and the thumbs-up fallback).

1. Put the PNG in game/assets/emoji/.
2. Name it with lowercase Unicode codepoints joined by hyphens, omitting FE0F:
   thumbs up: 1f44d.png; red heart: 2764.png; fire: 1f525.png;
   thumbs up with skin tone: 1f44d-1f3fd.png.
3. Use the literal emoji in a phone_msg body. phone_emojify replaces only
   clusters whose PNG was registered; missing art remains literal text and its
   appearance depends on the selected font. Contacts-list previews strip emoji.

PHONE_EMOJI_PX currently sets 24px inline images. The thumbs-up reaction uses
1f44d.png when loadable, otherwise the Phone System's UI glyph. The init scan
also runs during script reload; add assets before launching/reloading so text
caches and the registered image table agree.

Retain the source pack's license and attribution. A compatible filename does
not establish permission to redistribute the artwork.
