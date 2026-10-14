# Greywake Field: tactical presentation and save-safe action dispatch.
# Rules live in python-packages/greywake.py. All visible information belongs to the
# chosen command; the opposing army receives no narrative viewpoint.

default cs_df_battle = None

init -4 python:
    import copy as cs_df_copy
    from greywake import GreywakeBattle

    CS_DF_UI_SIDES = {"akai": "SOUTHERN COMPACT", "rival": "NORTHERN CONCORD"}
    CS_DF_UNIT_ART = {
        "lancer": "lancer", "armor": "shield", "cavalry": "cavalry",
        "cleric": "cleric", "archer": "archer", "infantry": "swordsman",
        "axe": "axe", "berserker": "sam", "medic": "medic", "scout": "scout",
    }

    def cs_df_unit_art(unit):
        role = unit["role"]
        if unit["id"] in ("gary", "rusk", "sam"):
            name = unit["id"]
        else:
            name = unit["side"] if role == "lord" else CS_DF_UNIT_ART.get(role, "swordsman")
        return "assets/greywake/units/" + name + ".png"

    def cs_df_terrain_art(battle, x, y):
        name = battle.terrain[y][x]
        if name == "ford":
            name = "ford_h"
        elif name == "road":
            road_types = ("road", "bridge", "ford")
            horizontal = sum(0 <= nx < 18 and battle.terrain[y][nx] in road_types for nx in (x - 1, x + 1))
            vertical = sum(0 <= ny < 12 and battle.terrain[ny][x] in road_types for ny in (y - 1, y + 1))
            if horizontal >= vertical:
                name = "road_h"
        return "assets/greywake/terrain/" + name + ".png"

    def cs_df_order(method, *args):
        """Replace the per-game state; Function must never return a value."""
        if store.cs_df_battle is None:
            return
        previous = store.cs_df_battle
        event_start = len(previous.event_queue)
        battle = cs_df_copy.deepcopy(previous)
        getattr(battle, method)(*args)
        battle._ui_motion = {
            unit["id"]: ((previous.unit(unit["id"])["x"] - unit["x"]) * 48,
                        (previous.unit(unit["id"])["y"] - unit["y"]) * 48)
            for unit in battle.units
            if (previous.unit(unit["id"])["x"], previous.unit(unit["id"])["y"])
                != (unit["x"], unit["y"])
        }
        if method == "final_exchange":
            battle._ui_duel_hp = {uid: previous.unit(uid)["hp"] for uid in ("akai", "rival")}
        store.cs_df_battle = battle
        events = battle.event_queue[event_start:]
        if battle.phase == "final" and previous.phase != "final":
            renpy.music.play("assets/audio/bgm/epicbattlephase2.ogg", fadeout=0.4, fadein=0.4)
        elif battle.storm and not previous.storm:
            renpy.music.play("assets/audio/bgm/devoted.ogg", fadeout=0.7, fadein=0.7)
        effects = []
        for event in events:
            target = battle.unit(event.get("target"))
            if target and event["kind"] in ("attack", "hit", "heal"):
                heal = event["kind"] == "heal"
                amount = event.get("healed", 0) if heal else event.get("damage", 0)
                effects.append((target["x"], target["y"], ("+" if heal else "-") + str(amount), heal))
        if effects or method == "final_exchange":
            renpy.show_screen("cs_df_action_feedback", effects=effects, clash=method == "final_exchange")
            renpy.sound.play("assets/audio/sfx/sfx-shing.wav" if method == "final_exchange" else
                "assets/audio/sfx/sfx-beep.wav" if all(effect[3] for effect in effects) else
                "assets/audio/sfx/sfx-stab2.wav")
        elif method in ("rescue", "secure") and events:
            renpy.sound.play("assets/audio/sfx/pageflip.ogg")
        if method == "begin_enemy_turn" and battle.phase == "enemy":
            renpy.show_screen("cs_df_round_banner", number=battle.round, storm=battle.storm, enemy=True)
        if method in ("end_turn", "enemy_step") and battle.phase == "player" and battle.round != previous.round:
            dispatch = cs_df_field_dispatch(battle) if "cs_df_field_dispatch" in globals() else None
            if dispatch:
                renpy.show_screen("cs_df_battle_report", speaker=dispatch[0], message=dispatch[1], portrait=dispatch[2], events=events)
            else:
                renpy.show_screen("cs_df_round_banner", number=battle.round, storm=battle.storm)
        renpy.retain_after_load()
        renpy.restart_interaction()

    def cs_df_ui_view(battle):
        """Compute pathfinding once per committed state, never per tile/hover."""
        if getattr(cs_df_ui_view, "cached_battle", None) is battle:
            return cs_df_ui_view.cached_view
        selected = battle.selected_unit()
        targets = battle.attack_targets() if selected else []
        view = {
            "selected": selected,
            "reachable": battle.reachable() if selected and battle.phase == "player" else {},
            "attack_ids": set(unit["id"] for unit in targets),
            "targets": targets,
            "heal": battle.heal_targets() if selected else [],
            "rescue": battle.rescue_targets() if selected else [],
            "objectives": battle.adjacent_objectives() if selected else [],
            "actions": battle.legal_actions() if selected else [],
            "danger": battle.danger_tiles(),
            "tiles": {(unit["x"], unit["y"]): unit for unit in battle.units
                if not unit.get("removed", False) and not unit.get("dead", False)},
            "ready": [unit for unit in battle.units if unit["side"] == battle.side
                and not unit["acted"] and not unit["down"]
                and not unit.get("dead", False) and not unit.get("removed", False)],
        }
        cs_df_ui_view.cached_battle = battle
        cs_df_ui_view.cached_view = view
        return view

    def cs_df_map_click(x, y):
        battle = store.cs_df_battle
        if battle is None or battle.phase != "player":
            return
        view = cs_df_ui_view(battle)
        target = view["tiles"].get((x, y))
        if target and target["id"] in view["attack_ids"]:
            renpy.show_screen("cs_df_attack_preview", target_id=target["id"])
            renpy.restart_interaction()
        else:
            cs_df_order("click_tile", x, y)

    def cs_df_objective_status(obj):
        if obj.get("kind") == "wagon" and obj.get("secured", False):
            return "%s / %s saved" % (obj.get("evacuated", 0), obj.get("total", 0))
        if obj.get("secured", False):
            return "SECURED"
        if obj.get("evacuated", False):
            return "EVACUATED"
        if obj.get("hp", 1) <= 0:
            return "LOST"
        if obj.get("kind") == "wagon":
            return str(obj.get("remaining", 0)) + " awaiting escort"
        return "UNSECURED"

    def cs_df_unit_status(unit):
        if unit.get("dead", False):
            return "DEAD"
        if unit.get("removed", False):
            return "WITHDRAWN"
        if unit["down"]:
            return "DOWN - RESCUE"
        return "ACTED" if unit["acted"] else "READY"

    def cs_df_brief(text, limit=92):
        text = str(text)
        return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


