# =============================================================================
# cs_tsubaki_gothic.rpy  --  SHARED GOTHIC PROSE ENGINE for "Heads" / "Tails"
# =============================================================================
#
# WHAT THIS IS
#   The presentation layer shared by Tsubaki's two side stories, which are the
#   same story told from either face of one coin:
#     cs_tsubaki_01.rpy  "Heads" -- the mender's manuscript (warm parchment)
#     cs_tsubaki_02.rpy  "Tails" -- the mended one's testimony (cold dark)
#   Architecture is deliberately parallel to the Nier text-adventure format
#   (addons/Nier Forest Text Adventure Format/nier_text_adventure.rpy): an
#   NVL-kind narrator rendered into a custom accumulating-prose screen, with
#   section title cards and inline choice menus. It is a separate engine
#   because the whole point of this pair is a themed INVERSE presentation:
#   one screen, two faces, switched by `tsg_theme`.
#
# USAGE (from the two story files)
#   call tsg_enter("heads")            -- or "tails"; saves+kills quick_menu
#   tsg "Prose."                       -- Heads narrator (ink on paper)
#   tsgt "Prose."                      -- Tails narrator (bone on dark);
#                                         each face MUST use its own narrator
#   call tsg_section("I. Title")       -- clear + themed title card
#   call tsg_clear                     -- new "page" without leaving the mode
#   $ tsg_set_mood(0.4)                -- 0..1; Heads: fever (scorch), Tails:
#                                         calm (warmth). Change ONLY around a
#                                         section card / clear: the backdrop is
#                                         swapped, which restarts shader time.
#   menu (screen="tsg_choice"): ...    -- themed inline choice
#   call tsg_exit                      -- restore quick_menu, fade out
#
# SHADERS (guarded like Purgatorium's; stories fall back to flat Solids)
#   enter_m.tsg_page  : "Heads" backdrop. Procedural ivory paper (fibre +
#       tonal blotch), a breathing candle vignette, and dust motes that RISE
#       through the light. u_fever 0..1 scorches the page from the edges and
#       turns the rising motes into FALLING soot -- the ending of "Heads"
#       visually quotes "Tails".
#   enter_m.tsg_umbra : "Tails" backdrop. Near-black with a cold breathing
#       glow, a systolic double-thump pulse that SKIPS every fifth beat (her
#       missing heartbeat), and ash that FALLS. u_calm 0..1 relaxes the pulse
#       and lets candle-warmth in -- the ending of "Tails" quotes "Heads".
#   Both are OPAQUE full-screen fragments hosted on a Solid with mesh True
#   (see the calendar-dial gotcha: shader-on-Solid needs mesh + opaque base).
#   u_time / u_model_size are supplied by Matsu'Py's model renderer.
# =============================================================================

# Mode state. tsg_theme picks the face; tsg_mood drives the theme shader's
# progress uniform (fever for heads, calm for tails).
default tsg_active = False
default tsg_prev_quick_menu = True
default tsg_theme = "heads"
default tsg_mood = 0.0

# One narrator PER FACE. NVL applies the character's what_style to the text
# by id, which REPLACES whatever style the screen picks -- so a single shared
# narrator would bleed one theme's ink into the other (Tails once rendered in
# Heads' #2c2217 ink because of exactly this). Character style and screen
# style must always agree per theme, like the Nier engine keeps them.
define tsg = Character(
    None,
    kind=nvl,
    screen="tsg_nvl",
    what_style="tsg_prose_heads",
    window_style="tsg_entry",
)
define tsgt = Character(
    None,
    kind=nvl,
    screen="tsg_nvl",
    what_style="tsg_prose_tails",
    window_style="tsg_entry",
)

# (No local audio aliases: the four cues these stories play -- vinyl, wind,
# hollowboom, heartbeat -- already have project aliases in def_audio.rpy.)

