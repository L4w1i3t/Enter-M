"""Greywake Field: deterministic, pickleable tactical rules with no Ren'Py imports.

Public commands deliberately return None, including rejected commands. The screen
copies this state before dispatch so Ren'Py rollback restores complete turns.
Coordinates are (column, row), origin at the northwest corner. Relief is shared:
neither army scores points by killing the people both coalitions need to feed.
"""

from heapq import heappop, heappush


SIDE_NAMES = {"akai": "Southern Compact", "rival": "Northern Concord"}
TERRAIN = {
    "grass": {"name": "Grassland", "defense": 0, "cost": 1},
    "road": {"name": "Military road", "defense": 0, "cost": 1},
    "forest": {"name": "Woodland", "defense": 2, "cost": 2},
    "ridge": {"name": "Broken ridge", "defense": 1, "cost": 2},
    "river": {"name": "Deep river", "defense": 0, "cost": None},
    "bridge": {"name": "Timber bridge", "defense": 0, "cost": 1},
    "ford": {"name": "Old ford", "defense": 0, "cost": 1},
    "fort": {"name": "Field redoubt", "defense": 3, "cost": 1},
    "village": {"name": "Abandoned village", "defense": 1, "cost": 1},
    "ruins": {"name": "Burned settlement", "defense": 1, "cost": 2},
}
MOUNTED = ("lancer", "cavalry")
MEDICS = ("cleric", "medic")


def distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])


def _unit(uid, name, side, role, x, y, hp, attack, defense, movement,
          weapon="sword", affiliation="", strength=96):
    return dict(id=uid, name=name, side=side, role=role, x=x, y=y, hp=hp,
                max_hp=hp, atk=attack, defense=defense, mov=movement,
                range_min=2 if role == "archer" else 1,
                range_max=2 if role == "archer" else 1, weapon=weapon,
                acted=False, down=False, dead=False, removed=False,
                stabilized=False, bleed=0, affiliation=affiliation,
                strength=strength, army_dead=0, army_wounded=0)