style cs_df_text is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 17
    color "#e7e5dc"
    outlines []

style cs_df_title is cs_df_text:
    font "assets/gui/font/VerilySerifMono.otf"
    size 29
    color "#e5c88c"

style cs_df_label is cs_df_text:
    size 13
    color "#ccb884"
    kerning 1.2

style cs_df_small is cs_df_text:
    size 14
    color "#aeb8c1"

style cs_df_button is button:
    background Solid("#203348")
    hover_background Solid("#3b5262")
    selected_background Solid("#4e503c")
    insensitive_background Solid("#15202b")
    padding (11, 7)
    minimum (0, 34)

style cs_df_button_text is cs_df_text:
    size 16
    hover_color "#fff0bd"
    selected_color "#ffe3a1"
    insensitive_color "#65737b"

style cs_df_primary is cs_df_button:
    background Solid("#91733e")
    hover_background Solid("#b38f50")

style cs_df_primary_text is cs_df_button_text:
    color "#fff3d7"

style cs_df_panel is frame:
    background Solid("#111f2ef5")
    padding (16, 14)

style cs_df_hp is bar:
    ysize 5
    left_bar Solid("#87bb9a")
    right_bar Solid("#354450")
    thumb None
    thumb_shadow None

transform cs_df_unit_motion(dx=0, dy=0):
    xoffset dx
    yoffset dy
    easeout 0.30 xoffset 0 yoffset 0

transform cs_df_damage_rise:
    alpha 0.0
    yoffset 4
    ease 0.12 alpha 1.0 yoffset -5
    pause 0.40
    ease 0.42 alpha 0.0 yoffset -28