# =============================================================================
#  SHADERS
# =============================================================================
init -10 python:
    def _tsg_register_shaders():
        # ---- "Heads": candlelit manuscript page -----------------------------
        renpy.register_shader("enter_m.tsg_page", variables="""
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform float u_fever;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float tsg_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float tsg_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                float a = tsg_hash(i);
                float b = tsg_hash(i + vec2(1.0, 0.0));
                float c = tsg_hash(i + vec2(0.0, 1.0));
                float d = tsg_hash(i + vec2(1.0, 1.0));
                vec2 u = f * f * (3.0 - 2.0 * f);
                return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
            }
            /* One layer of drifting flecks. dir=+1 rises, -1 falls. */
            float tsg_flecks(vec2 uv, float t, float scale, float speed, float dir, float seed) {
                vec2 g = uv * vec2(26.0, 15.0) * scale;
                g.y += t * speed * dir;
                vec2 cell = floor(g);
                float h = tsg_hash(cell + seed);
                vec2 pos = vec2(tsg_hash(cell + seed + 7.1), tsg_hash(cell + seed + 13.7));
                pos = 0.15 + 0.7 * pos;
                float pt = 1.0 - smoothstep(0.02, 0.10, length(fract(g) - pos));
                float on = step(0.94, h);
                float tw = 0.5 + 0.5 * sin(t * (1.0 + h * 2.5) + h * 17.0);
                return pt * on * tw;
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 c = uv - vec2(0.5, 0.46);

            // Aged paper: fine fibre grain + broad tonal blotching.
            float fib = tsg_noise(uv * vec2(190.0, 95.0));
            float blotch = tsg_noise(uv * 6.0);
            vec3 paper = vec3(0.938, 0.895, 0.795);
            paper -= fib * 0.035 + blotch * 0.055;

            // Candle breath: irregular flicker of both reach and brightness.
            float fl = 0.88
                + 0.055 * sin(u_time * 7.3) * sin(u_time * 3.1 + 1.7)
                + 0.045 * (tsg_hash(vec2(floor(u_time * 11.0), 3.7)) - 0.5);
            float d = length(c * vec2(1.28, 1.0));
            float light = smoothstep(0.98 * fl, 0.16 * fl, d);
            vec3 lit = mix(paper * vec3(0.50, 0.41, 0.32), paper * vec3(1.04, 1.0, 0.94), light);

            // Fever: scorch bleeds in from the edges, then eats the page.
            vec3 scorch = vec3(0.30, 0.19, 0.12);
            float edge = smoothstep(0.26, 0.72, d);
            float burn = clamp(edge * u_fever * 1.5 + u_fever * 0.30, 0.0, 1.0);
            lit = mix(lit, scorch * (0.35 + 0.55 * light), burn);

            // Motes rise while the account is calm; as the fever takes hold
            // they become soot and fall (the other story's weather).
            float dir = 1.0 - 2.0 * smoothstep(0.35, 0.75, u_fever);
            float m = tsg_flecks(uv, u_time, 1.0, 0.55, dir, 0.0)
                    + tsg_flecks(uv, u_time, 1.7, 0.90, dir, 31.0);
            vec3 moteCol = mix(vec3(1.0, 0.97, 0.85), vec3(0.09, 0.055, 0.035), u_fever);
            lit = mix(lit, moteCol, clamp(m * (0.22 + 0.40 * light), 0.0, 1.0));

            gl_FragColor = vec4(lit, 1.0);
        """)

        # ---- "Tails": the dark with a skipped heartbeat ----------------------
        renpy.register_shader("enter_m.tsg_umbra", variables="""
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform float u_calm;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float tsg_uhash(vec2 p) {
                return fract(sin(dot(p, vec2(269.5, 183.3))) * 43758.5453);
            }
            float tsg_uflecks(vec2 uv, float t, float scale, float speed, float dir, float seed) {
                vec2 g = uv * vec2(26.0, 15.0) * scale;
                g.y += t * speed * dir;
                vec2 cell = floor(g);
                float h = tsg_uhash(cell + seed);
                vec2 pos = vec2(tsg_uhash(cell + seed + 7.1), tsg_uhash(cell + seed + 13.7));
                pos = 0.15 + 0.7 * pos;
                float pt = 1.0 - smoothstep(0.02, 0.10, length(fract(g) - pos));
                float on = step(0.95, h);
                float tw = 0.5 + 0.5 * sin(t * (0.8 + h * 2.0) + h * 23.0);
                return pt * on * tw;
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 c = uv - vec2(0.5, 0.52);
            float d = length(c * vec2(1.25, 1.0));

            // Systolic double thump, ~57 bpm... except every fifth beat is
            // simply not there. That absence is the story.
            float rate = mix(1.05, 1.45, u_calm);
            float beatIdx = floor(u_time / rate);
            float tb = fract(u_time / rate);
            float skipped = step(3.999, mod(beatIdx, 5.0));
            float thump = exp(-tb * 11.0)
                        + 0.55 * exp(-max(tb - 0.30, 0.0) * 15.0) * step(0.30, tb);
            float pulse = clamp(thump, 0.0, 1.3) * (1.0 - skipped) * (1.0 - 0.75 * u_calm);

            // Cold breathing glow that contracts on each thump; calm lets a
            // candle-warm tint in from the centre (the other story's light).
            float r = 0.60 - 0.09 * pulse;
            float glow = smoothstep(r + 0.38, r - 0.24, d);
            vec3 base = vec3(0.010, 0.012, 0.018);
            vec3 tint = mix(vec3(0.085, 0.115, 0.165), vec3(0.235, 0.150, 0.080), u_calm);
            vec3 col = base + tint * glow * (0.55 + 0.35 * pulse);

            // A bruise of red low in the frame on the beat.
            col.r += 0.085 * pulse * smoothstep(0.55, 0.0, d);

            // Ash falls; calm slows it and lends it ember warmth.
            float fall = 1.0 - 0.65 * u_calm;
            float a = tsg_uflecks(uv, u_time, 1.0, 0.40 * fall, -1.0, 0.0)
                    + tsg_uflecks(uv, u_time, 1.8, 0.70 * fall, -1.0, 53.0);
            vec3 ashCol = mix(vec3(0.42, 0.47, 0.55), vec3(0.80, 0.62, 0.38), u_calm);
            col = mix(col, ashCol, clamp(a * (0.16 + 0.22 * glow), 0.0, 1.0));

            gl_FragColor = vec4(col, 1.0);
        """)

    try:
        _tsg_register_shaders()
        TSG_SHADERS = True
    except Exception as e:
        TSG_SHADERS = False
        if config.developer:
            renpy.log("TSUBAKI GOTHIC: shader registration failed: %r" % e)

    def tsg_set_mood(v):
        """Set the theme shader's progress uniform (heads: fever, tails: calm).
        Swap it around a section card or clear -- the backdrop displayable is
        replaced, so shader time restarts."""
        global tsg_mood
        tsg_mood = float(v)