class GreywakeBattle:
    """One isolated ten-round battle. Only ``side`` receives player commands."""

    width = 18
    height = 12
    max_rounds = 10

    def __init__(self, side):
        if side not in SIDE_NAMES:
            raise ValueError("Greywake requires a permanent coalition choice.")
        self.side = side
        self.enemy_side = "rival" if side == "akai" else "akai"
        self.round = 1
        self.phase = "player"
        self.storm = False
        self.selected_id = None
        self.moved = False
        self._move_origin = None
        self.log = []
        self.event_queue = []
        self.result = None
        self.final_cause = None
        self.last_exchange_pair = None
        self.enemy_queue = []
        self.terrain = self._make_map()
        self.units = [
            _unit("akai", "Akai", "akai", "lord", 3, 5, 34, 13, 5, 5,
                  affiliation="Orra river towns", strength=144),
            _unit("gary", "Gary", "akai", "lancer", 5, 2, 28, 12, 4, 6,
                  "lance", "Border free companies", 80),
            _unit("gregor", "Gregor", "akai", "armor", 3, 8, 36, 11, 8, 3,
                  "sword", "Varn shield companies", 144),
            _unit("leif", "Leif", "akai", "cavalry", 4, 9, 27, 12, 4, 7,
                  "sword", "Orra outriders", 96),
            _unit("tsubaki", "Tsubaki", "akai", "cleric", 2, 6, 23, 6, 2, 5,
                  "staff", "Southern field hospital", 80),
            _unit("vey", "Vey", "akai", "archer", 3, 2, 25, 12, 3, 5,
                  "bow", "Border free companies", 96),
            _unit("bran", "Bran", "akai", "infantry", 2, 4, 29, 11, 5, 5,
                  "sword", "Orra river levy", 120),
            _unit("rival", "MC", "rival", "lord", 14, 5, 34, 13, 5, 5,
                  affiliation="Capital levies", strength=144),
            _unit("sam", "Sam", "rival", "berserker", 5, 7, 35, 16, 3, 5,
                  "sword", "Upland barons", 120),
            _unit("ilen", "Ilen", "rival", "medic", 15, 6, 23, 6, 2, 5,
                  "staff", "Northern field hospital", 80),
            _unit("rusk", "Rusk", "rival", "lancer", 12, 2, 28, 12, 4, 6,
                  "lance", "Salt Coast regiments", 80),
            _unit("nera", "Nera", "rival", "archer", 14, 2, 25, 12, 3, 5,
                  "bow", "Upland barons", 96),
            _unit("orren", "Orren", "rival", "armor", 6, 8, 36, 11, 8, 3,
                  "sword", "Capital shield levy", 144),
            _unit("sable", "Sable", "rival", "scout", 15, 4, 27, 11, 4, 6,
                  "sword", "Salt Coast regiments", 96),
        ]
        self.objectives = [
            dict(id="north_wagons", name="North-road families", kind="wagon",
                 x=7, y=2, total=12, remaining=12, hp=12, evacuated=0,
                 secured=False, secured_by=None, lost=0),
            dict(id="east_wagons", name="East-camp wounded", kind="wagon",
                 x=10, y=6, total=16, remaining=16, hp=16, evacuated=0,
                 secured=False, secured_by=None, lost=0),
            dict(id="ford_wagons", name="Ford-road families", kind="wagon",
                 x=7, y=10, total=12, remaining=12, hp=12, evacuated=0,
                 secured=False, secured_by=None, lost=0),
            dict(id="west_grain", name="Orra grain", kind="granary",
                 x=5, y=5, total=8, remaining=8, hp=8, evacuated=0,
                 secured=False, secured_by=None, lost=0),
            dict(id="east_grain", name="Concord grain", kind="granary",
                 x=12, y=5, total=8, remaining=8, hp=8, evacuated=0,
                 secured=False, secured_by=None, lost=0),
        ]
        self._event("start", "Greywake Field. Save lives and seed grain. Only the two lords can fell each other; their Last Exchange always wounds both.", side)

    @staticmethod
    def _make_map():
        board = [["grass" for x in range(18)] for y in range(12)]
        for y in range(12):
            board[y][8] = "river"
        for x in range(18):
            board[5][x] = "road"
        board[5][8] = "bridge"
        board[9][8] = "ford"
        for x, y in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (5, 0),
                     (6, 0), (5, 1), (10, 0), (11, 0), (16, 0), (17, 0),
                     (16, 1), (17, 1), (6, 3), (7, 3), (10, 3), (11, 3),
                     (1, 6), (1, 7), (6, 7), (10, 8), (11, 8), (16, 8),
                     (2, 10), (3, 10), (2, 11), (3, 11), (15, 10), (15, 11)):
            board[y][x] = "forest"
        for x, y in ((2, 7), (3, 7), (4, 7), (5, 7), (4, 8), (5, 8), (12, 1),
                     (13, 1), (13, 2), (14, 1), (12, 10), (13, 10)):
            board[y][x] = "ridge"
        for x, y in ((6, 1), (7, 1), (7, 2), (7, 4), (9, 4), (10, 4),
                     (10, 6), (11, 6), (7, 9), (9, 9), (7, 10), (6, 10)):
            board[y][x] = "road"
        board[4][4] = board[6][13] = "fort"
        board[4][5] = board[4][12] = "village"
        board[10][5] = board[7][12] = "ruins"
        return board

    def _event(self, kind, text, side=None, **payload):
        event = dict(kind=kind, round=self.round, side=side, text=text)
        event.update(payload)
        self.event_queue.append(event)
        self.log.append(text)
        self.log = self.log[-80:]

    def unit(self, uid):
        return next((u for u in self.units if u["id"] == uid), None)

    def objective(self, oid):
        return next((o for o in self.objectives if o["id"] == oid), None)

    def unit_at(self, x, y):
        return next((u for u in self.units if not u["removed"] and
                     (u["x"], u["y"]) == (x, y)), None)

    def selected_unit(self):
        return self.unit(self.selected_id)

    def _active(self, unit):
        return unit is not None and not unit["removed"] and not unit["down"] and unit["hp"] > 0

    def _ready(self):
        unit = self.selected_unit()
        return (self.phase == "player" and self._active(unit) and
                unit["side"] == self.side and not unit["acted"])

    def _inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _neighbors(self, x, y):
        return [(nx, ny) for nx, ny in ((x - 1, y), (x, y - 1),
                                       (x + 1, y), (x, y + 1)) if self._inside(nx, ny)]

    def _cost(self, unit, x, y):
        terrain = self.terrain[y][x]
        if terrain == "ford" and self.storm:
            return None if unit["role"] in MOUNTED else 3
        cost = TERRAIN[terrain]["cost"]
        if cost is not None and unit["role"] in MOUNTED and terrain in ("forest", "ridge"):
            return cost + 1
        return cost

    def terrain_info(self, x, y):
        if not self._inside(x, y):
            return dict(name="Outside field", defense=0, cost=None, passable=False)
        info = dict(TERRAIN[self.terrain[y][x]])
        unit = self.selected_unit()
        if unit:
            info["cost"] = self._cost(unit, x, y)
        elif self.terrain[y][x] == "ford" and self.storm:
            info["cost"] = 3
        info["passable"] = info["cost"] is not None
        info["terrain"] = self.terrain[y][x]
        if self.terrain[y][x] == "ford" and self.storm:
            info["name"] = "Flooded ford (foot 3; horses blocked)"
        return info

    def _paths(self, unit, limit=None):
        """Dijkstra permits passage through allies, but never occupied endpoints."""
        if not self._active(unit):
            return {}
        origin = unit["x"], unit["y"]
        costs = {origin: 0}
        queue = [(0, origin)]
        while queue:
            spent, position = heappop(queue)
            if spent != costs[position]:
                continue
            for nx, ny in self._neighbors(*position):
                cost = self._cost(unit, nx, ny)
                blocker = self.unit_at(nx, ny)
                if cost is None or (self._active(blocker) and blocker["side"] != unit["side"]):
                    continue
                total = spent + cost
                if (limit is not None and total > limit) or total >= costs.get((nx, ny), 100000):
                    continue
                costs[nx, ny] = total
                heappush(queue, (total, (nx, ny)))
        return {pos: cost for pos, cost in costs.items()
                if pos == origin or self.unit_at(*pos) is None}

    def reachable(self, unit_id=None):
        unit = self.unit(unit_id) if unit_id is not None else self.selected_unit()
        if not self._active(unit) or unit["acted"]:
            return {}
        if unit_id is None and self.moved:
            return {(unit["x"], unit["y"]): 0}
        return self._paths(unit, unit["mov"])

    def _can_attack(self, attacker, defender):
        return (self._active(attacker) and self._active(defender) and
                attacker["side"] != defender["side"] and
                attacker["range_min"] <= distance(attacker, defender) <= attacker["range_max"])

    def _damage(self, attacker, defender):
        triangle = {"sword": "axe", "axe": "lance", "lance": "sword"}
        bonus = 2 if triangle.get(attacker["weapon"]) == defender["weapon"] else 0
        if triangle.get(defender["weapon"]) == attacker["weapon"]:
            bonus = -1
        cover = TERRAIN[self.terrain[defender["y"]][defender["x"]]]["defense"]
        return max(1, attacker["atk"] + bonus - defender["defense"] - cover)

    def preview(self, attacker_id, defender_id):
        attacker, defender = self.unit(attacker_id), self.unit(defender_id)
        legal = self._can_attack(attacker, defender)
        if not legal:
            return dict(damage=0, counter_damage=0, can_attack=False, defense=0,
                        lethal=False, counter_lethal=False, last_exchange=False,
                        paired=False, attacker_hp=None, defender_hp=None)
        damage = min(defender["hp"], self._damage(attacker, defender))
        if defender["role"] == "lord" and attacker["role"] != "lord":
            damage = min(damage, max(0, defender["hp"] - 1))
        counter = 0
        if damage < defender["hp"] and self._can_attack(defender, attacker):
            counter = min(attacker["hp"], self._damage(defender, attacker))
            if attacker["role"] == "lord" and defender["role"] != "lord":
                counter = min(counter, max(0, attacker["hp"] - 1))
        final = (attacker["role"] == defender["role"] == "lord" and
                 (damage >= defender["hp"] or counter >= attacker["hp"]))
        # The binding exchange supersedes the ordinary strike/counter sequence.
        # Its forecast must describe the complete simultaneous resolution.
        if final:
            damage, counter = defender["hp"], attacker["hp"]
        return dict(damage=damage, counter_damage=counter, can_attack=True,
                    defense=TERRAIN[self.terrain[defender["y"]][defender["x"]]]["defense"],
                    lethal=damage >= defender["hp"], counter_lethal=counter >= attacker["hp"],
                    last_exchange=final, paired=final,
                    attacker_hp=attacker["hp"] - counter, defender_hp=defender["hp"] - damage)

    def attack_targets(self, unit_id=None):
        unit = self.unit(unit_id) if unit_id else self.selected_unit()
        return [target for target in self.units if self._can_attack(unit, target)]

    def heal_targets(self):
        unit = self.selected_unit()
        if not self._ready() or unit["role"] not in MEDICS:
            return []
        return [u for u in self.units if self._active(u) and u["side"] == unit["side"]
                and u["hp"] < u["max_hp"] and distance(unit, u) <= 1]

    def adjacent_objectives(self):
        unit = self.selected_unit()
        if not self._ready():
            return []
        return [o for o in self.objectives if not o["secured"] and o["hp"] > 0
                and distance(unit, o) <= 1]

    def rescue_targets(self):
        unit = self.selected_unit()
        if not self._ready():
            return []
        targets = [u for u in self.units if u["side"] == unit["side"] and u["down"]
                   and not u["removed"] and distance(unit, u) <= 1]
        return targets + [o for o in self.adjacent_objectives() if o["kind"] == "wagon"]

    def legal_actions(self):
        if not self._ready():
            return []
        actions = []
        if self.attack_targets():
            actions.append("attack")
        if self.heal_targets():
            actions.append("heal")
        if self.rescue_targets():
            actions.append("rescue")
        if any(o["kind"] == "granary" for o in self.adjacent_objectives()):
            actions.append("secure")
        return actions + ["wait", "cancel"]

    def danger_tiles(self):
        danger = set()
        for unit in self.units:
            if not self._active(unit) or unit["side"] != self.enemy_side:
                continue
            for x, y in self._paths(unit, unit["mov"]):
                for dx in range(-unit["range_max"], unit["range_max"] + 1):
                    for dy in range(-unit["range_max"], unit["range_max"] + 1):
                        if (unit["range_min"] <= abs(dx) + abs(dy) <= unit["range_max"]
                                and self._inside(x + dx, y + dy)):
                            danger.add((x + dx, y + dy))
        return danger

    def select(self, unit_id):
        unit = self.unit(unit_id)
        if (self.phase != "player" or self.moved or not self._active(unit)
                or unit["side"] != self.side or unit["acted"]):
            return
        self.selected_id = unit_id
        self._move_origin = None

    def click_tile(self, x, y):
        if self.phase != "player" or not self._inside(x, y):
            return
        target = self.unit_at(x, y)
        if target:
            if self._ready() and target["side"] != self.side:
                self.attack(target["id"])
            elif self._ready() and target["down"]:
                self.rescue(target["id"])
            else:
                self.select(target["id"])
        elif self._ready():
            self.move(x, y)

    def move(self, x, y):
        if not self._ready() or self.moved or (x, y) not in self.reachable():
            return
        unit = self.selected_unit()
        self._move_origin = unit["x"], unit["y"]
        unit["x"], unit["y"] = x, y
        self.moved = True

    def cancel(self):
        if self.phase != "player":
            return
        unit = self.selected_unit()
        if unit and self._move_origin:
            unit["x"], unit["y"] = self._move_origin
        self._clear_selection()

    def _clear_selection(self):
        self.selected_id = None
        self.moved = False
        self._move_origin = None

    def _commit(self, unit):
        unit["acted"] = True
        self._clear_selection()

    def _formation_losses(self, unit, damage=0, attrition=0):
        available = max(0, unit["strength"] - unit["army_dead"] - unit["army_wounded"])
        dead = min(available, (damage + 2) // 3 + attrition)
        wounded = min(available - dead, damage * 2 + attrition)
        unit["army_dead"] += dead
        unit["army_wounded"] += wounded

    def _hit(self, attacker, defender, damage):
        if defender["role"] == "lord" and attacker["role"] != "lord":
            damage = min(damage, max(0, defender["hp"] - 1))
        if attacker["role"] == defender["role"] == "lord" and damage >= defender["hp"]:
            self.last_exchange_pair = (attacker["id"], defender["id"])
            self._arm_final("lord_duel")
            return
        actual = min(defender["hp"], damage)
        defender["hp"] -= actual
        self._formation_losses(defender, actual)
        self._event("attack", "{} strikes {} for {}.".format(attacker["name"], defender["name"], actual),
                    attacker["side"], attacker=attacker["id"], target=defender["id"], damage=actual)
        if defender["hp"] > 0:
            return
        if defender["role"] == "lord":
            self.last_exchange_pair = (attacker["id"], defender["id"])
            self._arm_final("lord_duel")
        else:
            defender["down"] = True
            defender["bleed"] = 2
            self._event("downed", "{} falls. An adjacent ally has two round-ends to rescue them.".format(defender["name"]),
                        defender["side"], unit=defender["id"])

    def _combat(self, attacker, defender):
        if not self._can_attack(attacker, defender):
            return
        if self.preview(attacker["id"], defender["id"])["last_exchange"]:
            # Queue both blows before either HP/formation ledger changes, even
            # when the ordinary counter would have been the decisive blow.
            self.last_exchange_pair = (attacker["id"], defender["id"])
            self._arm_final("lord_duel")
            return
        self._hit(attacker, defender, self._damage(attacker, defender))
        if self.phase in ("player", "enemy") and self._can_attack(defender, attacker):
            self._hit(defender, attacker, self._damage(defender, attacker))

    def attack(self, target_id):
        if not self._ready():
            return
        unit, target = self.selected_unit(), self.unit(target_id)
        if not self._can_attack(unit, target):
            return
        self._combat(unit, target)
        self._commit(unit)

    def _heal(self, unit, target):
        amount = min(12, target["max_hp"] - target["hp"])
        target["hp"] += amount
        self._event("heal", "{} treats {} (+{} HP). Formation casualties remain.".format(unit["name"], target["name"], amount),
                    unit["side"], unit=unit["id"], target=target["id"], healed=amount)

    def heal(self, target_id):
        if not self._ready():
            return
        target = self.unit(target_id)
        if target not in self.heal_targets():
            return
        unit = self.selected_unit()
        self._heal(unit, target)
        self._commit(unit)

    def _rescue_unit(self, unit, target):
        target["stabilized"] = True
        target["removed"] = True
        target["bleed"] = 0
        self._event("rescue", "{} gets {} to the bearers. Wounded, alive, out of battle.".format(unit["name"], target["name"]),
                    unit["side"], unit=unit["id"], target=target["id"])

    def _save_objective(self, unit, objective):
        objective["secured"] = True
        objective["secured_by"] = unit["side"]
        if objective["kind"] == "wagon":
            objective["evacuated"] = objective["remaining"]
            objective["remaining"] = 0
            self._event("evacuate", "{} escorts {} people from {} off the field.".format(unit["name"], objective["evacuated"], objective["name"]),
                        unit["side"], unit=unit["id"], objective=objective["id"], saved=objective["evacuated"])
        else:
            self._event("supply", "{} secures {} for the common relief road.".format(unit["name"], objective["name"]),
                        unit["side"], unit=unit["id"], objective=objective["id"])

    def rescue(self, target_id):
        if not self._ready():
            return
        target = next((t for t in self.rescue_targets() if t["id"] == target_id), None)
        if target is None:
            return
        unit = self.selected_unit()
        if target.get("kind") == "wagon":
            self._save_objective(unit, target)
        else:
            self._rescue_unit(unit, target)
        self._commit(unit)

    def secure(self, objective_id):
        if not self._ready():
            return
        objective = self.objective(objective_id)
        if objective not in self.adjacent_objectives() or objective["kind"] != "granary":
            return
        unit = self.selected_unit()
        self._save_objective(unit, objective)
        self._commit(unit)

    def wait_unit(self):
        if self._ready():
            self._commit(self.selected_unit())

    def _ai_action(self, unit):
        """Evaluate reachable endpoints and actions; approach via true path costs."""
        moves = self._paths(unit, unit["mov"])
        if not moves:
            return
        origin = unit["x"], unit["y"]
        candidates = []
        active_enemies = [u for u in self.units if self._active(u) and u["side"] != unit["side"]]
        relief_role = unit["role"] in MEDICS + ("lancer", "cavalry", "scout")
        # Coalition logistics stay on their own riverbank. The player can send
        # aid across it; leaving everything to the other army loses that choice.
        relief_objectives = [o for o in self.objectives
                             if (o["x"] < 8) == (unit["side"] == "akai")]
        for position, spent in moves.items():
            unit["x"], unit["y"] = position
            cover = TERRAIN[self.terrain[position[1]][position[0]]]["defense"]
            for target in self.units:
                if (target["side"] == unit["side"] and target["down"]
                        and not target["removed"] and distance(unit, target) <= 1):
                    candidates.append((120 + cover, -spent, position, "rescue", target["id"]))
                if (unit["role"] in MEDICS and self._active(target) and
                        target["side"] == unit["side"] and distance(unit, target) <= 1
                        and target["hp"] <= target["max_hp"] - 6):
                    candidates.append((75 + target["max_hp"] - target["hp"] + cover,
                                       -spent, position, "heal", target["id"]))
            if relief_role:
                for objective in relief_objectives:
                    if not objective["secured"] and objective["hp"] > 0 and distance(unit, objective) <= 1:
                        urgency = 90 if objective["kind"] == "granary" else 85
                        candidates.append((urgency + cover, -spent, position, "objective", objective["id"]))
            for target in active_enemies:
                if not self._can_attack(unit, target):
                    continue
                if unit["role"] == target["role"] == "lord" and self.round < 7:
                    continue
                preview = self.preview(unit["id"], target["id"])
                score = 30 + preview["damage"] * 2 - preview["counter_damage"] + cover * 2
                score += 22 if preview["lethal"] else 0
                if target["role"] == "lord" and unit["role"] != "lord" and target["hp"] == 1:
                    score -= 60
                candidates.append((score, -spent, position, "attack", target["id"]))
        unit["x"], unit["y"] = origin
        if candidates:
            _, _, position, action, target_id = max(candidates)
            unit["x"], unit["y"] = position
            if action == "attack":
                self._combat(unit, self.unit(target_id))
            elif action == "heal":
                self._heal(unit, self.unit(target_id))
            elif action == "rescue":
                self._rescue_unit(unit, self.unit(target_id))
            else:
                self._save_objective(unit, self.objective(target_id))
            unit["acted"] = True
            return
        goals = [(u["x"], u["y"]) for u in active_enemies
                 if not (unit["role"] == u["role"] == "lord" and self.round < 7)]
        if relief_role:
            goals.extend((o["x"], o["y"]) for o in relief_objectives if not o["secured"] and o["hp"] > 0)
        if not goals:
            unit["acted"] = True
            return
        # Reverse distances preserve terrain and blockers instead of steering into rivers.
        approaches = []
        for position, spent in moves.items():
            unit["x"], unit["y"] = position
            paths = self._paths(unit)
            nearest = min((cost + abs(px - gx) + abs(py - gy)
                           for (px, py), cost in paths.items() for gx, gy in goals
                           if abs(px - gx) + abs(py - gy) <= unit["range_max"]), default=10000)
            approaches.append((nearest, -TERRAIN[self.terrain[position[1]][position[0]]]["defense"],
                               spent, position))
        unit["x"], unit["y"] = min(approaches)[3]
        unit["acted"] = True

    def _pressure(self):
        protected = sum(1 for o in self.objectives if o["kind"] == "granary" and o["secured"])
        for unit in self.units:
            if unit["dead"]:
                continue
            if self._active(unit):
                self._formation_losses(unit, attrition=max(0, (2 if self.storm else 1) - protected))
                if self.terrain[unit["y"]][unit["x"]] == "fort":
                    unit["hp"] = min(unit["max_hp"], unit["hp"] + 3)
            if unit["down"] and not unit["removed"]:
                unit["bleed"] -= 1
                if unit["bleed"] <= 0:
                    unit["dead"] = unit["removed"] = True
                    self._event("death", "{} dies before the bearers can reach them.".format(unit["name"]),
                                unit["side"], unit=unit["id"])
        losses = 0
        for objective in self.objectives:
            if objective["secured"] or objective["hp"] <= 0:
                continue
            guards = any(self._active(u) and distance(u, objective) <= 1 for u in self.units)
            pressure = max(0, (2 if self.storm else 1) - int(guards)) if self.round >= 2 else 0
            loss = min(objective["hp"], pressure)
            objective["hp"] -= loss
            if objective["kind"] == "wagon":
                objective["remaining"] -= loss
                objective["lost"] += loss
                losses += loss
            else:
                objective["remaining"] = objective["hp"]
                if objective["hp"] == 0:
                    self._event("supply_lost", "{} burns before anyone secures it.".format(objective["name"]), objective=objective["id"])
        if losses:
            self._event("pressure", "{} people are lost to fire, exposure and the closing roads.".format(losses), lost=losses)

    def begin_enemy_turn(self):
        """Commit player movement and prepare individually observable AI orders."""
        if self.phase != "player":
            return
        # Ending the phase commits a tentative move, just as Wait would.
        if self._ready():
            self._commit(self.selected_unit())
        self._clear_selection()
        self.enemy_queue = [u["id"] for u in self.units
                            if self._active(u) and u["side"] == self.enemy_side]
        self.phase = "enemy"
        self._event("enemy_phase", "{} orders.".format(SIDE_NAMES[self.enemy_side]), self.enemy_side)

    def enemy_step(self):
        """Resolve one queued formation. Safe to save between any two orders."""
        if self.phase != "enemy":
            return
        if self.enemy_queue:
            unit = self.unit(self.enemy_queue.pop(0))
            if self._active(unit):
                self._ai_action(unit)
            if self.phase != "enemy":
                return
        if not self.enemy_queue:
            self._finish_round()

    def end_turn(self):
        """Synchronous convenience for deterministic offline simulation/tests."""
        if self.phase != "player":
            return
        self.begin_enemy_turn()
        while self.phase == "enemy":
            self.enemy_step()

    def _finish_round(self):
        self._pressure()
        if self.round >= self.max_rounds:
            self._arm_final("tenth_round")
            return
        self.round += 1
        self.phase = "player"
        if self.round == 5:
            self.storm = True
            self._event("storm", "Round 5: the ford floods. Foot soldiers spend 3 movement there; horses must use the bridge. Relief losses double.")
        for unit in self.units:
            unit["acted"] = False
        self._event("round", "Round {}. {} orders.".format(self.round, SIDE_NAMES[self.side]), self.side)

    def _arm_final(self, cause):
        self.final_cause = cause
        self.phase = "final"
        self._clear_selection()
        if cause == "lord_duel":
            text = "The lords commit to the Last Exchange. The binding counterstroke wounds both; remaining relief work ends here."
        else:
            text = "The tenth round closes the road. Both exhausted lords enter the Last Exchange; their formations cannot continue."
        self._event("final", text, cause=cause)

    def final_exchange(self):
        if self.phase != "final":
            return
        exchange_damage = {uid: self.unit(uid)["hp"] for uid in ("akai", "rival")}
        for uid in ("akai", "rival"):
            unit = self.unit(uid)
            self._formation_losses(unit, damage=exchange_damage[uid])
            unit["hp"] = 0
            unit["down"] = unit["stabilized"] = unit["removed"] = True
            unit["dead"] = False
            unit["bleed"] = 0
        for attacker_id, target_id in (("akai", "rival"), ("rival", "akai")):
            attacker, target = self.unit(attacker_id), self.unit(target_id)
            self._event("attack", "{} lands the binding strike on {} for {}. Both lords fall together.".format(
                attacker["name"], target["name"], exchange_damage[target_id]),
                attacker["side"], attacker=attacker_id, target=target_id,
                damage=exchange_damage[target_id], paired=True)
        # Unescorted people are not retroactively rescued by ending the battle.
        for objective in self.objectives:
            if objective["kind"] == "wagon" and not objective["secured"]:
                objective["lost"] += objective["remaining"]
                objective["remaining"] = objective["hp"] = 0
        statuses = {}
        for unit in self.units:
            statuses[unit["id"]] = ("dead" if unit["dead"] else "wounded"
                                     if unit["down"] or unit["hp"] < unit["max_hp"] else "alive")
        armies = {}
        for side in SIDE_NAMES:
            army = [u for u in self.units if u["side"] == side]
            armies[side] = dict(dead=sum(u["army_dead"] for u in army),
                                wounded=sum(u["army_wounded"] for u in army),
                                strength=sum(u["strength"] for u in army))
        self.result = dict(
            draw=True, cause=self.final_cause, side=self.side, turns=self.round,
            unit_status=statuses, armies=armies,
            army_dead=sum(a["dead"] for a in armies.values()),
            army_wounded=sum(a["wounded"] for a in armies.values()),
            civilians_evacuated=sum(o["evacuated"] for o in self.objectives if o["kind"] == "wagon"),
            civilians_lost=sum(o["lost"] for o in self.objectives if o["kind"] == "wagon"),
            supplies_secured=sum(1 for o in self.objectives if o["kind"] == "granary" and o["secured"]),
            dead=[u["name"] for u in self.units if statuses[u["id"]] == "dead"],
            wounded=[u["name"] for u in self.units if statuses[u["id"]] == "wounded"],
            allied_dead=sum(statuses[u["id"]] == "dead" for u in self.units if u["side"] == self.side),
            enemy_dead=sum(statuses[u["id"]] == "dead" for u in self.units if u["side"] == self.enemy_side),
        )
        self.phase = "done"
        self._event("draw", "Both lords fall. Both armies withdraw. {} of 40 people evacuated; {} of 2 grain stores secured.".format(
            self.result["civilians_evacuated"], self.result["supplies_secured"]))