transform cs_df_strike_flash:
    alpha 0.0
    linear 0.07 alpha 0.6
    linear 0.24 alpha 0.0

transform cs_df_round_reveal:
    alpha 0.0
    xoffset -36
    ease 0.18 alpha 1.0 xoffset 0
    pause 0.75
    ease 0.22 alpha 0.0 xoffset 36


screen cs_df_tactical_map(battle):
    modal True
    zorder 105
    default danger_visible = False
    default hovered_tile = None

    # A call-screen parameter contains its original object after copy-on-write.
    # The authoritative default is deliberately read on every interaction.
    $ b = cs_df_battle if cs_df_battle is not None else battle
    $ view = cs_df_ui_view(b)
    $ selected = view["selected"]

    key "rollback" action NullAction()
    key "K_d" action ToggleScreenVariable("danger_visible")
    key "K_u" action Show("cs_df_company")
    key "K_h" action Show("cs_df_field_help")
    if b.phase == "player":
        key "K_e" action Show("cs_df_end_turn_confirm")
        key "K_BACKSPACE" action Function(cs_df_order, "cancel")
    elif b.phase == "enemy":
        # One serialized company action per tick. The callback returns None,
        # and the saved engine queue permits loading during the enemy phase.
        timer 0.70 repeat True modal True action Function(cs_df_order, "enemy_step")

    add Solid("#09131e")
    add Solid("#b09561") pos (24, 72) xysize (1232, 1)
    text "DEAD FANTASY" style "cs_df_label" pos (26, 15)
    text "Greywake Field" style "cs_df_title" pos (24, 32)
    text CS_DF_UI_SIDES.get(b.side, b.side.upper()) style "cs_df_label" pos (370, 20)
    text "%s · ROUND %02d / 10" % ("ENEMY PHASE" if b.phase == "enemy" else "YOUR COMMAND", min(b.round, 10)) style "cs_df_text" pos (370, 42)
    text ("STORM · FORD FLOODED" if b.storm else "FORD OPEN · STORM IN ROUND 5") style "cs_df_label" pos (730, 22)
    text "The lords draw. The losses are yours to change." style "cs_df_small" pos (730, 44)
    textbutton "HELP  H" style "cs_df_button" pos (1168, 23) xsize 88 action Show("cs_df_field_help")

    fixed:
        pos (24, 92)
        xysize (864, 576)
        for ty in range(12):
            for tx in range(18):
                add cs_df_terrain_art(b, tx, ty) pos (tx * 48, ty * 48) xysize (48, 48) nearest True
                add Solid("#09131e32") pos (tx * 48 + 47, ty * 48) xysize (1, 48)
                add Solid("#09131e32") pos (tx * 48, ty * 48 + 47) xysize (48, 1)
                if danger_visible and (tx, ty) in view["danger"]:
                    add Solid("#d556623f") pos (tx * 48, ty * 48) xysize (48, 48)
                if (tx, ty) in view["reachable"]:
                    add Solid("#48adf44e") pos (tx * 48 + 1, ty * 48 + 1) xysize (46, 46)
                if (tx, ty) in view["tiles"] and view["tiles"][(tx, ty)]["id"] in view["attack_ids"]:
                    add Solid("#df585c90") pos (tx * 48 + 1, ty * 48 + 1) xysize (46, 46)

        for obj in b.objectives:
            $ complete = obj.get("secured", False) or obj.get("evacuated", False)
            $ marker_color = "#8cc99c" if complete else "#ecd590"
            fixed:
                pos (obj["x"] * 48, obj["y"] * 48)
                xysize (48, 48)
                add ("assets/greywake/terrain/camp.png" if obj["kind"] == "wagon" else "assets/greywake/terrain/granary.png") xysize (48, 48) nearest True alpha (0.45 if complete or obj.get("hp", 1) <= 0 else 1.0)
                add Solid("#0b172dcc") pos (1, 1) xysize (20, 20)
                text ("+" if obj["kind"] == "wagon" else "G") size 18 color marker_color pos (5, -1) outlines [(1, "#09131e", 0, 0)]

        for unit in b.units:
            if not unit.get("removed", False) and not unit.get("dead", False):
                $ friendly = unit["side"] == b.side
                $ uc = "#619ec7" if friendly else "#ce6f70"
                $ motion = getattr(b, "_ui_motion", {}).get(unit["id"], (0, 0))
                fixed:
                    pos (unit["x"] * 48, unit["y"] * 48)
                    xysize (48, 48)
                    add Solid(uc + "b0") pos (6, 35) xysize (36, 9)
                    add cs_df_unit_art(unit) xysize (48, 48) nearest True alpha (0.42 if unit["acted"] or unit["down"] else 1.0) at cs_df_unit_motion(*motion)
                    add Solid("#08121ddc") pos (5, 43) xysize (38, 4)
                    add Solid("#93d4a1" if friendly else "#e79683") pos (5, 43) xysize (max(0, int(38.0 * unit["hp"] / unit["max_hp"])), 3)
                    if unit["down"]:
                        text "+" color "#ffe9d0" size 26 bold True pos (31, -5) outlines [(2, "#8b303a", 0, 0)]
                    elif unit["acted"]:
                        add Solid("#eff2da") pos (39, 3) xysize (4, 4)
                    if unit["id"] == b.selected_id:
                        add Solid("#ffe3a1") xysize (48, 2)
                        add Solid("#ffe3a1") pos (0, 46) xysize (48, 2)
                        add Solid("#ffe3a1") xysize (2, 48)
                        add Solid("#ffe3a1") pos (46, 0) xysize (2, 48)

        for ty in range(12):
            for tx in range(18):
                button:
                    pos (tx * 48, ty * 48)
                    xysize (48, 48)
                    padding (0, 0)
                    background None
                    hover_background Solid("#fff4cc2b")
                    action Function(cs_df_map_click, tx, ty)
                    hovered SetScreenVariable("hovered_tile", (tx, ty))
                    unhovered SetScreenVariable("hovered_tile", None)
                    sensitive b.phase == "player"

    frame:
        style "cs_df_panel"
        pos (910, 92)
        xysize (346, 159)
        if selected:
            vbox:
                spacing 6
                text "%s · RNG %s%s / %s" % (selected["role"].upper(), selected["range_min"], ("-%s" % selected["range_max"]) if selected["range_max"] != selected["range_min"] else "", cs_df_unit_status(selected)) style "cs_df_label" size 12
                text selected["name"] style "cs_df_title" size 25
                bar value selected["hp"] range selected["max_hp"] style "cs_df_hp" xsize 312
                text "HP %s/%s   ATK %s   DEF %s   MOV %s" % (selected["hp"], selected["max_hp"], selected["atk"], selected["defense"], selected["mov"]) style "cs_df_text" size 16
                text ("Moved. Choose an order below." if b.moved else "Blue tiles: move. Red units: engage.") style "cs_df_small"
        else:
            vbox:
                spacing 8
                text "ORDERS" style "cs_df_label"
                if b.phase == "enemy":
                    text "Opposing army moves" style "cs_df_title" size 22
                    text "Watch the red companies.\nYour command resumes next round." style "cs_df_text"
                    text "Save / Menu remains available." style "cs_df_small"
                else:
                    text "Choose a blue unit" style "cs_df_title" size 23
                    text "Move, then fight or lend a hand.\nEvery company acts once per round." style "cs_df_text"
                    text "%s companies still ready" % len(view["ready"]) style "cs_df_small"

    frame:
        style "cs_df_panel"
        pos (910, 259)
        xysize (346, 153)
        viewport:
            mousewheel True
            draggable True
            ysize 125
            scrollbars "vertical"
            vbox:
                spacing 4
                if selected and b.phase == "player":
                    for target in view["targets"]:
                        textbutton "Engage  ·  %s" % target["name"] style "cs_df_button" xsize 290 action Show("cs_df_attack_preview", target_id=target["id"])
                    for target in view["heal"]:
                        textbutton "Heal  ·  %s" % target["name"] style "cs_df_button" xsize 290 action Function(cs_df_order, "heal", target["id"])
                    for target in view["rescue"]:
                        textbutton "Rescue  ·  %s" % target["name"] style "cs_df_button" xsize 290 action Function(cs_df_order, "rescue", target["id"])
                    if "secure" in view["actions"]:
                        for obj in view["objectives"]:
                            if obj["kind"] != "wagon" and not obj.get("secured", False) and obj.get("hp", 1) > 0:
                                textbutton "Secure  ·  %s" % obj["name"] style "cs_df_button" xsize 290 action Function(cs_df_order, "secure", obj["id"])
                    hbox:
                        spacing 6
                        textbutton "Wait" style "cs_df_button" xsize 142 action Function(cs_df_order, "wait_unit") sensitive "wait" in view["actions"]
                        textbutton ("Undo move" if b.moved else "Deselect") style "cs_df_button" xsize 142 action Function(cs_df_order, "cancel") sensitive "cancel" in view["actions"]
                else:
                    text "FIELD ORDERS" style "cs_df_label"
                    text "Escort the wagons. Secure the grain.\nRescue fallen allies before time runs out." style "cs_df_text" size 17
                    text "Only a lord can fell the other lord.\nTheir final exchange ends the map." style "cs_df_small"

    frame:
        style "cs_df_panel"
        pos (910, 420)
        xysize (346, 145)
        vbox:
            spacing 3
            text "PEOPLE & PROVISIONS" style "cs_df_label"
            for obj in b.objectives:
                hbox:
                    xsize 313
                    text cs_df_brief(obj["name"], 20) style "cs_df_small" xsize 156
                    text cs_df_objective_status(obj) style "cs_df_small" size 13 color ("#acd0aa" if obj.get("secured", False) or obj.get("evacuated", False) else "#dbc497")

    frame:
        style "cs_df_panel"
        pos (910, 573)
        xysize (346, 95)
        vbox:
            spacing 4
            text "LATEST DISPATCH" style "cs_df_label"
            if b.log:
                text cs_df_brief(b.log[-1], 110) style "cs_df_small" size 14

    if hovered_tile:
        $ terrain = b.terrain_info(*hovered_tile)
        $ hover_unit = view["tiles"].get(hovered_tile)
        text "%s%s  ·  COVER +%s  ·  MOVE %s" % ((hover_unit["name"] + " / ") if hover_unit else "", terrain["name"].upper(), terrain["defense"], terrain["cost"] if terrain["passable"] else "BLOCKED") style "cs_df_small" pos (24, 682) size 15
    else:
        text "BLUE: your command    RED: opposing army    +: rescue    G: grain" style "cs_df_small" pos (24, 682) size 15

    hbox:
        pos (676, 676)
        spacing 5
        textbutton "Danger  D" style "cs_df_button" selected danger_visible action ToggleScreenVariable("danger_visible")
        textbutton "Company  U" style "cs_df_button" action Show("cs_df_company")
        textbutton "Dispatches" style "cs_df_button" action Show("cs_df_dispatches")
        textbutton "Save / Menu" style "cs_df_button" action ShowMenu("save")
        textbutton "End round  E" style "cs_df_primary" action Show("cs_df_end_turn_confirm") sensitive b.phase == "player"

    if b.phase in ("final", "done"):
        use cs_df_final_engagement(b)


