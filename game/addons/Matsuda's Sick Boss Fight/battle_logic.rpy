default msbf_battle_state = None
default msbf_battle_menu_locked = False

init -1 python:
    import random
    import math

    MSBF_AFFINITY_NAMES = {
        "slash": "Slash",
        "pierce": "Pierce",
        "fire": "Fire",
        "ice": "Ice",
        "lightning": "Lightning",
        "wind": "Wind",
        "psychic": "Psychic",
        "almighty": "Almighty",
    }

    MSBF_PHASE1_AFFINITY_SETS = [
        (["fire"], ["ice", "pierce"]),
        (["ice"], ["fire", "slash"]),
        (["lightning"], ["wind", "pierce"]),
        (["wind"], ["lightning", "slash"]),
        (["fire", "slash"], ["lightning"]),
        (["ice", "pierce"], ["fire"]),
        (["slash"], ["pierce", "psychic"]),
        (["pierce"], ["fire", "psychic"]),
        (["psychic"], ["ice", "wind"]),
        (["lightning", "psychic"], ["pierce"]),
    ]

    MSBF_PHASE2_AFFINITY_ELEMENTS = ["slash", "pierce", "fire", "ice", "lightning", "wind", "psychic"]
    MSBF_PHASE2_WEAKNESS_COUNT = 3
    MSBF_PHASE2_RESIST_COUNT = 3
    MSBF_PHASE2_ADAPT_WEAK_HITS = 3
    MSBF_PHASE3_WEAKNESS_COUNT = 2
    MSBF_PHASE3_RESIST_COUNT = 4
    MSBF_PHASE3_ADAPT_WEAK_HITS = 2
    MSBF_IDMODE_PHASE3_MUSIC_INST = "addons/Matsuda's Sick Boss Fight/idmode/embracedbytheflameinst.ogg"
    MSBF_IDMODE_PHASE3_MUSIC_VOCAL = "addons/Matsuda's Sick Boss Fight/idmode/embracedbytheflamevocal.ogg"
    MSBF_IDMODE_PHASE3_INST_CHANNEL = "track1"
    MSBF_IDMODE_PHASE3_VOCAL_CHANNEL = "track2"
    MSBF_IDMODE_PHASE3_CROSSFADE = 1.45
    MSBF_IDMODE_PHASE3_VOCAL_FADEIN = 0.55
    MSBF_IDMODE_PHASE3_INST_BED = 0.18
    MSBF_SHMUP_STAGE_X = 452
    MSBF_SHMUP_STAGE_Y = 30
    MSBF_SHMUP_STAGE_WIDTH = 786
    MSBF_SHMUP_STAGE_HEIGHT = 458
    MSBF_SHMUP_DURATION_TICKS = 168
    MSBF_SHMUP_PLAYER_RADIUS = 6
    MSBF_SHMUP_SUCCESS_DAMAGE = 900
    MSBF_SHMUP_FAILURE_DAMAGE = 140
    MSBF_SHMUP_TICK_SECONDS = 0.033
    MSBF_SHMUP_MAX_BULLETS = 220
    MSBF_SHMUP_GRACE_TICKS = 24
    MSBF_SHMUP_HIT_LIMIT = 3
    MSBF_SHMUP_HIT_INVULN_TICKS = 24
    MSBF_SHMUP_PANIC_CLEAR_RADIUS = 118

    MSBF_SFX_DIR = "addons/Matsuda's Sick Boss Fight/sfx/"
    MSBF_TOUHOU_SFX_DIR = "addons/Matsuda's Sick Boss Fight/sfx_touhou/"
    MSBF_DAMAGE_VARIANCE_STDEV = 0.055
    MSBF_DAMAGE_VARIANCE_MIN = 0.88
    MSBF_DAMAGE_VARIANCE_MAX = 1.12
    MSBF_HEAL_VARIANCE_STDEV = 0.04
    MSBF_HEAL_VARIANCE_MIN = 0.90
    MSBF_HEAL_VARIANCE_MAX = 1.10
    MSBF_PLAYER_ACTION_CAP_MAX = 15
    MSBF_PRESS_TURN_SLOT_WIDTH = 40
    MSBF_PRESS_TURN_SLOT_SPACING = 4
    MSBF_PRESS_TURN_ROW_X = 7

    def msbf_sfx(filename):
        return MSBF_SFX_DIR + filename

    def msbf_touhou_sfx(filename):
        return MSBF_TOUHOU_SFX_DIR + filename

    def msbf_clamp(value, lower, upper):
        return max(lower, min(upper, value))

    def msbf_gaussian_variance(stdev, lower, upper):
        return msbf_clamp(random.gauss(1.0, stdev), lower, upper)

    def msbf_battle_is_live():
        battle = globals().get("msbf_battle_state", None)
        return bool(battle is not None and getattr(battle, "result", None) is None)

    def msbf_save_load_locked():
        return bool(globals().get("msbf_battle_menu_locked", False) and msbf_battle_is_live())

    def msbf_clear_battle_watch():
        global msbf_battle_state
        global msbf_battle_menu_locked
        msbf_battle_state = None
        msbf_battle_menu_locked = False
        try:
            persistent.msbf_battle_token = None
            persistent.msbf_battle_serial = 0
        except Exception:
            pass

    def msbf_stop_battle_music(fadeout=0.35):
        for channel_name in ("music", MSBF_IDMODE_PHASE3_INST_CHANNEL, MSBF_IDMODE_PHASE3_VOCAL_CHANNEL):
            try:
                renpy.music.stop(channel=channel_name, fadeout=fadeout)
            except Exception:
                pass

    MSBF_UI_SFX = {
        "hover": msbf_sfx("ui_hover.wav"),
        "accept": msbf_sfx("ui_accept.wav"),
        "denied": msbf_sfx("ui_denied.wav"),
    }

    MSBF_SFX = {
        "act": msbf_sfx("ui_accept.wav"),
        "denied": msbf_sfx("ui_denied.wav"),
        "turn": msbf_sfx("turn_ready.wav"),
        "turn_ready": msbf_sfx("turn_ready.wav"),
        "pass": msbf_sfx("pass.wav"),
        "hit": msbf_sfx("hit.wav"),
        "weak": msbf_sfx("weak.wav"),
        "crit": msbf_sfx("crit.wav"),
        "resist": msbf_sfx("resist.wav"),
        "miss": msbf_sfx("miss.wav"),
        "scan": msbf_sfx("scan.wav"),
        "heal": msbf_sfx("heal.wav"),
        "revive": msbf_sfx("revive.wav"),
        "buff": msbf_sfx("buff.wav"),
        "debuff": msbf_sfx("debuff.wav"),
        "guard": msbf_sfx("guard.wav"),
        "enemy": msbf_sfx("enemy.wav"),
        "shuffle": msbf_sfx("shuffle.wav"),
        "phase": msbf_sfx("phase.wav"),
        "explode": "addons/Matsuda's Sick Boss Fight/explode.ogg",
        "recover": msbf_sfx("recover.wav"),
        "down": msbf_sfx("down.wav"),
        "victory": msbf_sfx("victory.wav"),
        "touhou_start": msbf_touhou_sfx("powerup.wav"),
        "touhou_shot": msbf_touhou_sfx("tan00.wav"),
        "touhou_shot_alt": msbf_touhou_sfx("tan01.wav"),
        "touhou_needle": msbf_touhou_sfx("enep00.wav"),
        "touhou_burst": msbf_touhou_sfx("kira00.wav"),
        "touhou_burst_alt": msbf_touhou_sfx("kira01.wav"),
        "touhou_laser": msbf_touhou_sfx("lazer00.wav"),
        "touhou_graze": msbf_touhou_sfx("graze.wav"),
        "touhou_hit": msbf_touhou_sfx("damage00.wav"),
        "touhou_down": msbf_touhou_sfx("pldead00.wav"),
        "touhou_clear": msbf_touhou_sfx("extend.wav"),
        "touhou_warning": msbf_touhou_sfx("timeout.wav"),
    }

    MSBF_SFX_LAYERS = {
        "hit": [("enemy", 0.16)],
        "weak": [("hit", 0.45), ("shuffle", 0.24)],
        "crit": [("hit", 0.52), ("buff", 0.28)],
        "resist": [("guard", 0.34)],
        "guard": [("buff", 0.20)],
        "enemy": [("hit", 0.18)],
        "enemy_aoe": [("hit", 0.30), ("debuff", 0.20)],
        "shuffle": [("scan", 0.22)],
        "phase": [("crit", 0.42), ("shuffle", 0.48), ("down", 0.18)],
        "victory": [("phase", 0.24)],
        "down": [("debuff", 0.32)],
    }

    class MSBFSkill(object):
        def __init__(
                self,
                skill_id,
                name,
                cost=0,
                kind="damage",
                element="slash",
                power=0,
                target="boss",
                stat="offense",
                accuracy=1.0,
                crit=0.0,
                recoil=0.0,
                description=""):
            self.id = skill_id
            self.name = name
            self.cost = cost
            self.kind = kind
            self.element = element
            self.power = power
            self.target = target
            self.stat = stat
            self.accuracy = accuracy
            self.crit = crit
            self.recoil = recoil
            self.description = description

    class MSBFCombatant(object):
        def __init__(
                self,
                unit_id,
                name,
                max_hp,
                max_mp,
                offense,
                magic,
                defense,
                agility,
                attack_element="slash",
                weaknesses=None,
                resists=None,
                skills=None):
            self.id = unit_id
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_mp = max_mp
            self.mp = max_mp
            self.offense = offense
            self.magic = magic
            self.defense = defense
            self.agility = agility
            self.attack_element = attack_element
            self.weaknesses = list(weaknesses or [])
            self.resists = list(resists or [])
            self.skill_ids = list(skills or [])
            self.guard = False
            self.focus = False
            self.taunt = False
            self.row = "front"
            self.atk_stage = 0
            self.def_stage = 0
            self.agi_stage = 0
            self.phase = 1
            self.used_second_wind = False
            self.adapt_element = None
            self.adapt_turns = 0

        @property
        def alive(self):
            return self.hp > 0

        @property
        def hp_ratio(self):
            if self.max_hp <= 0:
                return 0.0
            return max(0.0, min(1.0, float(self.hp) / float(self.max_hp)))

        @property
        def mp_ratio(self):
            if self.max_mp <= 0:
                return 0.0
            return max(0.0, min(1.0, float(self.mp) / float(self.max_mp)))

        @property
        def skills(self):
            return [MSBF_SKILLS[skill_id] for skill_id in self.skill_ids]

        def clamp(self):
            self.hp = max(0, min(self.max_hp, int(self.hp)))
            self.mp = max(0, min(self.max_mp, int(self.mp)))
            self.atk_stage = max(-2, min(2, self.atk_stage))
            self.def_stage = max(-2, min(2, self.def_stage))
            self.agi_stage = max(-2, min(2, self.agi_stage))

    MSBF_SKILLS = {
        "attack": MSBFSkill(
            "attack",
            "Attack",
            kind="damage",
            element="weapon",
            power=68,
            accuracy=0.96,
            crit=0.06,
            description="A basic weapon strike."
        ),
        "attackpierce": MSBFSkill(
            "attackpierce",
            "Attack (Pierce)",
            kind="damage",
            element="pierce",
            power=68,
            accuracy=0.90,
            crit=0.12,
            description="A basic piercing strike."
        ),
        "ruin_edge": MSBFSkill(
            "ruin_edge",
            "Ruin Edge",
            cost=12,
            kind="damage",
            element="almighty",
            power=102,
            accuracy=0.96,
            crit=0.08,
            description="Almighty damage."
        ),
        "focus": MSBFSkill(
            "focus",
            "Focus",
            cost=5,
            kind="focus",
            element="support",
            description="Greatly strengthens the user's next attack."
        ),
        "fire": MSBFSkill(
            "fire",
            "Fire",
            cost=9,
            kind="damage",
            element="fire",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Fire spell damage."
        ),
        "blizzard": MSBFSkill(
            "blizzard",
            "Blizzard",
            cost=9,
            kind="damage",
            element="ice",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Ice spell damage."
        ),
        "thunder": MSBFSkill(
            "thunder",
            "Thunder",
            cost=9,
            kind="damage",
            element="lightning",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Lightning spell damage."
        ),
        "aero": MSBFSkill(
            "aero",
            "Aero",
            cost=11,
            kind="true_damage",
            element="wind",
            power=128,
            stat="offense",
            accuracy=0.96,
            crit=0.08,
            description="Wind true damage that ignores defense, but still checks affinities."
        ),
        "flare": MSBFSkill(
            "flare",
            "Flare",
            cost=22,
            kind="damage",
            element="fire",
            power=190,
            stat="magic",
            accuracy=0.94,
            crit=0.04,
            description="Expensive heavy fire spell damage."
        ),
        "scan": MSBFSkill(
            "scan",
            "Scan",
            cost=3,
            kind="analyze",
            element="support",
            description="Reveals affinities in phase 1. In phase 2, reads Matsuda's moveset instead."
        ),
        "aqua_breath": MSBFSkill(
            "aqua_breath",
            "Aqua Breath",
            cost=13,
            kind="damage",
            element="ice",
            power=138,
            stat="magic",
            accuracy=0.95,
            crit=0.04,
            description="Enemy skill: ice breath damage."
        ),
        "white_wind": MSBFSkill(
            "white_wind",
            "White Wind",
            cost=22,
            kind="white_wind",
            element="healing",
            power=0,
            stat="magic",
            target="party",
            description="Enemy skill: party healing based on Kotonoha's current HP."
        ),
        "thousand_needles": MSBFSkill(
            "thousand_needles",
            "1000 Needles",
            cost=18,
            kind="fixed_damage",
            element="almighty",
            power=260,
            accuracy=1.0,
            description="Enemy skill: fixed damage that ignores defense and affinities."
        ),
        "mighty_guard": MSBFSkill(
            "mighty_guard",
            "Mighty Guard",
            cost=24,
            kind="blue_guard",
            element="support",
            target="party",
            description="Enemy skill: raises party defense and guards everyone this turn."
        ),
        "bad_breath": MSBFSkill(
            "bad_breath",
            "Bad Breath",
            cost=16,
            kind="blue_debuff",
            element="support",
            description="Enemy skill: lowers Matsuda's attack, defense, and agility."
        ),
        "needle_shot": MSBFSkill(
            "needle_shot",
            "Needle Shot",
            cost=8,
            kind="damage",
            element="pierce",
            power=140,
            accuracy=0.97,
            crit=0.17,
            description="Precise pierce damage."
        ),
        "armor_piercer": MSBFSkill(
            "armor_piercer",
            "Armor Piercer",
            cost=16,
            kind="damage",
            element="pierce",
            power=188,
            accuracy=0.92,
            crit=0.20,
            description="Heavy pierce damage with high critical rate."
        ),
        "wild_swing": MSBFSkill(
            "wild_swing",
            "Wild Swing",
            cost=8,
            kind="damage",
            element="slash",
            power=170,
            accuracy=0.84,
            crit=0.32,
            description="Unstable slash damage with high critical rate."
        ),
        "reckless_blow": MSBFSkill(
            "reckless_blow",
            "Reckless Blow",
            cost=14,
            kind="damage",
            element="slash",
            power=240,
            accuracy=0.89,
            crit=0.22,
            recoil=0.10,
            description="Heavy slash damage. Costs HP after use."
        ),
        "war_cry": MSBFSkill(
            "war_cry",
            "War Cry",
            cost=12,
            kind="buff_attack_all",
            element="support",
            target="party",
            description="Raises party attack and draws attention."
        ),
        "cure": MSBFSkill(
            "cure",
            "Cure",
            cost=7,
            kind="heal",
            element="healing",
            power=170,
            stat="magic",
            target="ally",
            description="Restores HP to one wounded ally."
        ),
        "cura": MSBFSkill(
            "cura",
            "Cura",
            cost=14,
            kind="heal",
            element="healing",
            power=290,
            stat="magic",
            target="ally",
            description="Restores a large amount of HP to one ally."
        ),
        "medica": MSBFSkill(
            "medica",
            "Medica",
            cost=18,
            kind="heal_all",
            element="healing",
            power=150,
            stat="magic",
            target="party",
            description="Restores HP to all allies."
        ),
        "raise": MSBFSkill(
            "raise",
            "Raise",
            cost=20,
            kind="revive",
            element="healing",
            power=0,
            stat="magic",
            target="ally",
            description="Revives one downed ally with partial HP."
        ),
        "protect": MSBFSkill(
            "protect",
            "Protect",
            cost=10,
            kind="buff_defense_all",
            element="support",
            target="party",
            description="Raises party defense."
        ),
        "haste": MSBFSkill(
            "haste",
            "Haste",
            cost=13,
            kind="haste",
            element="support",
            target="party",
            description="Raises party agility. Once before Matsuda changes rhythm, steals one half-turn."
        ),
        "deprotect": MSBFSkill(
            "deprotect",
            "Deprotect",
            cost=11,
            kind="debuff_defense",
            element="support",
            description="Lowers Matsuda's defense."
        ),
        "slow": MSBFSkill(
            "slow",
            "Slow",
            cost=11,
            kind="debuff_attack",
            element="support",
            description="Lowers Matsuda's attack."
        ),
        "hexline": MSBFSkill(
            "hexline",
            "Hexline",
            cost=11,
            kind="damage",
            element="psychic",
            power=132,
            stat="magic",
            accuracy=0.95,
            crit=0.08,
            description="Psychic damage."
        ),
        "guard": MSBFSkill(
            "guard",
            "Guard",
            kind="guard",
            element="support",
            description="Reduces incoming damage until the enemy turn ends."
        ),
        "boss_slash": MSBFSkill(
            "boss_slash",
            "Crosscut",
            kind="damage",
            element="slash",
            power=92,
            accuracy=0.95,
            crit=0.08
        ),
        "boss_pierce": MSBFSkill(
            "boss_pierce",
            "Line Breaker",
            kind="damage",
            element="pierce",
            power=98,
            accuracy=0.94,
            crit=0.10
        ),
        "boss_fira": MSBFSkill(
            "boss_fira",
            "Fira",
            cost=0,
            kind="damage",
            element="fire",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_blizzara": MSBFSkill(
            "boss_blizzara",
            "Blizzara",
            cost=0,
            kind="damage",
            element="ice",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_thundara": MSBFSkill(
            "boss_thundara",
            "Thundara",
            cost=0,
            kind="damage",
            element="lightning",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_firaga": MSBFSkill(
            "boss_firaga",
            "Firaga",
            cost=0,
            kind="damage",
            element="fire",
            power=130,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_blizzaga": MSBFSkill(
            "boss_blizzaga",
            "Blizzaga",
            cost=0,
            kind="damage",
            element="ice",
            power=130,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_thundaga": MSBFSkill(
            "boss_thundaga",
            "Thundaga",
            cost=0,
            kind="damage",
            element="lightning",
            power=130,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_aeroga": MSBFSkill(
            "boss_aeroga",
            "Aeroga",
            cost=0,
            kind="damage",
            element="wind",
            power=84,
            target="all",
            stat="magic",
            accuracy=0.91,
            crit=0.04
        ),
        "boss_sweep": MSBFSkill(
            "boss_sweep",
            "Redline Sweep",
            kind="damage",
            element="wind",
            power=62,
            target="all",
            stat="magic",
            accuracy=0.88,
            crit=0.03
        ),
        "boss_focus": MSBFSkill(
            "boss_focus",
            "Limit Read",
            kind="focus",
            element="support"
        ),
        "boss_guard": MSBFSkill(
            "boss_guard",
            "Null Aegis",
            kind="boss_guard",
            element="support",
            target="self"
        ),
        "boss_second_wind": MSBFSkill(
            "boss_second_wind",
            "Second Wind",
            kind="heal",
            element="healing",
            power=240,
            target="self"
        ),
        "boss_curtain_script": MSBFSkill(
            "boss_curtain_script",
            "Curtain Script",
            kind="phase3_curtain",
            element="wind",
            power=58,
            target="all",
            stat="magic",
            accuracy=0.93,
            crit=0.04
        ),
        "boss_black_box_waltz": MSBFSkill(
            "boss_black_box_waltz",
            "Black Box Waltz",
            kind="phase3_black_box",
            element="psychic",
            power=46,
            target="all",
            stat="magic",
            accuracy=0.96,
            crit=0.02
        ),
        "boss_reticle_nightmare": MSBFSkill(
            "boss_reticle_nightmare",
            "Reticle Nightmare",
            kind="phase3_reticle",
            element="pierce",
            power=142,
            accuracy=0.96,
            crit=0.18
        ),
        "boss_identity_null": MSBFSkill(
            "boss_identity_null",
            "Identity Null",
            kind="phase3_null",
            element="almighty",
            power=76,
            target="all",
            stat="magic",
            accuracy=1.0,
            crit=0.0
        ),
    }

    MSBF_ROSTER = [
        {
            "id": "seeker",
            "name": "Seeker",
            "role": "Spellblade",
            "summary": "All-rounder, jack-of-all-trades.",
            "max_hp": 560,
            "max_mp": 60,
            "offense": 60,
            "magic": 48,
            "defense": 50,
            "agility": 52,
            "attack_element": "slash",
            "weaknesses": [],
            "resists": [],
            "skills": ["attack", "scan", "ruin_edge", "fire", "blizzard", "thunder", "cure", "guard"],
        },
        {
            "id": "monika",
            "name": "Monika",
            "role": "Black Mage",
            "summary": "Best elemental burst and quick reads.",
            "max_hp": 400,
            "max_mp": 88,
            "offense": 32,
            "magic": 80,
            "defense": 30,
            "agility": 48,
            "attack_element": "slash",
            "weaknesses": ["pierce", "wind"],
            "resists": ["fire"],
            "skills": ["attack", "scan", "fire", "blizzard", "thunder", "flare", "hexline", "guard"],
        },
        {
            "id": "kotonoha",
            "name": "Kotonoha",
            "role": "Blue Mage",
            "summary": "Enemy skills and light utility.",
            "max_hp": 500,
            "max_mp": 82,
            "offense": 42,
            "magic": 66,
            "defense": 44,
            "agility": 56,
            "attack_element": "slash",
            "weaknesses": ["lightning"],
            "resists": ["psychic"],
            "skills": ["attack", "scan", "aqua_breath", "white_wind", "thousand_needles", "mighty_guard", "bad_breath", "guard"],
        },
        {
            "id": "asahina",
            "name": "Asahina",
            "role": "Halberdier",
            "summary": "Pierce damage and speed control.",
            "max_hp": 500,
            "max_mp": 62,
            "offense": 76,
            "magic": 28,
            "defense": 42,
            "agility": 74,
            "attack_element": "pierce",
            "weaknesses": ["fire"],
            "resists": ["pierce"],
            "skills": ["attackpierce", "needle_shot", "armor_piercer", "aero", "focus", "haste", "slow", "guard"],
        },
        {
            "id": "sam",
            "name": "Sam",
            "role": "Berserker",
            "summary": "Unrelenting strength and power.",
            "max_hp": 700,
            "max_mp": 50,
            "offense": 90,
            "magic": 22,
            "defense": 48,
            "agility": 34,
            "attack_element": "slash",
            "weaknesses": ["ice"],
            "resists": ["slash"],
            "skills": ["attack", "wild_swing", "reckless_blow", "war_cry", "focus", "ruin_edge", "deprotect", "guard"],
        },
        {
            "id": "tsubaki",
            "name": "Tsubaki",
            "role": "White Mage",
            "summary": "The primary healer.",
            "max_hp": 460,
            "max_mp": 112,
            "offense": 30,
            "magic": 76,
            "defense": 42,
            "agility": 44,
            "attack_element": "slash",
            "weaknesses": ["slash"],
            "resists": ["ice"],
            "skills": ["attack", "cure", "cura", "raise", "medica", "protect", "haste", "guard"],
        },
        {
            "id": "himeko",
            "name": "Himeko",
            "role": "Trickster",
            "summary": "Fast Scan, Haste, debuffs, and psychic burst.",
            "max_hp": 430,
            "max_mp": 76,
            "offense": 38,
            "magic": 62,
            "defense": 34,
            "agility": 76,
            "attack_element": "slash",
            "weaknesses": ["fire", "slash"],
            "resists": ["psychic"],
            "skills": ["attack", "scan", "haste", "deprotect", "slow", "hexline", "focus", "guard"],
        },
    ]

    MSBF_ROSTER_BY_ID = dict((entry["id"], entry) for entry in MSBF_ROSTER)
    MSBF_ALL_MEMBER_IDS = [entry["id"] for entry in MSBF_ROSTER]

    def msbf_bar_width(value, max_value, width):
        if max_value <= 0:
            return 0
        ratio = max(0.0, min(1.0, float(value) / float(max_value)))
        return int(width * ratio)

    def msbf_scroll_adjustment_to_bottom(adjustment):
        try:
            adjustment.change(adjustment.range)
        except Exception:
            pass

    def msbf_affinity_label(elements):
        if not elements:
            return "None"
        return ", ".join(MSBF_AFFINITY_NAMES.get(element, element.title()) for element in elements)

    def msbf_row_label(row):
        return "Front" if row == "front" else "Rear"

    def msbf_default_rows(member_ids):
        rows = {}
        for idx, member_id in enumerate(member_ids):
            rows[member_id] = "front" if idx < 2 else "rear"
        return rows

    def msbf_front_count(member_ids, rows):
        return sum(1 for member_id in member_ids if rows.get(member_id, "front") == "front")

    def msbf_select_member(picks, rows, member_id):
        picks = list(picks)
        rows = dict(rows)
        if member_id in picks:
            picks.remove(member_id)
            rows.pop(member_id, None)
        elif len(picks) < 4:
            picks.append(member_id)
            rows[member_id] = "front" if msbf_front_count(picks, rows) < 2 else "rear"
        return picks, rows

    def msbf_remove_member(picks, rows, member_id):
        picks = list(picks)
        rows = dict(rows)
        if member_id in picks:
            picks.remove(member_id)
            rows.pop(member_id, None)
        return picks, rows

    def msbf_toggle_row(picks, rows, member_id):
        rows = dict(rows)
        current = rows.get(member_id, "front")
        if current == "front":
            rows[member_id] = "rear"
        else:
            rows[member_id] = "front"
        return rows

    def msbf_can_begin(picks, rows):
        return len(picks) == 4 and msbf_front_count(picks, rows) >= 1

    def msbf_party_config(member_ids, rows):
        return {
            "members": list(member_ids),
            "rows": dict(rows),
        }

    def msbf_make_party(member_ids, rows=None):
        rows = rows or msbf_default_rows(member_ids)
        party = []
        for member_id in member_ids:
            entry = MSBF_ROSTER_BY_ID[member_id]
            combatant = MSBFCombatant(
                entry["id"],
                entry["name"],
                entry["max_hp"],
                entry["max_mp"],
                entry["offense"],
                entry["magic"],
                entry["defense"],
                entry["agility"],
                attack_element=entry["attack_element"],
                weaknesses=entry["weaknesses"],
                resists=entry["resists"],
                skills=entry["skills"]
            )
            combatant.role = entry["role"]
            combatant.row = rows.get(member_id, "front")
            party.append(combatant)
        return party

    def msbf_make_boss():
        return MSBFCombatant(
            "matsuda",
            "Matsuda, Crimson-Azure",
            40,
            999,
            68,
            70,
            50,
            54,
            attack_element="slash",
            weaknesses=["ice", "pierce"],
            resists=["fire"],
            skills=[]
        )

    def msbf_new_battle(member_config, id_mode=False):
        return MSBFBattleState(member_config, id_mode=id_mode)

    class MSBFBattleState(object):
        def __init__(self, member_config, id_mode=False):
            if isinstance(member_config, dict):
                member_ids = list(member_config.get("members", []))
                rows = dict(member_config.get("rows", {}))
            else:
                member_ids = list(member_config)
                rows = msbf_default_rows(member_ids)

            self.party = msbf_make_party(member_ids, rows)
            self.boss = msbf_make_boss()
            self.id_mode = bool(id_mode)
            self.phase = 1
            self.turn_phase = "setup"
            self.actor_index = 0
            self.press_turn_icons_state = []
            self.press_turn_fx_events = []
            self.press_turn_fx_serial = 0
            self.pending_half_turn = False
            self.haste_bonus_used_this_phase = False
            self.player_actions_this_phase = 0
            self.player_action_cap = MSBF_PLAYER_ACTION_CAP_MAX
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.enemy_action_cap = 4
            self.enemy_settling = False
            self.enemy_step_delay = 0.35
            self.round_number = 0
            self.result = None
            self.analyzed = False
            self.log = []
            self.log_serial = 0
            self.fx_event = None
            self.fx_serial = 0
            self.fx_clear_delay = 0.70
            self.final_victory_whiteout = False
            self.phase_transition_delay = 0.18
            self.player_element_history = []
            self.heal_actions = 0
            self.last_player_action = None
            self.last_turn_bonus_converted = False
            self.last_enemy_target_id = None
            self.phase2_scan_insight_bag = []
            self.phase1_affinity_bag = []
            self.phase1_affinity_index = self._draw_phase_one_affinity_index(None)
            self.phase2_affinity_signature = None
            self.phase2_last_affinity_shift_round = -1
            self.phase2_weakness_hits = {}
            self.phase2_ai_stance = "balanced"
            self.phase2_ai_last_announced_stance = "balanced"
            self.phase2_opening_immunity = False
            self.phase2_transition_reveal_started = False
            self.phase3_started = False
            self.phase3_vocal_started = False
            self.phase3_scan_insight_bag = []
            self.phase3_genre_shift_count = 0
            self.phase3_reinforcements_added = 0
            self.shmup_serial = 0
            self.shmup_tick = 0
            self.shmup_hits = 0
            self.shmup_invuln_until_tick = 0
            self.shmup_player_x = MSBF_SHMUP_STAGE_WIDTH // 2
            self.shmup_player_y = MSBF_SHMUP_STAGE_HEIGHT - 70
            self.shmup_bullets = []
            self.shmup_source_skill_id = None
            self.shmup_sfx_cooldowns = {}
            self.phase_transition_title = "THE STAGE BEGINS ANEW"
            self.phase_transition_subtitle = "A WINGED ANGEL REWRITES THE SCRIPT"
            self._reset_phase_two_player_read()
            if self.id_mode:
                self._configure_phase_two(restore_party=True)
                self.add_log("Id Mode skips the first bar. Tohu Imago is already awake.")
            else:
                self._set_phase_one_affinities(self.phase1_affinity_index)
            self.start_player_turn(initial=True)

        @property
        def boss_art(self):
            if self.phase == 1:
                return "msbf_matsuda_phase1"
            if self.phase == 3:
                return "msbf_matsuda_phase3"
            return "msbf_matsuda_phase2"

        @property
        def max_press_turns(self):
            alive_count = len(self.alive_party())
            return max(1, alive_count)

        @property
        def press_turn_icons(self):
            return list(self.press_turn_icons_state)

        @property
        def enemy_press_turn_icons(self):
            return list(self.enemy_press_turn_icons_state)

        @property
        def enemy_display_active(self):
            return self.enemy_phase_active or self.shmup_segment_active

        @property
        def active_press_turn_icons(self):
            if self.enemy_display_active:
                return self.enemy_press_turn_icons
            return self.press_turn_icons

        @property
        def active_actions_this_phase(self):
            if self.enemy_display_active:
                return self.enemy_actions_this_phase
            return self.player_actions_this_phase

        @property
        def active_action_cap(self):
            if self.enemy_display_active:
                return self.enemy_action_cap
            return self.player_action_cap

        @property
        def press_turn_label(self):
            if self.enemy_display_active:
                return "MATSUDA TURNS"
            return "PRESS TURNS"

        @property
        def press_turn_empty_label(self):
            if self.enemy_display_active:
                return "Tempo spent"
            return "Matsuda has tempo"

        @property
        def press_turns(self):
            return sum(2 if icon == "full" else 1 for icon in self.press_turn_icons_state)

        def _press_turn_fx_x(self, index):
            return MSBF_PRESS_TURN_ROW_X + (index * (MSBF_PRESS_TURN_SLOT_WIDTH + MSBF_PRESS_TURN_SLOT_SPACING))

        def _queue_press_turn_fx(self, side, kind, icon_type, index):
            if index is None:
                return

            icon_width = 36 if icon_type == "full" else 18
            icon_x = 2 if icon_type == "full" else int((MSBF_PRESS_TURN_SLOT_WIDTH - icon_width) / 2)
            self.press_turn_fx_serial += 1
            self.press_turn_fx_events.append({
                "serial": self.press_turn_fx_serial,
                "side": side,
                "kind": kind,
                "icon": icon_type,
                "index": index,
                "x": self._press_turn_fx_x(index),
                "width": icon_width,
                "icon_x": icon_x,
            })
            self.press_turn_fx_events = self.press_turn_fx_events[-6:]

        def clear_press_turn_fx(self):
            self.press_turn_fx_events = []

        @property
        def current_actor(self):
            if self.result or self.turn_phase != "player":
                return None
            for _i in range(len(self.party)):
                candidate = self.party[self.actor_index % len(self.party)]
                if candidate.alive:
                    return candidate
                self.actor_index += 1
            return None

        @property
        def enemy_phase_active(self):
            return self.turn_phase == "enemy" and not self.result

        @property
        def shmup_segment_active(self):
            return self.turn_phase == "shmup_segment" and not self.result

        @property
        def phase_transition_active(self):
            return self.turn_phase == "phase_transition" and not self.result

        @property
        def final_victory_active(self):
            return self.turn_phase == "victory_sequence" and not self.result

        @property
        def phase2_reveal_started(self):
            return bool(getattr(self, "phase2_transition_reveal_started", False))

        @property
        def active_actor_label(self):
            if self.result:
                return "Done"
            if self.turn_phase == "victory_sequence":
                return "Final Break"
            if self.turn_phase == "shmup_segment":
                return "Curtain Script"
            if self.turn_phase == "enemy":
                return "Matsuda"
            actor = self.current_actor
            if actor is None:
                return "Resolving"
            return actor.name

        def alive_party(self):
            return [member for member in self.party if member.alive]

        def defeated_party(self):
            return [member for member in self.party if not member.alive]

        def add_log(self, text):
            self.log.append(text)
            self.log_serial += 1
            if len(self.log) > 16:
                self.log = self.log[-16:]

        def clear_fx(self):
            self.fx_event = None
            self.fx_clear_delay = 0.70

        def set_fx(self, event_name, sfx_name=None, duration=None):
            self.fx_event = event_name
            self.fx_serial += 1
            if duration is None:
                duration = 1.45 if event_name == "phase" else 0.70
            self.fx_clear_delay = duration
            if sfx_name:
                self._play_sfx(sfx_name)

        def _play_sfx(self, sfx_name):
            path = MSBF_SFX.get(sfx_name)
            if not path:
                return
            try:
                renpy.sound.play(path, channel="sound")
                for layer_name, volume in MSBF_SFX_LAYERS.get(sfx_name, []):
                    layer_path = MSBF_SFX.get(layer_name)
                    if layer_path:
                        renpy.music.play("<volume %.2f>%s" % (volume, layer_path), channel="audio", loop=False)
            except Exception:
                pass

        def _play_phase_two_music(self):
            try:
                renpy.music.play(
                    "mod_assets/bgm/epicbattlephase2.ogg",
                    channel="music",
                    loop=True,
                    fadeout=1.0,
                    fadein=0.0
                )
            except Exception:
                pass

        def _set_phase_three_layer_volumes(self, instrumental_volume, vocal_volume, delay=0.0):
            try:
                renpy.music.set_volume(instrumental_volume, delay=delay, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
                renpy.music.set_volume(vocal_volume, delay=delay, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
            except Exception:
                pass

        def _play_phase_three_music(self, vocal=False):
            instrumental_volume = MSBF_IDMODE_PHASE3_INST_BED if vocal else 1.0
            self._set_phase_three_layer_volumes(instrumental_volume, 1.0 if vocal else 0.0)
            try:
                renpy.music.play(
                    MSBF_IDMODE_PHASE3_MUSIC_INST,
                    channel=MSBF_IDMODE_PHASE3_INST_CHANNEL,
                    loop=True,
                    fadeout=0.0,
                    fadein=0.0,
                    synchro_start=True
                )
                renpy.music.play(
                    MSBF_IDMODE_PHASE3_MUSIC_VOCAL,
                    channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL,
                    loop=True,
                    fadeout=0.0,
                    fadein=0.0,
                    synchro_start=True
                )
            except Exception:
                pass

        def _crossfade_phase_three_vocal(self):
            try:
                renpy.music.set_volume(1.0, delay=0.0, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
                renpy.music.set_volume(0.0, delay=0.0, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
                renpy.music.set_volume(1.0, delay=MSBF_IDMODE_PHASE3_VOCAL_FADEIN, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
                renpy.music.set_volume(MSBF_IDMODE_PHASE3_INST_BED, delay=MSBF_IDMODE_PHASE3_CROSSFADE, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
            except Exception:
                pass

        def _play_current_phase_music(self):
            if self.phase == 3:
                self._play_phase_three_music(self.phase3_vocal_started)
            else:
                self._play_phase_two_music()

        def _fade_out_phase_music(self):
            msbf_stop_battle_music(0.35)

        def begin_phase_two_reveal(self):
            if self.result or self.phase not in (2, 3) or self.turn_phase != "phase_transition":
                return
            if self.phase2_reveal_started:
                return
            self.phase2_transition_reveal_started = True
            self.fx_event = "phase"
            self.fx_serial += 1
            self.fx_clear_delay = 5.25
            self._play_current_phase_music()
            self._play_sfx("phase")
            renpy.restart_interaction()

        def start_player_turn(self, initial=False):
            if self.result:
                return
            self.clear_press_turn_fx()
            self.turn_phase = "player"
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.enemy_settling = False
            self.round_number += 1
            self.press_turn_icons_state = ["full"] * self.max_press_turns
            self.pending_half_turn = False
            self.haste_bonus_used_this_phase = False
            self.player_actions_this_phase = 0
            self.player_action_cap = min(MSBF_PLAYER_ACTION_CAP_MAX, (self.max_press_turns * 2) + 1)
            if self.phase >= 2:
                self.phase2_opening_immunity = False
                self._reset_phase_two_player_read()
            self.actor_index = self._first_alive_index()
            for member in self.party:
                member.guard = False
                member.taunt = False
            if self.boss.adapt_turns > 0 and not initial:
                self.boss.adapt_turns -= 1
                if self.boss.adapt_turns <= 0:
                    self.add_log("Matsuda's temporary guard drops.")
                    self.boss.adapt_element = None
            if initial:
                if self.id_mode and self.phase == 2:
                    self.add_log("Tohu Imago tears the opening credits away.")
                else:
                    self.add_log("Matsuda steps onto the setpiece.")
            else:
                self.add_log("Round %d Start." % (self.round_number))
                self._play_sfx("turn")

        def _first_alive_index(self):
            for idx, member in enumerate(self.party):
                if member.alive:
                    return idx
            return 0

        def can_use(self, skill):
            if self.turn_phase != "player":
                return False
            actor = self.current_actor
            if skill.kind == "revive" and not self.defeated_party():
                return False
            return actor is not None and actor.alive and actor.mp >= skill.cost

        def skill_needs_ally_target(self, skill):
            return skill.target == "ally" or skill.kind in ("heal", "revive")

        def valid_ally_targets(self, skill):
            if skill.kind == "revive":
                return self.defeated_party()
            return self.alive_party()

        def can_target(self, skill, target):
            if not self.skill_needs_ally_target(skill):
                return False
            if target is None:
                return False
            return target in self.valid_ally_targets(skill)

        def _has_press_turns(self):
            return len(self.press_turn_icons_state) > 0

        def _remove_icon(self, icon_type):
            if icon_type not in self.press_turn_icons_state:
                return False
            idx = self.press_turn_icons_state.index(icon_type)
            self.press_turn_icons_state.pop(idx)
            self._queue_press_turn_fx("player", "spend", icon_type, idx)
            return True

        def _convert_full_to_half(self):
            for idx, icon in enumerate(self.press_turn_icons_state):
                if icon == "full":
                    self.press_turn_icons_state[idx] = "half"
                    self._queue_press_turn_fx("player", "convert", "full", idx)
                    return True
            return False

        def _consume_half_priority(self):
            if self._remove_icon("half"):
                return True
            return self._remove_icon("full")

        def _consume_pass_turn(self):
            if self._remove_icon("half"):
                return
            self._convert_full_to_half()

        def _has_enemy_press_turns(self):
            return len(self.enemy_press_turn_icons_state) > 0

        def _remove_enemy_icon(self, icon_type):
            if icon_type not in self.enemy_press_turn_icons_state:
                return False
            idx = self.enemy_press_turn_icons_state.index(icon_type)
            self.enemy_press_turn_icons_state.pop(idx)
            self._queue_press_turn_fx("enemy", "spend", icon_type, idx)
            return True

        def _convert_enemy_full_to_half(self):
            for idx, icon in enumerate(self.enemy_press_turn_icons_state):
                if icon == "full":
                    self.enemy_press_turn_icons_state[idx] = "half"
                    self._queue_press_turn_fx("enemy", "convert", "full", idx)
                    return True
            return False

        def _consume_enemy_half_priority(self):
            if self._remove_enemy_icon("half"):
                return True
            return self._remove_enemy_icon("full")

        def _apply_player_turn_cost(self, outcome):
            self.last_turn_bonus_converted = False
            if outcome == "minor":
                self._consume_pass_turn()
                return

            if outcome in ("weak", "critical"):
                self.last_turn_bonus_converted = self._convert_full_to_half()
                if not self.last_turn_bonus_converted:
                    self._remove_icon("half")
                return

            self._consume_half_priority()

            if outcome == "resist" and self._has_press_turns():
                self._consume_half_priority()
                self.add_log("The resisted hit burns extra tempo.")

        def _apply_enemy_turn_cost(self, outcome):
            if outcome in ("weak", "critical"):
                if not self._convert_enemy_full_to_half():
                    self._remove_enemy_icon("half")
                return

            self._consume_enemy_half_priority()

            if outcome == "resist" and self._has_enemy_press_turns():
                self._consume_enemy_half_priority()
                self.add_log("The resisted hit burns Matsuda's tempo.")

        def _record_player_action(self):
            self.player_actions_this_phase += 1
            return self.player_actions_this_phase >= self.player_action_cap

        def _record_enemy_action(self):
            self.enemy_actions_this_phase += 1
            return self.enemy_actions_this_phase >= self.enemy_action_cap

        def _force_player_phase_limit(self):
            self.press_turn_icons_state = []
            self.add_log("Your side has reached the %d-action limit for this tempo cycle." % self.player_action_cap)

        def _force_enemy_phase_limit(self):
            self.enemy_press_turn_icons_state = []
            self.add_log("Matsuda hits the %d-action limit for this tempo cycle." % self.enemy_action_cap)

        def _finish_player_phase(self):
            self._restore_party_mp()
            self.start_enemy_phase()

        def _restore_member_mp(self, member, ratio):
            if member.max_mp <= 0 or member.mp >= member.max_mp:
                return 0
            restore_amount = max(1, int(member.max_mp * ratio))
            old_mp = member.mp
            member.mp = min(member.max_mp, member.mp + restore_amount)
            return member.mp - old_mp

        def _restore_party_mp(self):
            total_restored = 0
            for member in self.party:
                total_restored += self._restore_member_mp(member, 0.10)
            if total_restored > 0:
                self.add_log("The party catches its breath and recovers 10% MP.")
                self.set_fx("recover_mp", "recover")

        def _restore_party_for_phase_two(self):
            for member in self.party:
                member.hp = member.max_hp
                member.mp = member.max_mp
                member.guard = False
                member.taunt = False
                member.clamp()

        def _summon_full_roster_for_phase_three(self):
            current_ids = [member.id for member in self.party]
            missing_ids = [member_id for member_id in MSBF_ALL_MEMBER_IDS if member_id not in current_ids]
            if not missing_ids:
                return 0

            rows = dict((member.id, member.row) for member in self.party)
            for member_id in missing_ids:
                front_count = sum(1 for current_id in current_ids if rows.get(current_id, "front") == "front")
                rows[member_id] = "front" if front_count < 3 else "rear"
                current_ids.append(member_id)

            self.party.extend(msbf_make_party(missing_ids, rows))
            return len(missing_ids)

        def _phase_two_opening_immunity_active(self):
            return self.phase in (2, 3) and self.turn_phase in ("enemy", "shmup_segment") and bool(getattr(self, "phase2_opening_immunity", False))

        def _apply_enemy_damage_to_member(self, target, damage):
            if self._phase_two_opening_immunity_active() and target.hp > 0 and target.hp - damage <= 0:
                target.hp = 1
            else:
                target.hp -= damage
                target.clamp()

        def _reset_phase_two_player_read(self):
            self.phase2_player_actions_observed = 0
            self.phase2_player_turn_damage = 0
            self.phase2_player_aggression = 0.0
            self.phase2_player_defense = 0.0
            self.phase2_player_weak_hits = 0
            self.phase2_player_critical_hits = 0

        def _record_phase_two_player_action(self, actor, skill, outcome, damage_done):
            if self.phase not in (2, 3):
                return

            self.phase2_player_actions_observed += 1
            self.phase2_player_turn_damage += max(0, int(damage_done))

            if outcome == "critical":
                self.phase2_player_critical_hits += 1

            if skill is None:
                self.phase2_player_defense += 1.0
                return

            if skill.kind in ("damage", "true_damage", "fixed_damage"):
                self.phase2_player_aggression += 2.0
                damage_ratio = 0.0
                if self.boss.max_hp > 0:
                    damage_ratio = float(max(0, int(damage_done))) / float(self.boss.max_hp)
                if damage_ratio >= 0.14:
                    self.phase2_player_aggression += 1.8
                elif damage_ratio >= 0.08:
                    self.phase2_player_aggression += 1.0
                if outcome == "critical":
                    self.phase2_player_aggression += 0.6
                return

            if skill.kind in ("focus", "buff_attack_all", "debuff_defense", "haste"):
                self.phase2_player_aggression += 1.35
                return

            if skill.kind in ("heal_all", "white_wind", "revive", "blue_guard"):
                self.phase2_player_defense += 2.4
                return

            if skill.kind in ("heal", "guard", "buff_defense_all"):
                self.phase2_player_defense += 2.0
                return

            if skill.kind in ("debuff_attack", "blue_debuff"):
                self.phase2_player_defense += 1.6
                return

            if skill.kind == "analyze":
                self.phase2_player_defense += 0.5

        def _update_phase_two_ai_stance(self):
            if self.phase not in (2, 3) or self.phase2_player_actions_observed <= 0:
                self.phase2_ai_stance = "balanced"
                return

            damage_ratio = 0.0
            if self.boss.max_hp > 0:
                damage_ratio = float(self.phase2_player_turn_damage) / float(self.boss.max_hp)

            aggression = self.phase2_player_aggression + self.phase2_player_weak_hits * 0.8
            defense = self.phase2_player_defense
            next_stance = "balanced"
            if self.phase == 3 and (aggression >= defense + 1.2 or damage_ratio >= 0.10 or self.phase2_player_weak_hits >= 1):
                next_stance = "defensive"
            elif self.phase == 3 and (defense >= aggression + 1.4 or (defense >= 2.5 and damage_ratio < 0.08)):
                next_stance = "aggressive"
            elif aggression >= defense + 2.5 or damage_ratio >= 0.16 or self.phase2_player_weak_hits >= 2:
                next_stance = "defensive"
            elif defense >= aggression + 2.0 or (defense >= 3.5 and damage_ratio < 0.08):
                next_stance = "aggressive"

            if next_stance != self.phase2_ai_last_announced_stance:
                if next_stance == "defensive":
                    self.add_log("Matsuda reads the assault and folds into a defensive theorem.")
                elif next_stance == "aggressive":
                    self.add_log("Matsuda reads the stall and sharpens her killing line.")
                elif self.phase2_ai_last_announced_stance != "balanced":
                    self.add_log("Matsuda's read loosens as the party changes tempo.")
                self.phase2_ai_last_announced_stance = next_stance

            self.phase2_ai_stance = next_stance

        def _reset_phase_two_adaptation(self):
            self.phase2_weakness_hits = {}
            self.player_element_history = []
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0

        def _phase_two_affinity_signature(self, weaknesses, resists):
            return (tuple(sorted(weaknesses)), tuple(sorted(resists)))

        def _phase_affinity_counts(self):
            if self.phase == 3:
                return MSBF_PHASE3_WEAKNESS_COUNT, MSBF_PHASE3_RESIST_COUNT
            return MSBF_PHASE2_WEAKNESS_COUNT, MSBF_PHASE2_RESIST_COUNT

        def _draw_phase_two_affinities(self):
            previous = self.phase2_affinity_signature
            fallback = None
            weakness_count, resist_count = self._phase_affinity_counts()
            for _i in range(12):
                elements = list(MSBF_PHASE2_AFFINITY_ELEMENTS)
                random.shuffle(elements)
                weaknesses = sorted(elements[:weakness_count])
                resists = sorted(elements[weakness_count:weakness_count + resist_count])
                signature = self._phase_two_affinity_signature(weaknesses, resists)
                if fallback is None:
                    fallback = (weaknesses, resists, signature)
                if signature != previous:
                    return weaknesses, resists, signature
            return fallback

        def _set_phase_two_affinities(self, weaknesses, resists, signature=None):
            self.boss.weaknesses = list(weaknesses)
            self.boss.resists = list(resists)
            self.phase2_affinity_signature = signature or self._phase_two_affinity_signature(weaknesses, resists)
            self._reset_phase_two_adaptation()

        def _shuffle_phase_two_affinities(self, initial=False):
            if self.phase not in (2, 3):
                return
            weaknesses, resists, signature = self._draw_phase_two_affinities()
            self._set_phase_two_affinities(weaknesses, resists, signature)
            self.phase2_last_affinity_shift_round = self.round_number
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            if not initial:
                self.set_fx("shuffle", "shuffle")
                if self.phase == 3:
                    self.add_log("Imago Rupta ruptures its affinities. The read window collapses.")
                else:
                    self.add_log("Matsuda rewrites her hidden affinities. Her reads reset.")

        def finish_phase_transition(self):
            if self.result or self.turn_phase != "phase_transition":
                return
            if self.phase in (2, 3) and not self.phase2_reveal_started:
                self.begin_phase_two_reveal()
                return
            self.phase_transition_delay = 0.18
            self.start_enemy_phase()
            renpy.restart_interaction()

        def finish_final_victory(self):
            if self.result or self.turn_phase != "victory_sequence":
                return
            self.final_victory_whiteout = True
            self.clear_fx()
            self.result = "victory"
            renpy.restart_interaction()

        def player_pass(self):
            if self.result or self.turn_phase != "player":
                return
            actor = self.current_actor
            if actor is None:
                return
            self._consume_pass_turn()
            self._record_phase_two_player_action(actor, None, "minor", 0)
            limit_reached = self._record_player_action()
            self.add_log("%s passes and spends half a press turn." % actor.name)
            self.set_fx("pass", "pass")
            self.actor_index = (self.actor_index + 1) % len(self.party)
            if limit_reached and self._has_press_turns():
                self._force_player_phase_limit()
            if not self._has_press_turns():
                self._finish_player_phase()
            renpy.restart_interaction()

        def player_use_skill(self, skill, target=None):
            if self.result or self.turn_phase != "player":
                return
            actor = self.current_actor
            if actor is None:
                return
            if self.skill_needs_ally_target(skill) and not self.can_target(skill, target):
                self.add_log("%s needs a valid target." % skill.name)
                self._play_sfx("denied")
                renpy.restart_interaction()
                return
            if actor.mp < skill.cost:
                self.add_log("%s does not have enough MP." % actor.name)
                self._play_sfx("denied")
                renpy.restart_interaction()
                return

            actor.mp -= skill.cost
            actor.clamp()
            self.pending_half_turn = False
            boss_hp_before = self.boss.hp
            outcome = self._resolve_player_skill(actor, skill, target)
            self._record_phase_two_player_action(actor, skill, outcome, max(0, boss_hp_before - self.boss.hp))
            self._apply_player_turn_cost(outcome)
            if self.pending_half_turn:
                self.press_turn_icons_state.append("half")
                self._queue_press_turn_fx("player", "gain", "half", len(self.press_turn_icons_state) - 1)
                self.pending_half_turn = False
            limit_reached = self._record_player_action()
            self.last_player_action = skill.id

            if outcome in ("weak", "critical"):
                self._grant_player_bonus(outcome)

            if self.result:
                renpy.restart_interaction()
                return

            if self._handle_boss_phase_thresholds():
                renpy.restart_interaction()
                return

            if self.boss.hp <= 0:
                self._handle_boss_bar_break()
                if self.result or self.phase_transition_active or self.final_victory_active:
                    renpy.restart_interaction()
                    return

            if not self.alive_party():
                self.result = "defeat"
                self.set_fx("defeat", "down")
                self.add_log("The party is down.")
                renpy.restart_interaction()
                return

            self.actor_index = (self.actor_index + 1) % len(self.party)
            if limit_reached and self._has_press_turns():
                self._force_player_phase_limit()
            if not self._has_press_turns():
                self._finish_player_phase()

            renpy.restart_interaction()

        def _resolve_player_skill(self, actor, skill, target=None):
            if skill.kind == "guard":
                actor.guard = True
                recovered = self._restore_member_mp(actor, 0.10)
                if recovered > 0:
                    self.add_log("%s guards and recovers %d MP." % (actor.name, recovered))
                else:
                    self.add_log("%s guards." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "focus":
                actor.focus = True
                self.add_log("%s focuses for the next strike." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "analyze":
                if self.phase >= 2:
                    if self.phase == 3:
                        self.add_log("%s scans, but Imago Rupta answers in overlapping genres." % actor.name)
                    else:
                        self.add_log("%s scans, but Matsuda's new form returns only static." % actor.name)
                    self.add_log(self._phase_two_scan_insight())
                    self.set_fx("scan", "scan")
                    return "minor"

                self.analyzed = True
                self.add_log("Scan: Weak to %s. Resists %s." % (
                    msbf_affinity_label(self.boss.weaknesses),
                    msbf_affinity_label(self.boss.resists)
                ))
                self.set_fx("scan", "scan")
                return "minor"

            if skill.kind == "heal":
                if target is None:
                    target = self._lowest_wounded_ally()
                amount = self._healing_amount(actor, skill)
                target.hp += amount
                target.clamp()
                self.heal_actions += 1
                self.add_log("%s casts %s. %s recovers %d HP." % (actor.name, skill.name, target.name, amount))
                self.set_fx("heal", "heal")
                return "normal"

            if skill.kind == "heal_all":
                amount = self._healing_amount(actor, skill)
                for member in self.alive_party():
                    member.hp += amount
                    member.clamp()
                self.heal_actions += 1
                self.add_log("%s casts %s. The party recovers %d HP." % (actor.name, skill.name, amount))
                self.set_fx("heal", "heal")
                return "normal"

            if skill.kind == "white_wind":
                amount = self._white_wind_amount(actor)
                for member in self.alive_party():
                    member.hp += amount
                    member.clamp()
                self.heal_actions += 1
                self.add_log("%s calls White Wind. The party recovers %d HP from her borrowed life force." % (actor.name, amount))
                self.set_fx("heal", "heal")
                return "normal"

            if skill.kind == "revive":
                if target is None:
                    target = self._first_defeated_ally()
                if target is None:
                    self.add_log("%s casts %s, but nobody is down." % (actor.name, skill.name))
                    self.set_fx("miss", "denied")
                    return "normal"
                revive_amount = max(1, int(target.max_hp * 0.35 + actor.magic * 0.75))
                target.hp = min(target.max_hp, revive_amount)
                target.guard = True
                target.clamp()
                self.heal_actions += 1
                self.add_log("%s casts %s. %s gets back up with %d HP." % (actor.name, skill.name, target.name, target.hp))
                self.set_fx("revive", "revive")
                return "normal"

            if skill.kind == "buff_attack_all":
                for member in self.alive_party():
                    member.atk_stage += 1
                    member.clamp()
                actor.taunt = True
                self.add_log("%s uses War Cry. Attack rises, and Matsuda notices." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "buff_defense_all":
                for member in self.alive_party():
                    member.def_stage += 1
                    member.clamp()
                self.add_log("%s casts Protect. Defense rises." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "blue_guard":
                for member in self.alive_party():
                    member.def_stage += 1
                    member.guard = True
                    member.clamp()
                self.add_log("%s mimics Mighty Guard. The party braces behind monster magic." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "haste":
                for member in self.alive_party():
                    member.agi_stage += 1
                    member.clamp()
                if self.haste_bonus_used_this_phase:
                    self.add_log("%s casts Haste. Agility rises, but the tempo boost is already spent." % actor.name)
                else:
                    self.pending_half_turn = True
                    self.haste_bonus_used_this_phase = True
                    self.add_log("%s casts Haste. Agility rises, and the party steals one half-turn." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "debuff_defense":
                self.boss.def_stage -= 1
                self.boss.clamp()
                self.add_log("%s casts Deprotect. Matsuda's defense falls." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "debuff_attack":
                self.boss.atk_stage -= 1
                self.boss.clamp()
                self.add_log("%s casts Slow. Matsuda's offense slips." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "blue_debuff":
                self.boss.atk_stage -= 1
                self.boss.def_stage -= 1
                self.boss.agi_stage -= 1
                self.boss.clamp()
                self.add_log("%s exhales Bad Breath. Matsuda's stance, guard, and timing all foul up." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "fixed_damage":
                return self._fixed_damage_boss(actor, skill)

            if skill.kind == "true_damage":
                element = self._actual_element(actor, skill)
                self._track_player_element(element)
                return self._true_damage_boss(actor, skill, element)

            if skill.kind == "damage":
                element = self._actual_element(actor, skill)
                self._track_player_element(element)
                return self._damage_boss(actor, skill, element)

            return "normal"

        def _fixed_damage_boss(self, actor, skill):
            damage = max(1, int(skill.power))
            self.boss.hp -= damage
            self.boss.clamp()
            self.add_log("%s uses %s for %d fixed damage." % (actor.name, skill.name, damage))
            self.set_fx("hit", "hit")
            return "normal"

        def _true_damage_boss(self, actor, skill, element):
            if random.random() > self._hit_chance(actor, self.boss, skill):
                self.add_log("%s uses %s, but Matsuda slips it." % (actor.name, skill.name))
                self.set_fx("miss", "miss")
                return "miss"

            affinity = self._boss_affinity(element)
            critical = random.random() < self._crit_chance(actor, self.boss, skill)
            damage = self._true_damage_amount(actor, skill, critical, affinity)
            self.boss.hp -= damage
            self.boss.clamp()

            prefix = "%s uses %s for %d true damage." % (actor.name, skill.name, damage)
            if affinity == "weak":
                prefix += " Weakness hit."
            elif affinity == "resist":
                prefix += " Matsuda resists."
            if critical:
                prefix += " Critical."
            self.add_log(prefix)
            self._track_phase_two_weakness_hit(element, affinity)
            if critical:
                self.set_fx("crit", "crit")
            elif affinity == "weak":
                self.set_fx("weak", "weak")
            elif affinity == "resist":
                self.set_fx("resist", "resist")
            else:
                self.set_fx("hit", "hit")
            return "critical" if critical else affinity

        def _damage_boss(self, actor, skill, element):
            if random.random() > self._hit_chance(actor, self.boss, skill):
                self.add_log("%s uses %s, but Matsuda slips it." % (actor.name, skill.name))
                self.set_fx("miss", "miss")
                return "miss"

            affinity = self._boss_affinity(element)
            critical = random.random() < self._crit_chance(actor, self.boss, skill)
            damage = self._damage_amount(actor, self.boss, skill, element, critical, affinity)
            self.boss.hp -= damage
            self.boss.clamp()

            if skill.recoil > 0.0:
                recoil_damage = max(1, int(actor.max_hp * skill.recoil))
                actor.hp -= recoil_damage
                actor.clamp()

            prefix = "%s uses %s for %d damage." % (actor.name, skill.name, damage)
            if affinity == "weak":
                prefix += " Weakness hit."
            elif affinity == "resist":
                prefix += " Matsuda resists."
            if critical:
                prefix += " Critical."
            if skill.recoil > 0.0:
                prefix += " %s takes recoil." % actor.name
            self.add_log(prefix)
            self._track_phase_two_weakness_hit(element, affinity)
            if critical:
                self.set_fx("crit", "crit")
            elif affinity == "weak":
                self.set_fx("weak", "weak")
            elif affinity == "resist":
                self.set_fx("resist", "resist")
            else:
                self.set_fx("hit", "hit")
            return "critical" if critical else affinity

        def _track_player_element(self, element):
            if element in ("support", "healing", "almighty"):
                return
            self.player_element_history.append(element)
            if len(self.player_element_history) > 5:
                self.player_element_history = self.player_element_history[-5:]

        def _track_phase_two_weakness_hit(self, element, affinity):
            if self.phase not in (2, 3) or affinity != "weak":
                return
            self.phase2_player_weak_hits += 1
            if self.boss.adapt_turns > 0:
                return

            current_hits = self.phase2_weakness_hits.get(element, 0) + 1
            self.phase2_weakness_hits[element] = current_hits
            adapt_hits = MSBF_PHASE3_ADAPT_WEAK_HITS if self.phase == 3 else MSBF_PHASE2_ADAPT_WEAK_HITS
            if current_hits >= adapt_hits:
                self.phase2_weakness_hits[element] = 0
                self.boss.adapt_element = element
                self.boss.adapt_turns = 2
                if self.phase == 3:
                    self.add_log("Imago Rupta rejects the repeated %s script." % MSBF_AFFINITY_NAMES.get(element, element.title()))
                else:
                    self.add_log("Matsuda reads the repeated weakness and braces against %s." % MSBF_AFFINITY_NAMES.get(element, element.title()))

        def _boss_affinity(self, element):
            if element == "almighty":
                return "normal"
            if self.boss.adapt_element == element and self.boss.adapt_turns > 0:
                return "resist"
            if self.boss.guard and element in self.boss.weaknesses:
                return "normal"
            if element in self.boss.weaknesses:
                return "weak"
            if element in self.boss.resists:
                return "resist"
            return "normal"

        def _grant_player_bonus(self, reason):
            if not self.last_turn_bonus_converted:
                self.add_log("No full press turns remain, so the half-turn gets spent.")
                return
            if reason == "weak":
                self.add_log("The weakness hit converts the next full turn into a half turn.")
            else:
                self.add_log("The critical hit converts the next full turn into a half turn.")

        def _penalize_player_resist(self):
            pass

        def _configure_phase_two(self, restore_party=True):
            self.phase = 2
            self.boss.phase = 2
            self.boss.name = "Tohu Imago"
            self.boss.max_hp = max(40, int(self.boss.max_hp * 0.70))
            self.boss.hp = self.boss.max_hp
            self.boss.offense = 70
            self.boss.magic = 74
            self.boss.defense = 56
            self.boss.agility = 66
            self.boss.atk_stage = 0
            self.boss.def_stage = 0
            self.boss.agi_stage = 0
            self.boss.focus = True
            self.boss.guard = False
            self.boss.taunt = False
            self.boss.used_second_wind = False
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0
            if restore_party:
                self._restore_party_for_phase_two()
            self._shuffle_phase_two_affinities(initial=True)
            self.phase2_ai_stance = "balanced"
            self.phase2_ai_last_announced_stance = "balanced"
            self.phase2_opening_immunity = True
            self.phase2_transition_reveal_started = False
            self._reset_phase_two_player_read()
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            self.player_element_history = []

        def _begin_phase_two_transition(self):
            self._configure_phase_two(restore_party=True)
            self.phase_transition_title = "THE STAGE BEGINS ANEW"
            self.phase_transition_subtitle = "A WINGED ANGEL REWRITES THE SCRIPT"
            self.press_turn_icons_state = []
            self.enemy_press_turn_icons_state = []
            self.turn_phase = "phase_transition"
            self.phase_transition_delay = 0.12
            self._fade_out_phase_music()
            self.set_fx("phase_blackout", "explode", 5.0)
            self.add_log("Matsuda's guard breaks. Light floods the battlefield.")
            self.add_log("The party steadies itself as HP and MP surge to full.")
            self.add_log("Her rhythm snaps into a new pattern. Olden ways are futile.")

        def _configure_phase_three(self):
            self.phase = 3
            self.phase3_started = True
            self.phase3_vocal_started = False
            self.phase3_scan_insight_bag = []
            self.phase3_genre_shift_count = 0
            self.phase3_reinforcements_added = self._summon_full_roster_for_phase_three()
            self.boss.phase = 3
            self.boss.name = "Imago Rupta"
            self.boss.max_hp = 7600
            self.boss.hp = self.boss.max_hp
            self.boss.offense = 78
            self.boss.magic = 86
            self.boss.defense = 66
            self.boss.agility = 78
            self.boss.atk_stage = 1
            self.boss.def_stage = 0
            self.boss.agi_stage = 0
            self.boss.focus = True
            self.boss.guard = False
            self.boss.taunt = False
            self.boss.used_second_wind = True
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0
            self._restore_party_for_phase_two()
            self._shuffle_phase_two_affinities(initial=True)
            self.phase2_ai_stance = "aggressive"
            self.phase2_ai_last_announced_stance = "aggressive"
            self.phase2_opening_immunity = True
            self.phase2_transition_reveal_started = False
            self._reset_phase_two_player_read()
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            self.player_element_history = []

        def _begin_phase_three_transition(self):
            self._configure_phase_three()
            self.phase_transition_title = "IMAGO RUPTA"
            self.phase_transition_subtitle = "THE IMAGE RUPTURES AND THE SCRIPT CHANGES GENRE"
            self.press_turn_icons_state = []
            self.enemy_press_turn_icons_state = []
            self.clear_press_turn_fx()
            self.turn_phase = "phase_transition"
            self.phase_transition_delay = 0.10
            self._fade_out_phase_music()
            self.set_fx("phase_blackout", "explode", 5.1)
            self.add_log("Tohu Imago dies halfway through the sentence.")
            self.add_log("Matsuda grabs for another script. The image ruptures.")
            self.add_log("Imago Rupta enters Id Mode's final phase.")
            if self.phase3_reinforcements_added > 0:
                self.add_log("Every available ally forces their way onto the command deck.")

        def _handle_boss_phase_thresholds(self):
            if self.id_mode and self.phase == 2 and not self.phase3_started and self.boss.hp_ratio <= 0.50:
                self._begin_phase_three_transition()
                return True

            if self.id_mode and self.phase == 3 and not self.phase3_vocal_started and self.boss.hp > 0 and self.boss.hp_ratio <= 0.50:
                self.phase3_vocal_started = True
                self._crossfade_phase_three_vocal()
                self.add_log("Voices rupture even further.")
                self.set_fx("shuffle", "phase")

            return False

        def _handle_boss_bar_break(self):
            if self.phase == 1:
                self._begin_phase_two_transition()
            elif self.id_mode and self.phase == 2 and not self.phase3_started:
                self._begin_phase_three_transition()
            else:
                self.turn_phase = "victory_sequence"
                self.phase_transition_delay = 0.18
                self.press_turn_icons_state = []
                self.enemy_press_turn_icons_state = []
                self.clear_press_turn_fx()
                self._fade_out_phase_music()
                self.final_victory_whiteout = False
                self.set_fx("final_victory", "explode", 5.2)
                self.add_log("The killing blow lands.")
                if self.phase == 3:
                    self.add_log("Imago Rupta fails to find another genre to hide in.")
                    self.add_log("Matsuda's last script shatters.")
                else:
                    self.add_log("Tohu Imago fractures under the impact.")
                    self.add_log("Matsuda's last guard shatters.")

        def _set_phase_one_affinities(self, index):
            weaknesses, resists = MSBF_PHASE1_AFFINITY_SETS[index]
            self.phase1_affinity_index = index
            self.boss.weaknesses = list(weaknesses)
            self.boss.resists = list(resists)

        def _draw_phase_one_affinity_index(self, avoid_index=None):
            if len(MSBF_PHASE1_AFFINITY_SETS) <= 1:
                return 0
            if not self.phase1_affinity_bag:
                self.phase1_affinity_bag = list(range(len(MSBF_PHASE1_AFFINITY_SETS)))
                random.shuffle(self.phase1_affinity_bag)
                if avoid_index is not None and self.phase1_affinity_bag[-1] == avoid_index:
                    self.phase1_affinity_bag.insert(0, self.phase1_affinity_bag.pop())
            return self.phase1_affinity_bag.pop()

        def _shuffle_phase_one_affinities(self):
            if self.phase != 1:
                return
            next_index = self._draw_phase_one_affinity_index(self.phase1_affinity_index)
            self._set_phase_one_affinities(next_index)
            self.analyzed = False
            self.set_fx("shuffle", "shuffle")
            self.add_log("Matsuda shuffles her guard. Scan will find the new opening.")

        def _phase_two_scan_insight(self):
            if self.phase == 3:
                if not getattr(self, "phase3_scan_insight_bag", None):
                    self.phase3_scan_insight_bag = [
                        "Moveset read: Imago Rupta carries fewer openings, more resists, and adapts after repeated weakness hits faster than Tohu Imago.",
                        "Moveset read: Imago Rupta upgrades the phase 2 spell line into Firaga, Blizzaga, Thundaga, and Aeroga.",
                        "Moveset read: The full roster can act in phase 3, but the command deck still has a hard tempo limit.",
                        "Moveset read: Curtain Script briefly turns the fight into a bullet pattern. Guarding blunts the lane damage.",
                        "Moveset read: Black Box Waltz attacks the interface itself, burning MP and stripping stable buffs.",
                        "Moveset read: Reticle Nightmare marks a vulnerable target like a point-and-click escape room with no escape prompt.",
                        "Moveset read: Identity Null is almighty pressure. It gets worse when the party is over-buffed.",
                        "Moveset read: When this phase reaches half HP, the vocal layer enters and her action economy tightens."
                    ]
                    random.shuffle(self.phase3_scan_insight_bag)
                return self.phase3_scan_insight_bag.pop()

            if self.boss.focus:
                return "Moveset read: Limit Read is active. Matsuda's next damaging move will spend the charge."

            if not self.boss.used_second_wind and self.boss.hp_ratio < 0.45:
                return "Moveset read: Second Wind is primed. Pushing her below 38% HP will trigger one heal and attack boost."

            if self.phase2_ai_stance == "defensive":
                return "Moveset read: She is countering burst with Null Aegis. Change tempo before hitting the same line again."

            if self.phase2_ai_stance == "aggressive":
                return "Moveset read: She is punishing the stall with heavier weakness checks and Redline Sweep pressure."

            if not getattr(self, "phase2_scan_insight_bag", None):
                alive = self.alive_party()
                exploitable = []
                for skill_id in ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]:
                    skill = MSBF_SKILLS[skill_id]
                    if any(skill.element in member.weaknesses and not member.guard for member in alive):
                        exploitable.append(skill.name)

                self.phase2_scan_insight_bag = [
                    "Moveset read: Her phase 2 kit includes Crosscut, Line Breaker, Fira, Blizzara, Thundara, Redline Sweep, Limit Read, Null Aegis, and one Second Wind.",
                    "Moveset read: Redline Sweep is wind magic that pressures the whole party when at least three allies are standing.",
                    "Moveset read: Limit Read is a setup turn. It charges her next damaging action instead of dealing damage immediately.",
                    "Moveset read: She checks unguarded weaknesses before choosing a target, then falls back to a mixed physical and spell pool.",
                    "Moveset read: Second Wind can happen once when her HP drops below 38%. It heals and raises her attack.",
                    "Moveset read: Her phase 2 affinities keep rotating behind the static: three weaknesses, three resists, one neutral.",
                    "Moveset read: Her weakness-read counter resets whenever her hidden affinities rewrite."
                ]
                if exploitable:
                    names = ", ".join(sorted(set(exploitable)))
                    self.phase2_scan_insight_bag.append("Moveset read: She can currently exploit unguarded party weaknesses with %s." % names)
                random.shuffle(self.phase2_scan_insight_bag)

            return self.phase2_scan_insight_bag.pop()

        def start_enemy_phase(self):
            if self.result:
                return
            self.clear_press_turn_fx()
            if not self.alive_party():
                self.result = "defeat"
                return

            if self.phase >= 2:
                self._update_phase_two_ai_stance()
                self.boss.guard = False
            else:
                self.phase2_ai_stance = "balanced"

            self.turn_phase = "enemy"
            self.press_turn_icons_state = []
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            if self.phase == 3:
                self.enemy_press_turn_icons_state = ["full", "full", "full"] if self.phase3_vocal_started else ["full", "full", "half"]
            else:
                self.enemy_press_turn_icons_state = ["full", "full"]
            self.enemy_actions_this_phase = 0
            self.enemy_action_cap = (5 if self.phase3_vocal_started else 4) if self.phase == 3 else 4
            self.enemy_settling = False
            try:
                renpy.music.stop(channel="audio", fadeout=0.0)
            except Exception:
                pass
            self.set_fx("enemy", "turn_ready")
            if self.phase == 3:
                self.add_log("Imago Rupta seizes the wheel.")
            else:
                self.add_log("Matsuda takes the initiative.")

        def enemy_turn(self):
            self.start_enemy_phase()

        def advance_enemy_phase(self):
            if self.result or self.turn_phase != "enemy":
                return

            if not self.alive_party():
                self.result = "defeat"
                self.set_fx("defeat", "down")
                self.add_log("The party is down.")
                renpy.restart_interaction()
                return

            if self.enemy_settling or not self._has_enemy_press_turns() or self.enemy_actions_this_phase >= self.enemy_action_cap:
                self._finish_enemy_phase()
                renpy.restart_interaction()
                return

            skill = self._choose_boss_skill()
            outcome = self._resolve_enemy_skill(skill)
            if self.shmup_segment_active:
                renpy.restart_interaction()
                return
            self._apply_enemy_turn_cost(outcome)
            limit_reached = self._record_enemy_action()

            if not self.alive_party():
                self.result = "defeat"
                self.set_fx("defeat", "down")
                self.add_log("The party is down.")
                renpy.restart_interaction()
                return

            if limit_reached and self._has_enemy_press_turns():
                self._force_enemy_phase_limit()

            if not self._has_enemy_press_turns():
                self.enemy_settling = True

            renpy.restart_interaction()

        def _finish_enemy_phase(self):
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.phase2_opening_immunity = False
            for member in self.party:
                member.guard = False
                member.taunt = False

            if not self.alive_party():
                self.result = "defeat"
                self.set_fx("defeat", "down")
                self.add_log("The party is down.")
                return

            if self.phase == 1 and self.round_number % 2 == 0:
                self._shuffle_phase_one_affinities()
            elif self.phase == 2 and self.round_number - self.phase2_last_affinity_shift_round >= 2:
                self._shuffle_phase_two_affinities()
            elif self.phase == 3 and self.round_number - self.phase2_last_affinity_shift_round >= 1:
                self._shuffle_phase_two_affinities()
            self.start_player_turn()

        def _choose_boss_skill(self):
            if self.phase == 3:
                return self._choose_phase_three_skill()

            if self.phase == 2 and not self.boss.used_second_wind and self.boss.hp_ratio < 0.38:
                self.boss.used_second_wind = True
                return MSBF_SKILLS["boss_second_wind"]

            stance = self.phase2_ai_stance if self.phase == 2 else "balanced"
            if self.phase == 2 and stance == "defensive":
                if self.enemy_actions_this_phase == 0 and not self.boss.guard and random.random() < 0.72:
                    return MSBF_SKILLS["boss_guard"]
                if not self.boss.focus and random.random() < 0.24:
                    return MSBF_SKILLS["boss_focus"]
            elif self.phase == 2 and stance == "aggressive":
                if not self.boss.focus and random.random() < 0.30:
                    return MSBF_SKILLS["boss_focus"]
            elif self.phase == 2 and not self.boss.focus and random.random() < 0.18:
                return MSBF_SKILLS["boss_focus"]

            alive = self.alive_party()
            sweep_chance = 0.08 if self.phase == 1 else 0.14
            if self.phase == 2 and stance == "aggressive":
                sweep_chance = 0.24
            elif self.phase == 2 and stance == "defensive":
                sweep_chance = 0.08
            if len(alive) >= 3 and random.random() < sweep_chance:
                return MSBF_SKILLS["boss_sweep"]

            exploitable = []
            for skill_id in ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]:
                skill = MSBF_SKILLS[skill_id]
                if any(skill.element in member.weaknesses and not member.guard for member in alive):
                    exploitable.append(skill)

            exploit_chance = 0.22 if self.phase == 1 else 0.32
            if self.phase == 2 and stance == "aggressive":
                exploit_chance = 0.52
            elif self.phase == 2 and stance == "defensive":
                exploit_chance = 0.24
            if exploitable and random.random() < exploit_chance:
                return random.choice(exploitable)

            pool = ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]
            return MSBF_SKILLS[random.choice(pool)]

        def _choose_phase_three_skill(self):
            alive = self.alive_party()
            stance = self.phase2_ai_stance
            phase3_exploit_ids = ["boss_slash", "boss_pierce", "boss_firaga", "boss_blizzaga", "boss_thundaga", "boss_aeroga"]

            if not self.phase3_vocal_started and self.boss.hp_ratio <= 0.55 and random.random() < 0.18:
                return MSBF_SKILLS["boss_identity_null"]

            if self.phase3_vocal_started and random.random() < 0.18:
                return MSBF_SKILLS["boss_identity_null"]

            if stance == "defensive":
                if self.enemy_actions_this_phase == 0 and not self.boss.guard and random.random() < 0.40:
                    return MSBF_SKILLS["boss_guard"]
                if random.random() < 0.30:
                    return MSBF_SKILLS["boss_black_box_waltz"]
            elif stance == "aggressive":
                if not self.boss.focus and random.random() < 0.22:
                    return MSBF_SKILLS["boss_focus"]
                if random.random() < 0.30:
                    return MSBF_SKILLS["boss_reticle_nightmare"]

            if len(alive) >= 4 and random.random() < (0.28 if self.phase3_vocal_started else 0.18):
                return MSBF_SKILLS["boss_aeroga"]

            if len(alive) >= 3 and random.random() < (0.34 if self.phase3_vocal_started else 0.24):
                return MSBF_SKILLS["boss_curtain_script"]

            exploitable = []
            for skill_id in phase3_exploit_ids:
                skill = MSBF_SKILLS[skill_id]
                if any(skill.element in member.weaknesses and not member.guard for member in alive):
                    exploitable.append(skill)
            if exploitable and random.random() < (0.50 if self.phase3_vocal_started else 0.40):
                return random.choice(exploitable)

            pool = [
                "boss_slash",
                "boss_pierce",
                "boss_firaga",
                "boss_blizzaga",
                "boss_thundaga",
                "boss_aeroga",
                "boss_curtain_script",
                "boss_black_box_waltz",
                "boss_reticle_nightmare",
            ]
            return MSBF_SKILLS[random.choice(pool)]

        def _resolve_enemy_skill(self, skill):
            if skill.kind == "focus":
                self.boss.focus = True
                self.add_log("Matsuda uses Limit Read. Her next hit is charged.")
                self.set_fx("enemy_buff", "buff")
                return "normal"

            if skill.kind == "boss_guard":
                self.boss.guard = True
                if self.boss.def_stage < 2:
                    self.boss.def_stage += 1
                self.boss.clamp()
                self.add_log("Matsuda invokes Null Aegis. The next assault has to pierce a theorem.")
                self.set_fx("enemy_guard", "guard")
                return "normal"

            if skill.id == "boss_second_wind":
                heal_amount = 240 + (90 if self.phase == 2 else 0)
                self.boss.hp += heal_amount
                self.boss.atk_stage += 1
                self.boss.clamp()
                self.add_log("Matsuda catches a Second Wind and recovers %d HP." % heal_amount)
                self.set_fx("enemy_heal", "heal")
                return "normal"

            if skill.kind == "phase3_curtain":
                return self._resolve_phase_three_curtain(skill)

            if skill.kind == "phase3_black_box":
                return self._resolve_phase_three_black_box(skill)

            if skill.kind == "phase3_reticle":
                return self._resolve_phase_three_reticle(skill)

            if skill.kind == "phase3_null":
                return self._resolve_phase_three_null(skill)

            if skill.target == "all":
                best_outcome = "normal"
                total_damage = 0
                for member in list(self.alive_party()):
                    outcome, damage = self._damage_party_member(member, skill)
                    total_damage += damage
                    if outcome == "weak":
                        best_outcome = "weak"
                    elif outcome == "critical" and best_outcome != "weak":
                        best_outcome = "critical"
                self.add_log("Matsuda uses %s across the party for %d total damage." % (skill.name, total_damage))
                self.set_fx("enemy_aoe", "enemy")
                return best_outcome

            target = self._choose_enemy_target(skill)
            outcome, damage = self._damage_party_member(target, skill)
            self.last_enemy_target_id = target.id
            line = "Matsuda uses %s on %s for %d damage." % (skill.name, target.name, damage)
            if outcome == "weak":
                line += " Weakness hit."
            elif outcome == "resist":
                line += " %s resists." % target.name
            elif outcome == "critical":
                line += " Critical."
            elif outcome == "miss":
                line += " Miss."
            if not target.alive:
                line += " %s is down." % target.name
            self.add_log(line)
            if outcome == "weak":
                self.set_fx("enemy_weak", "weak")
            elif outcome == "critical":
                self.set_fx("enemy_crit", "crit")
            elif outcome == "resist":
                self.set_fx("enemy_resist", "resist")
            elif outcome == "miss":
                self.set_fx("miss", "miss")
            else:
                self.set_fx("enemy_hit", "enemy")
            return outcome

        def _resolve_phase_three_curtain(self, skill):
            self._start_phase_three_shmup(skill)
            return "minor"

        def _start_phase_three_shmup(self, skill):
            self.phase3_genre_shift_count += 1
            self.turn_phase = "shmup_segment"
            self.shmup_serial += 1
            self.shmup_tick = 0
            self.shmup_hits = 0
            self.shmup_invuln_until_tick = 0
            self.shmup_player_x = MSBF_SHMUP_STAGE_WIDTH // 2
            self.shmup_player_y = MSBF_SHMUP_STAGE_HEIGHT - 70
            self.shmup_bullets = []
            self.shmup_source_skill_id = skill.id
            self.shmup_sfx_cooldowns = {}
            self.add_log("Curtain Script compresses the fight into a bullet field.")
            self.set_fx("shuffle", "shuffle", 0.45)
            self._play_shmup_sfx("touhou_start", 0, 0.58)

        def shmup_nudge(self, dx, dy):
            if not self.shmup_segment_active:
                return
            radius = MSBF_SHMUP_PLAYER_RADIUS
            self.shmup_player_x = msbf_clamp(self.shmup_player_x + dx, radius, MSBF_SHMUP_STAGE_WIDTH - radius)
            self.shmup_player_y = msbf_clamp(self.shmup_player_y + dy, radius, MSBF_SHMUP_STAGE_HEIGHT - radius)
            self._check_shmup_collision()
            renpy.restart_interaction()

        def update_shmup_segment(self):
            if not self.shmup_segment_active:
                return

            try:
                mouse_x, mouse_y = renpy.get_mouse_pos()
                radius = MSBF_SHMUP_PLAYER_RADIUS
                target_x = msbf_clamp(mouse_x - MSBF_SHMUP_STAGE_X, radius, MSBF_SHMUP_STAGE_WIDTH - radius)
                target_y = msbf_clamp(mouse_y - MSBF_SHMUP_STAGE_Y, radius, MSBF_SHMUP_STAGE_HEIGHT - radius)
                if 0 <= mouse_x - MSBF_SHMUP_STAGE_X <= MSBF_SHMUP_STAGE_WIDTH and 0 <= mouse_y - MSBF_SHMUP_STAGE_Y <= MSBF_SHMUP_STAGE_HEIGHT:
                    self.shmup_player_x += (target_x - self.shmup_player_x) * 0.55
                    self.shmup_player_y += (target_y - self.shmup_player_y) * 0.55
            except Exception:
                pass

            self.shmup_tick += 1
            self._spawn_shmup_bullets()
            self._advance_shmup_bullets()

            if self._check_shmup_collision():
                return

            if self.shmup_tick >= MSBF_SHMUP_DURATION_TICKS:
                self.finish_phase_three_shmup(True)
                return

            renpy.restart_interaction()

        def _play_shmup_sfx(self, sfx_name, min_interval=6, volume=0.42):
            path = MSBF_SFX.get(sfx_name)
            if not path:
                return
            last_tick = self.shmup_sfx_cooldowns.get(sfx_name, -999)
            if self.shmup_tick - last_tick < min_interval:
                return
            self.shmup_sfx_cooldowns[sfx_name] = self.shmup_tick
            try:
                renpy.music.play("<volume %.2f>%s" % (volume, path), channel="audio", loop=False)
            except Exception:
                pass

        def _add_shmup_bullet(self, x, y, vx, vy, size=10, color="#ff3868dd", shape="orb", sway=0.0, phase=0.0, ax=0.0, ay=0.0, ttl=None):
            rot = 0.0
            if shape == "needle":
                rot = math.degrees(math.atan2(vy, vx)) + 90.0
            self.shmup_bullets.append({
                "x": float(x),
                "y": float(y),
                "vx": float(vx),
                "vy": float(vy),
                "size": int(size),
                "color": color,
                "shape": shape,
                "sway": float(sway),
                "phase": float(phase),
                "rot": rot,
                "age": 0,
                "ax": float(ax),
                "ay": float(ay),
                "ttl": ttl,
            })

        def _add_shmup_beam(self, x, y, w, h, vx, vy, color="#ff3868dd", arm_age=5, ttl=42):
            self.shmup_bullets.append({
                "x": float(x),
                "y": float(y),
                "vx": float(vx),
                "vy": float(vy),
                "size": int(max(w, h)),
                "w": int(w),
                "h": int(h),
                "color": color,
                "shape": "beam",
                "sway": 0.0,
                "phase": 0.0,
                "rot": 0.0,
                "age": 0,
                "ax": 0.0,
                "ay": 0.0,
                "ttl": int(ttl),
                "arm_age": int(arm_age),
            })

        def _add_shmup_radial_burst(self, x, y, count, speed, offset, color, size=9, gap_every=None, gap_shift=0, shape="orb", sway=0.0):
            for idx in range(count):
                if gap_every and (idx + gap_shift) % gap_every == 0:
                    continue
                angle = offset + (math.pi * 2.0 * idx / float(count))
                self._add_shmup_bullet(
                    x,
                    y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    size,
                    color,
                    shape,
                    sway,
                    idx * 0.37
                )

        def _spawn_shmup_bullets(self):
            tick = self.shmup_tick
            vocal = bool(getattr(self, "phase3_vocal_started", False))
            density_bonus = 1 if vocal else 0

            if tick % 6 == 0:
                lane_count = 8
                gap = (tick // 6 + self.phase3_genre_shift_count) % lane_count
                for lane in range(lane_count):
                    if lane == gap or lane == (gap + 1) % lane_count:
                        continue
                    x = 54 + lane * 96
                    self._add_shmup_bullet(
                        x,
                        -16,
                        math.sin((tick + lane * 11) * 0.20) * (0.48 + density_bonus * 0.10),
                        4.55 + density_bonus * 0.30,
                        8,
                        "#ff3868dd",
                        "orb",
                        0.025,
                        float(lane)
                    )
                self._play_shmup_sfx("touhou_shot", 10, 0.25)

            if tick >= 24 and tick % 14 == 3:
                origin_x = 48 + ((tick * 83) % (MSBF_SHMUP_STAGE_WIDTH - 96))
                origin_y = -20
                dx = self.shmup_player_x - origin_x
                dy = self.shmup_player_y - origin_y
                angle = math.atan2(dy, dx)
                offsets = [-0.24, 0.0, 0.24]
                if vocal:
                    offsets = [-0.32, -0.12, 0.12, 0.32]
                for offset in offsets:
                    speed = 4.55 + density_bonus * 0.28
                    self._add_shmup_bullet(
                        origin_x,
                        origin_y,
                        math.cos(angle + offset) * speed,
                        math.sin(angle + offset) * speed,
                        8,
                        "#f5fbffdd",
                        "needle",
                        0.0,
                        offset * 10.0
                    )
                self._play_shmup_sfx("touhou_needle", 14, 0.30)

            if tick >= 18 and tick % 22 == 0:
                count = 14 + density_bonus * 4
                speed = 2.95 + density_bonus * 0.24
                offset = tick * 0.19 + self.phase3_genre_shift_count * 0.38
                origin_x = MSBF_SHMUP_STAGE_WIDTH * (0.36 + 0.20 * math.sin(tick * 0.071))
                origin_y = 92 + 58 * math.sin(tick * 0.047)
                self._add_shmup_radial_burst(
                    origin_x,
                    origin_y,
                    count,
                    speed,
                    offset,
                    "#a66bffdd",
                    9,
                    gap_every=5,
                    gap_shift=(tick // 22) % 5,
                    shape="orb",
                    sway=0.08 + density_bonus * 0.03
                )
                self._play_shmup_sfx("touhou_burst", 18, 0.35)

            if tick >= 42 and tick % 30 == 15:
                count = 10 + density_bonus * 3
                offset = -tick * 0.13
                self._add_shmup_radial_burst(
                    MSBF_SHMUP_STAGE_WIDTH * 0.50,
                    MSBF_SHMUP_STAGE_HEIGHT * 0.48,
                    count,
                    3.15 + density_bonus * 0.18,
                    offset,
                    "#ffcf66dd",
                    8,
                    gap_every=5,
                    gap_shift=(tick // 9) % 5,
                    shape="needle",
                    sway=0.04
                )
                self._play_shmup_sfx("touhou_burst_alt", 22, 0.28)

            if tick % 16 == 8:
                row = (tick // 16) % 6
                y = 40 + row * 70
                wobble = 0.15 + density_bonus * 0.05
                self._add_shmup_bullet(-18, y, 4.95, 0.14, 8, "#55ddffdd", "orb", wobble, tick * 0.17)
                self._add_shmup_bullet(MSBF_SHMUP_STAGE_WIDTH + 18, y + 34, -4.95, -0.14, 8, "#ff6b9fdd", "orb", wobble, tick * 0.13)
                self._play_shmup_sfx("touhou_shot_alt", 14, 0.21)

            if tick >= 34 and tick % 22 == 11:
                base_x = msbf_clamp(self.shmup_player_x + math.sin(tick * 0.21) * 64, 42, MSBF_SHMUP_STAGE_WIDTH - 42)
                for idx, spread in enumerate([-1, 0, 1]):
                    self._add_shmup_bullet(
                        base_x + spread * 24,
                        MSBF_SHMUP_STAGE_HEIGHT + 18 + abs(spread) * 4,
                        spread * 0.44 + math.sin(tick * 0.11 + idx) * 0.20,
                        -4.55 - density_bonus * 0.22 + abs(spread) * 0.08,
                        8,
                        "#66e08add",
                        "orb",
                        0.07,
                        tick + idx,
                        ay=0.010
                    )
                self._play_shmup_sfx("touhou_graze", 24, 0.20)

            if tick >= 48 and tick % 44 == 22:
                lane_count = 11
                lane_spacing = float(MSBF_SHMUP_STAGE_WIDTH - 72) / float(lane_count - 1)
                gap = (tick // 44 + self.phase3_genre_shift_count) % (lane_count - 1)
                for lane in range(lane_count):
                    if lane == gap or lane == gap + 1:
                        continue
                    x = 36 + lane * lane_spacing
                    wave = math.sin(tick * 0.09 + lane * 0.73)
                    self._add_shmup_bullet(
                        x,
                        MSBF_SHMUP_STAGE_HEIGHT + 22,
                        wave * (0.42 + density_bonus * 0.06),
                        -3.35 - density_bonus * 0.18 - (lane % 3) * 0.07,
                        8,
                        "#ff3868dd",
                        "orb",
                        0.05,
                        tick + lane
                    )
                    if lane % 2 == (tick // 44) % 2:
                        self._add_shmup_bullet(
                            x + wave * 18,
                            MSBF_SHMUP_STAGE_HEIGHT + 54,
                            -wave * 0.32,
                            -3.05 - density_bonus * 0.16,
                            7,
                            "#ffcf66dd",
                            "orb",
                            0.04,
                            tick + lane * 2
                        )
                self._play_shmup_sfx("touhou_shot_alt", 24, 0.26)

            if tick >= 64 and tick % 52 == 26:
                side = -1 if (tick // 52) % 2 == 0 else 1
                x = -18 if side < 0 else MSBF_SHMUP_STAGE_WIDTH + 18
                vx = (4.15 + density_bonus * 0.18) * (-side)
                center_y = MSBF_SHMUP_STAGE_HEIGHT - 78 - ((tick * 17) % 156)
                gap = (tick // 52) % 6
                for idx, y_offset in enumerate([-72, -44, -16, 16, 44, 72]):
                    if idx == gap:
                        continue
                    y = msbf_clamp(center_y + y_offset, 34, MSBF_SHMUP_STAGE_HEIGHT - 34)
                    self._add_shmup_bullet(
                        x,
                        y,
                        vx,
                        math.sin(tick * 0.08 + idx * 0.65) * 0.34,
                        7,
                        "#55ddffdd",
                        "needle",
                        0.025,
                        tick + idx
                    )
                self._play_shmup_sfx("touhou_needle", 26, 0.28)

            if tick >= 56 and tick % 34 == 17:
                origin_y = MSBF_SHMUP_STAGE_HEIGHT + 24
                origin_x = 74 + ((tick * 61) % (MSBF_SHMUP_STAGE_WIDTH - 148))
                dx = self.shmup_player_x - origin_x
                dy = self.shmup_player_y - origin_y
                angle = math.atan2(dy, dx)
                for offset in [-0.22, 0.0, 0.22]:
                    speed = 4.10 + density_bonus * 0.22
                    self._add_shmup_bullet(origin_x, origin_y, math.cos(angle + offset) * speed, math.sin(angle + offset) * speed, 7, "#f5fbffdd", "needle", 0.0, tick + offset)

            if vocal and tick >= 72 and tick % 12 == 6:
                lane = (tick // 8) % 6
                x = 80 + lane * 124
                self._add_shmup_bullet(x, -18, -1.85, 4.95, 7, "#ffffffd8", "needle", 0.04, tick)
                self._add_shmup_bullet(MSBF_SHMUP_STAGE_WIDTH - x, -18, 1.85, 4.95, 7, "#ff3868d8", "needle", 0.04, tick + 3)

        def _advance_shmup_bullets(self):
            updated = []
            margin = 64
            for bullet in self.shmup_bullets:
                age = bullet.get("age", 0) + 1
                bullet["age"] = age
                ttl = bullet.get("ttl", None)
                if ttl is not None and age > ttl:
                    continue
                sway = bullet.get("sway", 0.0)
                phase = bullet.get("phase", 0.0)
                bullet["vx"] += bullet.get("ax", 0.0)
                bullet["vy"] += bullet.get("ay", 0.0)
                bullet["x"] += bullet.get("vx", 0.0) + math.sin((age + phase) * 0.20) * sway
                bullet["y"] += bullet.get("vy", 0.0)
                if bullet.get("shape") == "needle":
                    bullet["rot"] = math.degrees(math.atan2(bullet.get("vy", 0.0), bullet.get("vx", 0.0))) + 90.0
                if -margin <= bullet["x"] <= MSBF_SHMUP_STAGE_WIDTH + margin and -margin <= bullet["y"] <= MSBF_SHMUP_STAGE_HEIGHT + margin:
                    updated.append(bullet)
            self.shmup_bullets = updated[-MSBF_SHMUP_MAX_BULLETS:]

        def _check_shmup_collision(self):
            if not self.shmup_segment_active:
                return False
            if self.shmup_tick < MSBF_SHMUP_GRACE_TICKS:
                return False
            if self.shmup_tick < getattr(self, "shmup_invuln_until_tick", 0):
                return False
            player_radius = MSBF_SHMUP_PLAYER_RADIUS
            for bullet in self.shmup_bullets:
                if bullet.get("shape") == "beam":
                    if bullet.get("age", 0) < bullet.get("arm_age", 0):
                        continue
                    dx = abs(bullet.get("x", 0) - self.shmup_player_x)
                    dy = abs(bullet.get("y", 0) - self.shmup_player_y)
                    if dx <= (bullet.get("w", 0) * 0.5 + player_radius) and dy <= (bullet.get("h", 0) * 0.5 + player_radius):
                        return self._register_shmup_hit()
                    continue
                bullet_radius = bullet.get("size", 10) * (0.34 if bullet.get("shape") == "needle" else 0.42)
                dx = bullet.get("x", 0) - self.shmup_player_x
                dy = bullet.get("y", 0) - self.shmup_player_y
                hit_radius = player_radius + bullet_radius
                if dx * dx + dy * dy <= hit_radius * hit_radius:
                    return self._register_shmup_hit()
            return False

        def _register_shmup_hit(self):
            self.shmup_hits += 1
            self._play_shmup_sfx("touhou_hit", 0, 0.62)

            if self.shmup_hits >= MSBF_SHMUP_HIT_LIMIT:
                self.finish_phase_three_shmup(False)
                return True

            self.shmup_invuln_until_tick = self.shmup_tick + MSBF_SHMUP_HIT_INVULN_TICKS
            self._clear_shmup_pressure_near_player()
            self.add_log("Curtain Script clips the hitbox (%d/%d)." % (self.shmup_hits, MSBF_SHMUP_HIT_LIMIT))
            return False

        def _clear_shmup_pressure_near_player(self):
            radius_sq = MSBF_SHMUP_PANIC_CLEAR_RADIUS * MSBF_SHMUP_PANIC_CLEAR_RADIUS
            remaining = []
            for bullet in self.shmup_bullets:
                dx = bullet.get("x", 0.0) - self.shmup_player_x
                dy = bullet.get("y", 0.0) - self.shmup_player_y
                if bullet.get("shape") != "beam" and dx * dx + dy * dy <= radius_sq:
                    continue
                if bullet.get("shape") == "beam":
                    clear_x = bullet.get("w", 0) * 0.5 + MSBF_SHMUP_PANIC_CLEAR_RADIUS
                    clear_y = bullet.get("h", 0) * 0.5 + MSBF_SHMUP_PANIC_CLEAR_RADIUS
                    if abs(dx) <= clear_x and abs(dy) <= clear_y:
                        continue
                remaining.append(bullet)
            self.shmup_bullets = remaining

        def finish_phase_three_shmup(self, success):
            if not self.shmup_segment_active:
                return

            self.shmup_bullets = []
            self.turn_phase = "enemy"

            if success:
                base_damage = min(MSBF_SHMUP_SUCCESS_DAMAGE, max(90, int(self.boss.max_hp * 0.22)))
                damage = int(base_damage * max(0.55, 1.0 - self.shmup_hits * 0.16))
                old_hp = self.boss.hp
                self.boss.hp = max(0, self.boss.hp - damage)
                damage_done = old_hp - self.boss.hp
                if self.shmup_hits:
                    self.add_log("The party escapes Curtain Script with %d clip(s). Imago Rupta eats %d backlash damage." % (self.shmup_hits, damage_done))
                else:
                    self.add_log("The party slips through Curtain Script. Imago Rupta eats %d backlash damage." % damage_done)
                self._play_shmup_sfx("touhou_clear", 0, 0.58)
                self.set_fx("resist", "weak")
                outcome = "resist"

                if self.boss.hp <= 0:
                    self._record_enemy_action()
                    self._handle_boss_bar_break()
                    renpy.restart_interaction()
                    return

                if self._handle_boss_phase_thresholds():
                    renpy.restart_interaction()
                    return
            else:
                total_damage = 0
                for member in list(self.alive_party()):
                    damage = int(MSBF_SHMUP_FAILURE_DAMAGE + self.boss.magic * 0.35)
                    if member.guard:
                        damage = int(damage * 0.62)
                    self._apply_enemy_damage_to_member(member, damage)
                    total_damage += damage
                self.add_log("Curtain Script tags the hitbox. Identity Null splashes the party for %d total damage." % total_damage)
                self._play_shmup_sfx("touhou_down", 0, 0.60)
                self.set_fx("enemy_aoe", "enemy")
                outcome = "normal"

            self._apply_enemy_turn_cost(outcome)
            limit_reached = self._record_enemy_action()

            if not self.alive_party():
                self.result = "defeat"
                self.set_fx("defeat", "down")
                self.add_log("The party is down.")
                renpy.restart_interaction()
                return

            if limit_reached and self._has_enemy_press_turns():
                self._force_enemy_phase_limit()

            if not self._has_enemy_press_turns():
                self.enemy_settling = True

            renpy.restart_interaction()

        def _resolve_phase_three_black_box(self, skill):
            self.phase3_genre_shift_count += 1
            best_outcome = "normal"
            total_damage = 0
            mp_burn = 0
            for member in list(self.alive_party()):
                outcome, damage = self._damage_party_member(member, skill)
                total_damage += damage
                if member.mp > 0:
                    burn = max(3, int(member.max_mp * (0.10 if member.guard else 0.18)))
                    old_mp = member.mp
                    member.mp = max(0, member.mp - burn)
                    mp_burn += old_mp - member.mp
                if member.atk_stage > 0:
                    member.atk_stage -= 1
                if member.def_stage > 0 and not member.guard:
                    member.def_stage -= 1
                if member.agi_stage > 0 and not member.guard:
                    member.agi_stage -= 1
                member.clamp()
                if outcome == "weak":
                    best_outcome = "weak"
                elif outcome == "critical" and best_outcome != "weak":
                    best_outcome = "critical"
            self.add_log("Black Box Waltz corrupts the command deck for %d damage and %d MP." % (total_damage, mp_burn))
            self.set_fx("enemy_aoe", "debuff")
            return best_outcome

        def _resolve_phase_three_reticle(self, skill):
            self.phase3_genre_shift_count += 1
            alive = self.alive_party()
            if not alive:
                return "normal"

            healers = [member for member in alive if "cure" in member.skill_ids or "medica" in member.skill_ids or "white_wind" in member.skill_ids or "raise" in member.skill_ids]
            if healers and random.random() < 0.55:
                target = min(healers, key=lambda member: member.hp_ratio)
            else:
                target = min(alive, key=lambda member: member.hp_ratio)

            outcome, damage = self._damage_party_member(target, skill)
            if target.alive and not target.guard:
                target.def_stage -= 1
                target.agi_stage -= 1
                target.clamp()
            self.last_enemy_target_id = target.id

            line = "Reticle Nightmare paints %s for %d damage." % (target.name, damage)
            if outcome == "weak":
                line += " Weakness hit."
            elif outcome == "critical":
                line += " Critical."
            elif outcome == "miss":
                line += " Miss."
            if not target.alive:
                line += " %s is down." % target.name
            self.add_log(line)
            if outcome == "critical":
                self.set_fx("enemy_crit", "crit")
            elif outcome == "weak":
                self.set_fx("enemy_weak", "weak")
            elif outcome == "miss":
                self.set_fx("miss", "miss")
            else:
                self.set_fx("enemy_hit", "enemy")
            return outcome

        def _resolve_phase_three_null(self, skill):
            self.phase3_genre_shift_count += 1
            total_damage = 0
            buffed_members = 0
            for member in list(self.alive_party()):
                buff_bonus = max(0, member.atk_stage) + max(0, member.def_stage) + max(0, member.agi_stage)
                if buff_bonus > 0:
                    buffed_members += 1
                damage = max(1, int(skill.power + self.boss.magic * 0.82 + buff_bonus * 28))
                if member.guard:
                    damage = int(damage * 0.62)
                self._apply_enemy_damage_to_member(member, damage)
                member.atk_stage = min(0, member.atk_stage)
                member.def_stage = min(0, member.def_stage)
                member.agi_stage = min(0, member.agi_stage)
                member.clamp()
                total_damage += damage
            self.add_log("Identity Null burns the role labels off %d allies for %d total damage." % (buffed_members, total_damage))
            self.set_fx("enemy_aoe", "enemy")
            return "normal"

        def _choose_enemy_target(self, skill):
            alive = self.alive_party()
            stance = self.phase2_ai_stance if self.phase >= 2 else "balanced"
            taunters = [member for member in alive if member.taunt]
            if taunters and random.random() < (0.56 if self.phase == 3 else 0.70):
                return self._weighted_enemy_target(taunters)

            if self.heal_actions >= 2:
                healers = [member for member in alive if "cure" in member.skill_ids or "medica" in member.skill_ids or "white_wind" in member.skill_ids or "raise" in member.skill_ids]
                healer_chance = 0.16
                if stance == "aggressive":
                    healer_chance = 0.36 if self.phase == 3 else 0.28
                elif stance == "defensive":
                    healer_chance = 0.12
                if healers and random.random() < healer_chance:
                    return self._weighted_enemy_target(healers)

            weak_targets = [member for member in alive if skill.element in member.weaknesses and not member.guard]
            weak_target_chance = 0.22 if self.phase == 1 else (0.30 if self.phase == 3 else 0.32)
            if stance == "aggressive":
                weak_target_chance = 0.42 if self.phase == 3 else 0.50
            elif stance == "defensive":
                weak_target_chance = 0.22 if self.phase == 3 else 0.22
            if weak_targets and random.random() < weak_target_chance:
                return self._weighted_enemy_target(weak_targets)

            lowest_hp_chance = 0.20 if self.phase == 3 else 0.18
            if stance == "aggressive":
                lowest_hp_chance = 0.28 if self.phase == 3 else 0.26
            elif stance == "defensive":
                lowest_hp_chance = 0.14 if self.phase == 3 else 0.12
            if random.random() < lowest_hp_chance:
                return min(alive, key=lambda member: member.hp_ratio)
            return self._weighted_enemy_target(alive)

        def _weighted_enemy_target(self, candidates):
            weighted = []
            for member in candidates:
                weight = 5 if member.row == "front" else 2
                if member.id == self.last_enemy_target_id and len(candidates) > 1:
                    weight = max(1, weight - 3)
                if member.hp_ratio < 0.30:
                    weight = max(1, weight - 2)
                for _i in range(weight):
                    weighted.append(member)
            if not weighted:
                return random.choice(candidates)
            return random.choice(weighted)

        def _damage_party_member(self, target, skill):
            if random.random() > self._hit_chance(self.boss, target, skill):
                return "miss", 0

            affinity = self._target_affinity(target, skill.element)
            critical = random.random() < self._crit_chance(self.boss, target, skill)
            damage = self._damage_amount(self.boss, target, skill, skill.element, critical, affinity)
            self._apply_enemy_damage_to_member(target, damage)
            return ("critical" if critical else affinity), damage

        def _target_affinity(self, target, element):
            if target.guard and element in target.weaknesses:
                return "normal"
            if element in target.weaknesses:
                return "weak"
            if element in target.resists:
                return "resist"
            return "normal"

        def _actual_element(self, actor, skill):
            if skill.element == "weapon":
                return actor.attack_element
            return skill.element

        def _hit_chance(self, attacker, target, skill):
            chance = skill.accuracy + ((attacker.agility + attacker.agi_stage * 8) - (target.agility + target.agi_stage * 8)) * 0.0025
            if target.guard:
                chance -= 0.02
            return max(0.55, min(0.99, chance))

        def _crit_chance(self, attacker, target, skill):
            chance = skill.crit + max(0, attacker.agility - target.agility) * 0.0015
            if attacker.focus:
                chance += 0.06
            return max(0.0, min(0.45, chance))

        def _damage_amount(self, attacker, target, skill, element, critical, affinity):
            source = attacker.magic if skill.stat == "magic" else attacker.offense
            if attacker.id == "matsuda":
                if self.phase == 3:
                    base = skill.power + source * 1.08 - target.defense * 0.62
                    damage_ceiling = 1.50
                    damage_floor = 22.0
                else:
                    base = skill.power + source * 1.28 - target.defense * 0.58
                    damage_ceiling = 1.70
                    damage_floor = 20.0
            else:
                base = skill.power * 0.92 + source * 1.18 - target.defense * 0.62
                damage_ceiling = 1.95
                damage_floor = 28.0
            base = max(damage_floor, base)

            stage_mult = max(0.58, 1.0 + attacker.atk_stage * 0.14 - target.def_stage * 0.12)
            damage_mult = stage_mult
            if attacker.focus:
                damage_mult *= 1.20 if attacker.id == "matsuda" else 1.32
                attacker.focus = False
            if affinity == "weak":
                damage_mult *= 1.14 if attacker.id == "matsuda" else 1.18
            elif affinity == "resist":
                damage_mult *= 0.55
            if critical:
                damage_mult *= 1.18 if attacker.id == "matsuda" else 1.25
            if target.guard:
                damage_mult *= 0.55
            if attacker.id == "matsuda" and target.row == "rear":
                if element in ("slash", "pierce"):
                    damage_mult *= 0.76
                else:
                    damage_mult *= 0.88
            damage_mult = msbf_clamp(damage_mult, 0.25, damage_ceiling)
            variance = msbf_gaussian_variance(
                MSBF_DAMAGE_VARIANCE_STDEV,
                MSBF_DAMAGE_VARIANCE_MIN,
                MSBF_DAMAGE_VARIANCE_MAX
            )
            return max(1, int(round(base * damage_mult * variance)))

        def _true_damage_amount(self, actor, skill, critical, affinity):
            source = actor.magic if skill.stat == "magic" else actor.offense
            base = max(1.0, skill.power + source * 0.72)
            damage_mult = max(0.72, 1.0 + actor.atk_stage * 0.12)
            if actor.focus:
                damage_mult *= 1.24
                actor.focus = False
            if affinity == "weak":
                damage_mult *= 1.18
            elif affinity == "resist":
                damage_mult *= 0.55
            if critical:
                damage_mult *= 1.18
            if self.boss.guard:
                damage_mult *= 0.72
            variance = msbf_gaussian_variance(
                MSBF_DAMAGE_VARIANCE_STDEV,
                MSBF_DAMAGE_VARIANCE_MIN,
                MSBF_DAMAGE_VARIANCE_MAX
            )
            return max(1, int(round(base * damage_mult * variance)))

        def _healing_amount(self, actor, skill):
            base = skill.power + actor.magic * 1.15
            variance = msbf_gaussian_variance(
                MSBF_HEAL_VARIANCE_STDEV,
                MSBF_HEAL_VARIANCE_MIN,
                MSBF_HEAL_VARIANCE_MAX
            )
            return max(1, int(round(base * variance)))

        def _white_wind_amount(self, actor):
            return max(1, int(actor.hp * 0.42 + actor.magic * 0.25))

        def _lowest_wounded_ally(self):
            alive = self.alive_party()
            wounded = [member for member in alive if member.hp < member.max_hp]
            if not wounded:
                return min(alive, key=lambda member: member.hp_ratio)
            return min(wounded, key=lambda member: member.hp_ratio)

        def _first_defeated_ally(self):
            defeated = self.defeated_party()
            if not defeated:
                return None
            return defeated[0]