# Shader hosts (opaque Solid base + mesh, per the project's shader-on-Solid
# rule). The mood is baked in as a transform arg -- see tsg_set_mood's note.
transform tsg_page_fx(fever=0.0):
    mesh True
    shader "enter_m.tsg_page"
    u_fever fever

transform tsg_umbra_fx(calm=0.0):
    mesh True
    shader "enter_m.tsg_umbra"
    u_calm calm


# =============================================================================
#  BACKDROP  (theme switch + no-shader fallback, drawn by every screen)
# =============================================================================
screen tsg_backdrop():
    if tsg_theme == "heads":
        if TSG_SHADERS:
            add Solid("#efe4cb") at tsg_page_fx(tsg_mood)
        else:
            add Solid("#e8dcc0")
    else:
        if TSG_SHADERS:
            add Solid("#05060a") at tsg_umbra_fx(tsg_mood)
        else:
            add Solid("#05060a")


# =============================================================================
#  NVL SCREEN  --  accumulating gothic prose, themed
# =============================================================================
screen tsg_nvl(dialogue, items=None):

    use tsg_backdrop

    on "show" action SetVariable("quick_menu", False)
    on "replace" action SetVariable("quick_menu", False)

    # Book-page margins: 190px both sides, matched by the style xmaximums so
    # the column stays put even if a style is applied through the say id.
    vpgrid:
        cols 1
        xpos 190
        ypos 64
        xsize 900
        ymaximum 592
        mousewheel True
        yinitial 1.0
        spacing 6

        if dialogue:
            for d in dialogue:
                window:
                    id d.window_id
                    style "tsg_entry"
                    text d.what id d.what_id style ("tsg_prose_heads" if tsg_theme == "heads" else "tsg_prose_tails")

        if items:
            null height 14
            for i in items:
                hbox:
                    spacing 10
                    xoffset 36
                    if tsg_theme == "heads":
                        text "‣" color "#9c2b2baa" size 20 yalign 0.5 outlines [] font gui.interface_font
                    else:
                        text "‣" color "#8fa8bfaa" size 20 yalign 0.5 outlines [] font gui.interface_font
                    textbutton i.caption:
                        style ("tsg_choice_heads" if tsg_theme == "heads" else "tsg_choice_tails")
                        action i.action