screen cs_df_attack_preview(target_id):
    modal True
    zorder 120
    $ b = cs_df_battle
    $ attacker = b.selected_unit()
    $ defender = b.unit(target_id)
    $ forecast = b.preview(attacker["id"], target_id) if attacker and defender else None
    key "game_menu" action Hide("cs_df_attack_preview")
    # A button can inherit the main game's fixed height/hover background.
    # Draw the scrim independently; Back and Escape dismiss this modal.
    add Solid("#050c16ca") xysize (1280, 720)
    if forecast:
        frame:
            style "cs_df_panel"
            align (0.5, 0.5)
            xsize 610
            padding (28, 24)
            vbox:
                spacing 16
                text ("LAST EXCHANGE FORECAST" if forecast.get("paired", False) else "COMBAT FORECAST") style "cs_df_label" xalign 0.5
                hbox:
                    spacing 26
                    vbox:
                        xsize 252
                        spacing 10
                        text attacker["name"] style "cs_df_title" size 23
                        add cs_df_unit_art(attacker) xysize (96, 96) xalign 0.5 nearest True
                        text "HP  %s to %s" % (attacker["hp"], max(0, attacker["hp"] - forecast["counter_damage"])) style "cs_df_text"
                        text "STRIKE  %s" % forecast["damage"] style "cs_df_title" size 24
                    vbox:
                        xsize 252
                        spacing 10
                        text defender["name"] style "cs_df_title" size 23
                        add cs_df_unit_art(defender) xysize (96, 96) xalign 0.5 nearest True
                        text "HP  %s to %s" % (defender["hp"], max(0, defender["hp"] - forecast["damage"])) style "cs_df_text"
                        text "%s  %s" % ("BOUND STRIKE" if forecast.get("paired", False) else "COUNTER", forecast["counter_damage"]) style "cs_df_title" size 24
                text "Damage is certain. Cover and weapon range are included." style "cs_df_small"
                if forecast.get("last_exchange", False):
                    text "A lord's decisive strike triggers the paired final exchange.\nBoth lords will fall; all remaining rescue time is lost." style "cs_df_text" color "#efd28a"
                elif forecast.get("lethal", False):
                    text "This strike puts the target out of the fight." style "cs_df_text" color "#e2a3a0"
                elif forecast["counter_damage"] >= attacker["hp"]:
                    text "The counterattack puts %s out of the fight." % attacker["name"] style "cs_df_text" color "#e2a3a0"
                hbox:
                    spacing 12
                    textbutton ("Enter the Last Exchange" if forecast.get("paired", False) else "Commit attack") style "cs_df_primary" xsize 260 action [Hide("cs_df_attack_preview"), Function(cs_df_order, "attack", target_id)] sensitive forecast["can_attack"]
                    textbutton "Back" style "cs_df_button" xsize 260 action Hide("cs_df_attack_preview")


screen cs_df_end_turn_confirm():
    modal True
    zorder 120
    $ b = cs_df_battle
    $ ready = len(cs_df_ui_view(b)["ready"])
    key "game_menu" action Hide("cs_df_end_turn_confirm")
    add Solid("#050c16cc")
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xsize 570
        padding (28, 26)
        vbox:
            spacing 18
            text "END ROUND %s?" % min(b.round, 10) style "cs_df_title"
            if ready:
                text "%s companies still have an action. The opposing army moves next; wounded companies and exposed wagons remain at risk." % ready style "cs_df_text"
            else:
                text "Your companies have acted. The opposing army moves next, then the storm and supply losses are resolved." style "cs_df_text"
            if b.round >= 10:
                text "This is the last round. After the opposing army moves, both lords must meet." style "cs_df_text" color "#ead095"
            hbox:
                spacing 12
                textbutton "End round" style "cs_df_primary" xsize 250 action [Hide("cs_df_end_turn_confirm"), Function(cs_df_order, "begin_enemy_turn")]
                textbutton "Keep issuing orders" style "cs_df_button" xsize 250 action Hide("cs_df_end_turn_confirm")


screen cs_df_company():
    modal True
    zorder 120
    $ b = cs_df_battle
    key "game_menu" action Hide("cs_df_company")
    key "K_u" action Hide("cs_df_company")
    add Solid("#050c16dd")
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xysize (750, 606)
        padding (28, 24)
        vbox:
            spacing 12
            text "YOUR COMPANIES" style "cs_df_title"
            text "Select a ready company to locate it on the field." style "cs_df_small"
            viewport:
                ysize 435
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 7
                    for unit in b.units:
                        if unit["side"] == b.side:
                            button:
                                style "cs_df_button"
                                xsize 670
                                action [Hide("cs_df_company"), Function(cs_df_order, "select", unit["id"])]
                                sensitive b.phase == "player" and not unit.get("removed", False) and not unit["down"] and not unit.get("dead", False) and not unit["acted"]
                                hbox:
                                    spacing 12
                                    add cs_df_unit_art(unit) xysize (48, 48) nearest True
                                    vbox:
                                        xsize 270
                                        text unit["name"] style "cs_df_text" size 21
                                        text unit["role"].upper() style "cs_df_label"
                                    vbox:
                                        text "HP %s / %s" % (unit["hp"], unit["max_hp"]) style "cs_df_text"
                                        text cs_df_unit_status(unit) style "cs_df_label"
            textbutton "Back to the field" style "cs_df_primary" xfill True action Hide("cs_df_company")