# =============================================================================
#  CHOICE SCREEN  --  for `menu (screen="tsg_choice"):`
# =============================================================================
screen tsg_choice(items):
    modal True

    use tsg_backdrop

    vbox:
        xpos 226
        ypos 240
        spacing 14

        for i in items:
            hbox:
                spacing 10
                if tsg_theme == "heads":
                    text "‣" color "#7a1f1faa" size 20 yalign 0.5 outlines [] font gui.interface_font
                else:
                    text "‣" color "#8fa8bfaa" size 20 yalign 0.5 outlines [] font gui.interface_font
                textbutton i.caption:
                    style ("tsg_choice_heads" if tsg_theme == "heads" else "tsg_choice_tails")
                    action i.action


# =============================================================================
#  SECTION TITLE CARD
# =============================================================================
screen tsg_section_display(title):
    modal True

    use tsg_backdrop

    vbox:
        xalign 0.5
        yalign 0.44
        spacing 12

        text title:
            xalign 0.5
            style ("tsg_section_heads" if tsg_theme == "heads" else "tsg_section_tails")

        if tsg_theme == "heads":
            add Solid("#5d4a35") xysize (220, 1) xalign 0.5
        else:
            add Solid("#5f6d7d") xysize (220, 1) xalign 0.5

    timer 0.01 action With(Dissolve(0.8))
    timer 3.2 action Return()
    key "dismiss" action Return()


# =============================================================================
#  STYLES
# =============================================================================

style tsg_entry is default:
    background None
    padding (0, 3, 0, 3)
    xpos 0
    ypos 0
    xfill True
    xmaximum 900

# "Heads": ink on candlelit paper.
style tsg_prose_heads is default:
    color "#5c3c1a"
    font gui.default_font
    size 25
    outlines []
    line_spacing 3
    xpos 36
    ypos 0
    xmaximum 864

# "Tails": bone on the dark.
style tsg_prose_tails is default:
    color "#ccd3dd"
    font gui.default_font
    size 25
    outlines []
    line_spacing 3
    xpos 36
    ypos 0
    xmaximum 864

style tsg_section_heads is default:
    font "assets/gui/font/F25_Bank_Printer.ttf"
    size 30
    color "#3a2c1c"
    outlines []
    text_align 0.5

style tsg_section_tails is default:
    font "assets/gui/font/F25_Bank_Printer.ttf"
    size 30
    color "#b9c2cd"
    outlines []
    text_align 0.5

style tsg_choice_heads:
    background None
    hover_background Solid("#00000012")
    padding (8, 4)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style tsg_choice_heads_text:
    color "#6b5335"
    hover_color "#7a1f1f"
    font gui.default_font
    size 25
    outlines []

style tsg_choice_tails:
    background None
    hover_background Solid("#ffffff14")
    padding (8, 4)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style tsg_choice_tails_text:
    color "#77828f"
    hover_color "#dfe6ee"
    font gui.default_font
    size 25
    outlines []


# =============================================================================
#  HELPER LABELS  (mirroring the nier_* set)
# =============================================================================

# Enter the mode on a given face. Leaves the screen black; the first
# tsg_section / tsg line brings the themed backdrop up.
# GOTCHA: label parameters assign into the GLOBAL store. This one was once
# named `theme`, which clobbered Matsu'Py's built-in `theme` object (an instance
# of a deleted class from 00themes.rpy) -- the rollback log then held that
# unpicklable instance and EVERY save/reload died with
# "Can't pickle <class 'store._Theme'>". Keep label params namespaced.
label tsg_enter(tsg_face="heads"):
    $ tsg_prev_quick_menu = quick_menu
    $ tsg_active = True
    $ quick_menu = False
    $ tsg_theme = tsg_face
    $ tsg_mood = 0.0
    scene black
    $ renpy.pause(0.8)
    return

# Leave the mode: clear prose, restore state, cut to black, silence the
# engine's ambience channel.
label tsg_exit:
    nvl clear
    $ tsg_active = False
    $ quick_menu = tsg_prev_quick_menu
    stop track1 fadeout 2.0
    scene black
    return

# Themed section card. Clears accumulated prose. (Param namespaced for the
# same store-leak reason as tsg_enter's.)
label tsg_section(tsg_title=""):
    nvl clear
    scene black
    with dissolve
    $ renpy.pause(0.3)
    call screen tsg_section_display(tsg_title)
    scene black
    $ renpy.pause(0.3)
    return

# New page without leaving the mode.
label tsg_clear:
    nvl clear
    return