screen cs_df_dispatches():
    modal True
    zorder 120
    key "game_menu" action Hide("cs_df_dispatches")
    add Solid("#050c16dd")
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xysize (820, 600)
        padding (28, 24)
        vbox:
            spacing 16
            text "FIELD DISPATCHES" style "cs_df_title"
            text "Most recent first. These are reports received by your command." style "cs_df_small"
            viewport:
                ysize 418
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 12
                    for entry in reversed(cs_df_battle.log):
                        text str(entry) style "cs_df_text" xsize 732
            textbutton "Back to the field" style "cs_df_primary" xfill True action Hide("cs_df_dispatches")


screen cs_df_field_help():
    modal True
    zorder 125
    key "game_menu" action Hide("cs_df_field_help")
    key "K_h" action Hide("cs_df_field_help")
    add Solid("#050c16e6")
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xysize (900, 630)
        padding (30, 25)
        vbox:
            spacing 14
            text "GREYWAKE · FIELD MANUAL" style "cs_df_title"
            text "Ten rounds. One command. No victory without a cost." style "cs_df_text" color "#e6ce95"
            viewport:
                ysize 446
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 15
                    xsize 812
                    text "MOVE & ACT" style "cs_df_label"
                    text "Click a blue company, then a blue tile to move. Each company may move and take one order per round. Red targets are in weapon range; select one to review the exact strike and counterattack before committing. Wait spends the action. Undo move is available until you commit an order." style "cs_df_text"
                    text "Bows attack from two tiles away; other weapons attack adjacent tiles. Swords beat axes, axes beat lances, and lances beat swords: advantage adds 2 damage, disadvantage subtracts 1. Combat forecasts include these modifiers." style "cs_df_small"
                    text "BRING PEOPLE HOME" style "cs_df_label"
                    text "Move beside a wagon and choose Rescue to escort its people off the field. Rescue also withdraws an adjacent fallen ally. Clerics and medics can heal nearby wounded companies. Move beside a grain objective and choose Secure to preserve its stores. Unprotected people and supplies are lost as the battle continues." style "cs_df_text"
                    text "THE FIELD FIGHTS BACK" style "cs_df_label"
                    text "Roads ease movement; woodland, ridges and fortifications cost time but offer cover. Rivers require a crossing. Hover a tile to inspect its cost and cover. Danger (D) shows the opposing army's potential reach; it is a warning, not a promise that every marked tile will be attacked." style "cs_df_text"
                    text "THE TWO LORDS" style "cs_df_label"
                    text "Ordinary companies cannot finish a lord. Only the two lords can defeat each other. A decisive lord attack ends rescue time early. Otherwise the final engagement begins after round ten. You must resolve their paired strike: neither army wins, but the companies, civilians and grain you save change what remains." style "cs_df_text"
                    text "CONTROLS & SAVES" style "cs_df_label"
                    text "D: danger overlay. U: company list. H: this manual. E: end-round confirmation. Backspace: undo movement or deselect. Escape opens the game menu; Save / Menu opens the save screen. Battle state is saved during the map. Dialogue rollback is disabled during tactical play." style "cs_df_text"
            textbutton "Return to Greywake" style "cs_df_primary" xfill True action Hide("cs_df_field_help")


screen cs_df_final_engagement(b):
    $ akai = b.unit("akai")
    $ rival = b.unit("rival")
    add Solid("#050c16e5")
    button:
        style "default"
        pos (0, 0)
        xysize (1280, 720)
        padding (0, 0)
        background None
        hover_background None
        selected_background None
        selected_hover_background None
        action NullAction()
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xysize (960, 662)
        padding (32, 25)
        vbox:
            spacing 8
            text ("FINAL ENGAGEMENT" if b.phase == "final" else "GREYWAKE HOLDS NO VICTOR") style "cs_df_title" xalign 0.5 size 28
            text "SOUTHERN COMPACT                 NORTHERN CONCORD" style "cs_df_label" xalign 0.5
            hbox:
                xalign 0.5
                spacing 126
                vbox:
                    xsize 200
                    add cs_df_unit_art(akai) xysize (112, 112) xalign 0.5 nearest True
                    text akai["name"] style "cs_df_title" size 22 xalign 0.5
                    text ("FINAL STRIKE" if b.phase == "final" else "FALLEN") style "cs_df_label" xalign 0.5
                    text "HP %s to 0" % (akai["hp"] if b.phase == "final" else getattr(b, "_ui_duel_hp", {}).get("akai", 0)) style "cs_df_text" xalign 0.5
                vbox:
                    xsize 200
                    add cs_df_unit_art(rival) xysize (112, 112) xalign 0.5 nearest True
                    text rival["name"] style "cs_df_title" size 22 xalign 0.5
                    text ("FINAL STRIKE" if b.phase == "final" else "FALLEN") style "cs_df_label" xalign 0.5
                    text "HP %s to 0" % (rival["hp"] if b.phase == "final" else getattr(b, "_ui_duel_hp", {}).get("rival", 0)) style "cs_df_text" xalign 0.5
            if b.phase == "final":
                null height 36
                text "Both lords commit to the same opening. The first blow cannot cancel the second. Resolve the exchange to end the battle." style "cs_df_text" xsize 896 text_align 0.5
                text "Binding counterstroke · Both lords incapacitated · No further orders" style "cs_df_small" xalign 0.5
                textbutton "Resolve the paired strike" style "cs_df_primary" xfill True action Function(cs_df_order, "final_exchange")
            else:
                text "The lords fall together. The survivors carry the result away." style "cs_df_text" xalign 0.5
                text "%s / 40 PEOPLE EVACUATED    ·    %s / 2 GRAIN STORES SECURED" % (b.result["civilians_evacuated"], b.result["supplies_secured"]) style "cs_df_label" xalign 0.5
                text "%s soldiers dead  ·  %s wounded across both armies" % (b.result["army_dead"], b.result["army_wounded"]) style "cs_df_small" xalign 0.5
                text "Southern Compact: %s dead / %s wounded    ·    Northern Concord: %s dead / %s wounded" % (b.result["armies"]["akai"]["dead"], b.result["armies"]["akai"]["wounded"], b.result["armies"]["rival"]["dead"], b.result["armies"]["rival"]["wounded"]) style "cs_df_small" size 14 xalign 0.5
                viewport:
                    ysize 99
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        text "COMPANY LEADERS" style "cs_df_label"
                        text "Dead: %s" % (", ".join(b.result["dead"]) or "None") style "cs_df_text" size 17 xsize 866 color "#e3aaaa"
                        text "Wounded: %s" % (", ".join(b.result["wounded"]) or "None") style "cs_df_text" size 17 xsize 866
                textbutton "Leave the field" style "cs_df_primary" xfill True action Return(b.result)


screen cs_df_action_feedback(effects, clash=False):
    zorder 110
    if clash:
        add Solid("#efdbb5") at cs_df_strike_flash
    for i, effect in enumerate(effects):
        $ fx, fy, amount, healed = effect
        if not healed:
            add Solid("#f3cabc") pos (24 + fx * 48, 92 + fy * 48) xysize (48, 48) at cs_df_strike_flash
        text amount pos (34 + fx * 48, 89 + fy * 48) size 25 color ("#adf0b7" if healed else "#fff0d7") outlines [(2, "#101724", 0, 0)] at cs_df_damage_rise
    timer 1.1 action Hide("cs_df_action_feedback")


screen cs_df_round_banner(number, storm=False, enemy=False):
    zorder 109
    frame:
        style "cs_df_panel"
        pos (214, 313)
        xsize 484
        padding (28, 20)
        at cs_df_round_reveal
        vbox:
            spacing 5
            text "ROUND %02d · %s" % (number, "ENEMY PHASE" if enemy else "YOUR COMMAND") style "cs_df_title" size 23 xalign 0.5
            text ("The ford is flooded." if storm else "The storm is coming.") style "cs_df_small" xalign 0.5
    timer 1.2 action Hide("cs_df_round_banner")


screen cs_df_battle_report(speaker, message, portrait=None, events=()):
    modal True
    zorder 120
    key "game_menu" action Hide("cs_df_battle_report")
    add Solid("#050c16c9")
    frame:
        style "cs_df_panel"
        align (0.5, 0.5)
        xsize 800
        padding (28, 24)
        vbox:
            spacing 17
            text "ROUND %s · COMMAND REPORT" % cs_df_battle.round style "cs_df_label"
            hbox:
                spacing 24
                if portrait:
                    add ("assets/extra_sprites/dead_fantasy/%s.png" % ("sam_clean" if portrait == "sam" else portrait)) xysize (130, 170) fit "contain"
                vbox:
                    xsize (590 if portrait else 742)
                    spacing 10
                    text speaker style "cs_df_title" size 26
                    text message style "cs_df_text" size 21
            for entry in [event for event in events if event["kind"] in ("death", "pressure", "supply_lost", "evacuate")][-3:]:
                text entry["text"] style "cs_df_small" xsize 742
            textbutton "Acknowledge" style "cs_df_primary" xfill True action Hide("cs_df_battle_report")
