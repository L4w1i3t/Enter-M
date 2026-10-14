# =============================================================================
# SPEC EMULATOR -- play the game as a slower machine would  (DEVELOPER ONLY)
# =============================================================================
# This folder is excluded from release builds (options.rpy), and nothing here
# runs until a preset is picked on the Dev Hub's SYSTEM page or the game is
# launched with ENTER_M_SPEC=<preset key> in the environment.
#
# WHY IT EXISTS
#   The development machine (Ryzen 5 8400F, RTX 5060, 240Hz) holds every mode
#   in the game at its refresh rate, so nothing that would stutter on a laptop
#   ever stutters here. This throttles it to a named slower machine, so the
#   heavy modes can be judged -- and their Low Detail stop tuned -- at the
#   speed a real player will see.
#
# THE MODEL
#   On the emulated machine a frame costs  max(CPU x cpu_time, GPU x gpu_time).
#   The main thread's Python (screens, the render tree, every CDD's sim, GL
#   submission) and the GPU's work overlap, so the slower of the two sets the
#   pace. Both are MEASURED live, every frame, on this machine:
#     cpu_time  wall time from the end of the previous flip to this one, minus
#               the time the interact loop spent blocked waiting for events.
#     gpu_time  a GL_TIME_ELAPSED query from the end of the render tree to the
#               flip -- the draws, render-to-texture passes and every shader.
#   The flip is held until the emulated cost has elapsed.
#
# THE 60HZ PANEL
#   Almost every slower machine is plugged into a 60Hz display, and that is a
#   different thing from this one: a frame that is ready a hair after a vblank
#   waits a whole 16.7ms for the next. Emulated here as a VIRTUAL vblank grid
#   with triple-buffered vsync -- one finished frame may wait in the queue
#   while the next is built, and a flip blocks only until the frame before it
#   has been shown. (Setting the real swap interval to 4 on a 240Hz panel was
#   tried and is NOT equivalent: the driver presents "at least four vblanks
#   later", so a late frame costs 4ms, not 16.7ms, and missed frames vanish.)
#   The real panel keeps presenting at its own rate; only the timing the game
#   experiences, and the intervals this records, follow the virtual grid.
#
# WHAT IT DOES NOT MODEL -- read before trusting a number
#   * The factors are ratios of published single-thread CPU scores and of GPU
#     ALU throughput and memory bandwidth (geometric mean of the two) against
#     this machine. Caches, drivers and thermal throttling all differ.
#   * The max() assumes perfect CPU/GPU overlap, but the hold itself is serial,
#     so a frame heavy on both reads slightly pessimistic. That is the right
#     direction to be wrong in for a stress test.
#   * Only the main thread is slowed. Image decode on the preload thread, audio
#     and disk run at this machine's speed.
#   * The GPU factor is scaled by screen AREA (the preset's own screen against
#     the window this is running in), which assumes the GPU work is fill-bound.
#     True of full-screen shaders and render targets; false of fixed per-draw
#     costs, which are small here.
#   * PIN GPU CLOCKS holds full clocks only while the emulated rate stays near
#     60. Once a preset drags a mode far below that, the real GPU idles through
#     most of each held frame and drops its clocks anyway; the inflated GPU
#     readings then lengthen the next hold, so a collapse reads worse than it
#     is. The readout flags it (LOW CLOCKS) and the harness prints gr/mem.
# =============================================================================

init -30 python:

    import time as _dse_time
    import math as _dse_math
    import collections as _dse_coll
    import ctypes as _dse_ct

    # key, label, CPU x, GPU x, presented Hz, target screen, what it stands for
    DEV_SPEC_PRESETS = (
        ("native", "THIS MACHINE", 1.0, 1.0, None, None,
            "No throttle, native refresh -- measures only."),
        ("native60", "THIS PC @ 60HZ", 1.0, 1.0, 60, None,
            "No throttle, presented on a 60Hz grid."),
        ("midrange", "MID LAPTOP", 1.4, 9.0, 60, (1920, 1080),
            "i5-1135G7 + Iris Xe (2021 thin-and-light), 1080p."),
        ("deck", "STEAM DECK", 2.0, 8.0, 60, (1280, 800),
            "Zen 2 4c/8t + RDNA2 8 CU, 1280x800."),
        ("budget", "BUDGET 2018", 2.4, 23.0, 60, (1920, 1080),
            "i5-8250U + UHD 620, 1080p."),
        ("potato", "POTATO", 5.0, 45.0, 60, (1366, 768),
            "Celeron N4020 + UHD 600, 1366x768. Expected to struggle."),
    )

    def dev_spec_preset(key):
        for row in DEV_SPEC_PRESETS:
            if row[0] == key:
                return row
        return None

    class _DseNvml(python_object):
        """
        Read-only NVIDIA clock sampling (nvml.dll ships with the driver). The
        development GPU idles in a low power state while this game runs it at
        a few percent load -- measured P5, ~700-1100MHz graphics and 810MHz
        memory against maxima of 3090/14001 -- and a GPU timer read in that
        state is inflated, worst for bandwidth-bound work. Knowing the clocks
        is what lets a measurement be put back on the full-clock footing the
        presets' ratios assume. Absent or failing: every method is inert.
        """

        def __init__(self):
            self.ok = False
            self.gr_max = self.mem_max = 0
            self.gr = self.mem = 0
            self._at = -1.0
            try:
                lib = _dse_ct.WinDLL("nvml.dll")
                if lib.nvmlInit_v2() != 0:
                    raise Exception("nvmlInit failed")
                h = _dse_ct.c_void_p()
                if lib.nvmlDeviceGetHandleByIndex_v2(0, _dse_ct.byref(h)) != 0:
                    raise Exception("no device 0")
                self.lib = lib
                self.h = h
                self.v = _dse_ct.c_uint(0)
                lib.nvmlDeviceGetMaxClockInfo(h, 0, _dse_ct.byref(self.v))
                self.gr_max = int(self.v.value)
                lib.nvmlDeviceGetMaxClockInfo(h, 2, _dse_ct.byref(self.v))
                self.mem_max = int(self.v.value)
                self.ok = self.gr_max > 0 and self.mem_max > 0
            except Exception:
                self.ok = False

        def sample(self, now):
            """(graphics MHz, memory MHz), re-read at most every 100ms."""
            if not self.ok:
                return (0, 0)
            if now - self._at >= 0.1:
                self._at = now
                try:
                    self.lib.nvmlDeviceGetClockInfo(self.h, 0, _dse_ct.byref(self.v))
                    self.gr = int(self.v.value)
                    self.lib.nvmlDeviceGetClockInfo(self.h, 2, _dse_ct.byref(self.v))
                    self.mem = int(self.v.value)
                except Exception:
                    self.ok = False
            return (self.gr, self.mem)


    # THE CLOCK PIN. At this game's load the development GPU never leaves its
    # low power states, and a GPU timer read there is inflated -- by ~11x for
    # a render-to-texture pass with memory at 810MHz instead of 7001MHz
    # (measured, same work, two loads). No formula over the clocks fixes that
    # (each kind of work scales differently), so the measurement is taken at
    # full clocks instead: right after each flip, a dummy pass into an
    # offscreen texture keeps the GPU busy enough that the driver holds its
    # top state. It runs OUTSIDE the timed window -- a TIME_ELAPSED query
    # starts only once every earlier command has finished -- and its work
    # grows until NVML reports full clocks.
    try:
        # No tex0: the child is a Solid, which Ren'Py draws through its own
        # solid-colour shader part, so there is no texture to bind.
        renpy.register_shader("dse.heater", variables="""
            uniform float u_dse_n;
            uniform float u_dse_seed;
            attribute vec4 a_position;
            varying vec2 v_dse_pos;
        """, vertex_300="""
            v_dse_pos = a_position.xy;
        """, fragment_300="""
            vec2 p = v_dse_pos * 0.001;
            float acc = u_dse_seed;
            for (int i = 0; i < 16384; i++) {
                if (float(i) >= u_dse_n) {
                    break;
                }
                acc = fract(sin(dot(p + acc, vec2(12.9898, 78.233))) * 43758.5453);
            }
            gl_FragColor = vec4(acc, acc, acc, 1.0);
        """)
        _DSE_HEATER_OK = True
    except Exception:
        _DSE_HEATER_OK = False


    class _DseHeater(python_object):
        """
        Adaptive GPU load that holds the clocks up. See the note above.

        Deliberately SMALL: one 512x512 pass whose cost is arithmetic, not
        memory traffic. A first cut ran six full-screen passes and the work
        leaked into the CPU readings (Kotonoha's flood went 9.4 -> 21ms of
        "CPU"): the next frame's GL calls blocked behind it. The load now
        walks DOWN as well as up, to the least that keeps full clocks, and it
        times itself with its own GPU query so it can be capped.
        """

        W = 512
        H = 512
        CAP_MS = 6.0        # never spend more than this per frame on it

        def __init__(self):
            self.n = 160.0
            self.err = None
            self.gpu_ms = 0.0
            self._at = -1.0
            self._good_since = None
            self._solid = Solid("#203040")
            self._seed = 0.0

        def tune(self, clk, nvml, now):
            if now - self._at < 0.25 or not nvml.ok:
                return
            self._at = now
            gr, mem = clk
            full = gr >= 0.90 * nvml.gr_max and mem >= 0.90 * nvml.mem_max
            if not full:
                self._good_since = None
                if self.gpu_ms < self.CAP_MS:
                    self.n = min(16000.0, self.n * 1.25 + 8.0)
            else:
                if self._good_since is None:
                    self._good_since = now
                elif now - self._good_since > 1.5 and self.n > 24.0:
                    self.n *= 0.93
                    self._good_since = now
            if self.gpu_ms > self.CAP_MS:
                self.n = max(16.0, self.n * 0.85)

        def run(self):
            if self.err is not None:
                return
            try:
                child = renpy.display.render.render(self._solid, self.W, self.H, 0, 0)
                self._seed = (self._seed + 0.618) % 1.0
                rv = renpy.Render(self.W, self.H)
                rv.mesh = True
                rv.add_shader("dse.heater")
                rv.add_uniform("u_dse_n", float(self.n))
                rv.add_uniform("u_dse_seed", self._seed)
                rv.blit(child, (0, 0))
                rv.render_to_texture(True)
            except Exception as e:
                self.err = repr(e)


    _DSE_GL_TIME_ELAPSED = 0x88BF
    _DSE_GL_QUERY_RESULT = 0x8866
    _DSE_GL_QUERY_RESULT_AVAILABLE = 0x8867


    class DevSpecEmulator(python_object):
        """
        The throttle. The engine hooks it drives are installed once per
        PROCESS and look it up through an attribute on pygame_sdl2.display,
        so a script reload hands them the new instance instead of leaving them
        bound to a dead one.
        """

        RING = 600          # frames kept for the live readout
        QUERIES = 8         # GL timer queries in flight at most
        QUEUE = 1           # finished frames allowed to wait for a vblank

        def __init__(self):
            self.key = None
            self.label = ""
            self.note = ""
            self.cpu_x = 1.0
            self.gpu_x = 1.0
            self.gpu_x_eff = 1.0
            self.area_x = 1.0
            self.hz = None
            self.screen = None
            self.active = False
            self.pending = None
            self.overlay = True
            self.gl_note = ""
            self.frames = _dse_coll.deque(maxlen=self.RING)
            self.segment = None
            self.segments = []
            self._idle = 0.0
            self._t_flip = None
            self._rec = None
            self._gpu_ms = 0.0
            self._gl = None
            self._q_free = []
            self._q_pending = []
            self._q_active = None
            self._grid0 = None      # time of virtual vblank 0
            self._n_prev = None     # virtual vblank the last frame was shown on
            self._nvml = None
            self._clk = (0, 0)
            self._area_at = -1.0
            # Hold the GPU at full clocks while measuring (see THE CLOCK PIN).
            self.pin = True
            self._heater = None

        # ----- selection -----------------------------------------------------

        def select(self, key):
            """Pick a preset by key, or None to switch the emulator off."""

            row = dev_spec_preset(key) if key else None

            if row is None:
                self._deactivate()
                return

            _dse_install_hooks()

            self.key, self.label = row[0], row[1]
            self.cpu_x, self.gpu_x = float(row[2]), float(row[3])
            self.hz, self.screen, self.note = row[4], row[5], row[6]

            # Remembered on the hooks' module so a Shift+R keeps the throttle.
            import pygame_sdl2
            pygame_sdl2.display._dse_key = self.key

            # GL work needs the context current, which is only a given inside a
            # frame -- so arm it here and let the next flip finish the job.
            self.pending = self.key
            renpy.restart_interaction()

        def _activate(self):
            self.pending = None
            self._gl_init()
            if self._nvml is None:
                self._nvml = _DseNvml()
            if self._heater is None and _DSE_HEATER_OK and self._nvml.ok:
                self._heater = _DseHeater()

            self._update_area()

            self.frames.clear()
            self._t_flip = None
            self._idle = 0.0
            self._rec = None
            self._grid0 = None
            self._n_prev = None
            self.active = True

            if "dev_spec_overlay" not in config.overlay_screens:
                config.overlay_screens.append("dev_spec_overlay")

        def _update_area(self):
            """
            Area scaling: the preset's own screen against this window. Re-read
            every half second from before_flip as well, because the window can
            change size after a preset is armed (a resize, a fullscreen toggle,
            a harness setting its size) -- computed once, a 1280x720 factor was
            applied to a 1739x978 window.
            """
            area = 1.0
            if self.screen:
                try:
                    pw, ph = renpy.get_physical_size()
                    area = (self.screen[0] * self.screen[1]) / float(max(1, pw * ph))
                except Exception:
                    area = 1.0
            self.area_x = area
            self.gpu_x_eff = self.gpu_x * area

        def _deactivate(self):
            self.pending = None
            if self.active:
                self._query_end()
            self.active = False
            self.key = None
            self.label = ""
            try:
                import pygame_sdl2
                pygame_sdl2.display._dse_key = None
            except Exception:
                pass
            if "dev_spec_overlay" in config.overlay_screens:
                config.overlay_screens.remove("dev_spec_overlay")
            renpy.restart_interaction()

        # ----- GL timer queries ----------------------------------------------

        def _gl_init(self):
            if self._gl is not None:
                return self._gl

            gl = False

            try:
                if renpy.get_renderer_info().get("renderer") != "gl2":
                    raise Exception("renderer is not desktop GL")

                lib = _dse_ct.WinDLL("opengl32")
                lib.wglGetCurrentContext.restype = _dse_ct.c_void_p
                lib.wglGetProcAddress.restype = _dse_ct.c_void_p
                lib.wglGetProcAddress.argtypes = [_dse_ct.c_char_p]
                lib.glGetError.restype = _dse_ct.c_uint

                ctx = lib.wglGetCurrentContext()
                if not ctx:
                    raise Exception("no current GL context")

                def proc(name, *sig):
                    p = lib.wglGetProcAddress(name)
                    if not p:
                        raise Exception("missing " + name.decode())
                    return _dse_ct.WINFUNCTYPE(*sig)(p)

                U = _dse_ct.c_uint
                gl = {
                    "lib": lib,
                    "ctx": ctx,
                    "gen": proc(b"glGenQueries", None, _dse_ct.c_int, _dse_ct.POINTER(U)),
                    "begin": proc(b"glBeginQuery", None, U, U),
                    "end": proc(b"glEndQuery", None, U),
                    "geti": proc(b"glGetQueryObjectiv", None, U, U, _dse_ct.POINTER(_dse_ct.c_int)),
                    "getu64": proc(b"glGetQueryObjectui64v", None, U, U, _dse_ct.POINTER(_dse_ct.c_uint64)),
                    "ival": _dse_ct.c_int(0),
                    "uval": _dse_ct.c_uint64(0),
                    }

                ids = (U * self.QUERIES)()
                gl["gen"](self.QUERIES, ids)
                self._q_free = [int(i) for i in ids]
                self._q_pending = []
                self._q_active = None
                self.gl_note = "gpu timer: on"

            except Exception as e:
                gl = False
                self.gl_note = "gpu timer: OFF (%s)" % (e,)

            self._gl = gl
            return gl

        def query_begin(self):
            """Called right after the render tree is built, before any draw."""

            gl = self._gl
            if not gl:
                return

            if self._q_active is not None:
                # A render tree that never reached a flip (a screenshot, say).
                gl["end"](_DSE_GL_TIME_ELAPSED)
                self._q_free.append(self._q_active)
                self._q_active = None

            if not self._q_free:
                self._poll_queries()
                if not self._q_free:
                    return

            qid = self._q_free.pop()
            lib = gl["lib"]
            for i in range(8):
                if not lib.glGetError():
                    break
            gl["begin"](_DSE_GL_TIME_ELAPSED, qid)
            if lib.glGetError():
                self._q_free.append(qid)
                self._gl = False
                self.gl_note = "gpu timer: OFF (glBeginQuery failed)"
                return
            self._q_active = qid

        def _query_end(self):
            gl = self._gl
            if not gl or self._q_active is None:
                return
            gl["end"](_DSE_GL_TIME_ELAPSED)
            self._q_pending.append(self._q_active)
            self._q_active = None

        def _poll_queries(self):
            """Collect finished queries in order, without ever waiting on one."""

            gl = self._gl
            if not gl:
                return
            ival = gl["ival"]
            uval = gl["uval"]
            while self._q_pending:
                qid = self._q_pending[0]
                gl["geti"](qid, _DSE_GL_QUERY_RESULT_AVAILABLE, _dse_ct.byref(ival))
                if not ival.value:
                    break
                gl["getu64"](qid, _DSE_GL_QUERY_RESULT, _dse_ct.byref(uval))
                self._gpu_ms = uval.value / 1000000.0
                self._q_free.append(self._q_pending.pop(0))

        def _heater_query(self, begin):
            """Time the heater on its own query pair, outside the frame's."""
            gl = self._gl
            if not gl:
                return
            hq = getattr(self, "_hq", None)
            if hq is None:
                ids = (_dse_ct.c_uint * 2)()
                gl["gen"](2, ids)
                hq = self._hq = [int(ids[0]), int(ids[1])]
                self._hq_live = [False, False]
                self._hq_i = 0
            if begin:
                i = self._hq_i
                if self._hq_live[i]:
                    ival = gl["ival"]
                    gl["geti"](hq[i], _DSE_GL_QUERY_RESULT_AVAILABLE, _dse_ct.byref(ival))
                    if not ival.value:
                        self._hq_skip = True
                        return
                    gl["getu64"](hq[i], _DSE_GL_QUERY_RESULT, _dse_ct.byref(gl["uval"]))
                    self._heater.gpu_ms = gl["uval"].value / 1000000.0
                self._hq_skip = False
                gl["begin"](_DSE_GL_TIME_ELAPSED, hq[i])
            else:
                if getattr(self, "_hq_skip", True):
                    return
                gl["end"](_DSE_GL_TIME_ELAPSED)
                self._hq_live[self._hq_i] = True
                self._hq_i = 1 - self._hq_i

        def _check_context(self):
            """A display reset can hand us a new context; queries die with it."""
            gl = self._gl
            if not gl:
                return
            if gl["lib"].wglGetCurrentContext() != gl["ctx"]:
                self._gl = None
                self._q_free = []
                self._q_pending = []
                self._q_active = None
                self._gl_init()

        # ----- per frame -----------------------------------------------------

        def add_idle(self, seconds):
            self._idle += seconds

        @staticmethod
        def _wait_until(deadline):
            while True:
                left = deadline - _dse_time.perf_counter()
                if left <= 0.0:
                    return
                if left > 0.002:
                    _dse_time.sleep(left - 0.0015)

        def before_flip(self):
            if self.pending is not None:
                self._activate()
                return

            now = _dse_time.perf_counter()

            self._check_context()
            self._query_end()
            self._poll_queries()
            if self._nvml is not None:
                self._clk = self._nvml.sample(now)
            if self.screen and now - self._area_at >= 0.5:
                self._area_at = now
                self._update_area()

            if self._t_flip is None:
                self._rec = None
                return

            # 1. Hold until the frame has cost what it would have there.
            cpu_ms = (now - self._t_flip - self._idle) * 1000.0
            if cpu_ms < 0.0:
                cpu_ms = 0.0
            gpu_ms = self._gpu_ms
            target = max(cpu_ms * self.cpu_x, gpu_ms * self.gpu_x_eff)
            stall = target - cpu_ms
            if stall > 0.05:
                self._wait_until(now + stall / 1000.0)
            else:
                stall = 0.0

            # 2. The 60Hz panel. The frame is shown on the first virtual vblank
            #    at or after the moment it is ready, and never on the same one
            #    as the frame before it. The flip blocks only until the frame
            #    before it is on screen (one may wait in the queue).
            shown = None
            if self.hz:
                period = 1.0 / self.hz
                ready = _dse_time.perf_counter()
                if self._grid0 is None:
                    self._grid0 = ready
                    self._n_prev = 0
                    n = 0
                else:
                    n = int(_dse_math.ceil((ready - self._grid0) / period - 1e-9))
                    if n <= self._n_prev:
                        n = self._n_prev + 1
                if self.QUEUE >= 1:
                    self._wait_until(self._grid0 + self._n_prev * period)
                else:
                    self._wait_until(self._grid0 + n * period)
                shown = (n - self._n_prev) * period * 1000.0
                self._n_prev = n

            self._rec = (cpu_ms, gpu_ms, target, stall, self._idle * 1000.0, shown)

        def after_flip(self):
            now = _dse_time.perf_counter()
            rec = self._rec
            if rec is not None and self._t_flip is not None:
                shown = rec[5]
                if shown is None:
                    shown = (now - self._t_flip) * 1000.0
                rec = rec[:5] + (shown, self._clk[0], self._clk[1])
                self.frames.append(rec)
                seg = self.segment
                if seg is not None:
                    seg["recs"].append(rec)
            self._rec = None
            heater = self._heater
            if heater is not None and self.pin:
                heater.tune(self._clk, self._nvml, now)
                self._heater_query(True)
                heater.run()
                self._heater_query(False)
                now = _dse_time.perf_counter()
            self._t_flip = now
            self._idle = 0.0

        # ----- reporting -----------------------------------------------------

        def period_ms(self):
            if self.hz:
                return 1000.0 / self.hz
            try:
                return 1000.0 / float(renpy.display.get_info().refresh_rate or 60.0)
            except Exception:
                return 1000.0 / 60.0

        def stats(self, recs=None):
            """
            Summary of (cpu, gpu, emulated, stall, idle, shown) records. `shown`
            is how long the frame was on screen (the virtual vblank interval on
            a 60Hz preset); `missed` counts frames shown for more than one
            vblank, i.e. a visible repeat.
            """

            recs = list(self.frames if recs is None else recs)
            if not recs:
                return {"frames": 0}

            def pct(vals, q):
                vals = sorted(vals)
                return vals[min(len(vals) - 1, int(len(vals) * q))]

            iv = [r[5] for r in recs]
            cpu = [r[0] for r in recs]
            gpu = [r[1] for r in recs]
            tgt = [r[2] for r in recs]
            period = self.period_ms()
            span = sum(iv)
            missed = sum(1 for v in iv if v > period * 1.5)
            gpu_bound = sum(1 for r in recs if r[1] * self.gpu_x_eff > r[0] * self.cpu_x)

            return {
                "frames": len(recs),
                "fps": (len(iv) * 1000.0 / span) if span > 0 else 0.0,
                "iv_mean": span / len(iv),
                "iv_p50": pct(iv, 0.50),
                "iv_p95": pct(iv, 0.95),
                "iv_p99": pct(iv, 0.99),
                "iv_max": max(iv),
                "missed": missed,
                "missed_pct": 100.0 * missed / len(iv),
                "cpu_mean": sum(cpu) / len(cpu),
                "cpu_p95": pct(cpu, 0.95),
                "cpu_max": max(cpu),
                "gpu_mean": sum(gpu) / len(gpu),
                "gpu_p95": pct(gpu, 0.95),
                "gpu_max": max(gpu),
                "emu_mean": sum(tgt) / len(tgt),
                "emu_p95": pct(tgt, 0.95),
                "emu_max": max(tgt),
                "gpu_bound_pct": 100.0 * gpu_bound / len(recs),
                "period": period,
            }

        def readout(self):
            if self.pending is not None:
                return "SPEC  %s  arming..." % self.label
            s = self.stats(list(self.frames)[-120:])
            head = "SPEC  %s  CPU x%.1f  GPU x%.1f%s  %s" % (
                self.label, self.cpu_x, self.gpu_x_eff,
                (" (area x%.2f)" % self.area_x) if abs(self.area_x - 1.0) > 0.01 else "",
                ("%dHz panel" % self.hz) if self.hz else "native refresh")
            if not s.get("frames"):
                return head
            bound = "GPU" if s["gpu_bound_pct"] >= 50.0 else "CPU"
            # GPU timings read high when the card has dropped out of its top
            # clocks (see THE CLOCK PIN), so say so next to the number.
            clk = ""
            nv = self._nvml
            if nv is not None and nv.ok and self._clk[0]:
                gr, mem = self._clk
                clk = "   gpu clk %d/%d MHz" % (gr, mem)
                if gr < 0.9 * nv.gr_max or mem < 0.9 * nv.mem_max:
                    clk += "  LOW CLOCKS: gpu reads high"
            return "%s\n%3.0f fps   p95 %5.1f ms   worst %5.1f   missed %4.1f%%   cpu %5.2f  gpu %5.2f ms   %s-bound%s" % (
                head, s["fps"], s["iv_p95"], s["iv_max"], s["missed_pct"],
                s["cpu_mean"], s["gpu_mean"], bound, clk)

        # ----- harness API ---------------------------------------------------

        def seg_begin(self, name):
            self.segment = {"name": name, "recs": []}

        def seg_end(self):
            seg = self.segment
            self.segment = None
            if seg is None:
                return None
            seg["stats"] = self.stats(seg["recs"])
            self.segments.append(seg)
            return seg


    DEV_SPEC = DevSpecEmulator()


    def _dse_install_hooks():
        """
        Wrap the four engine points the model needs. Idempotent and safe to
        call again after a script reload: each wrapper carries a `_dse` mark,
        and every wrapper finds the live emulator through
        pygame_sdl2.display._dse_hook rather than through a closure.
        """

        import pygame_sdl2

        disp = pygame_sdl2.display
        disp._dse_hook = DEV_SPEC

        if not getattr(disp.flip, "_dse", False):
            orig_flip = disp.flip

            def flip(*args, **kwargs):
                emu = disp._dse_hook
                if emu is None or not (emu.active or emu.pending is not None):
                    return orig_flip(*args, **kwargs)
                emu.before_flip()
                rv = orig_flip(*args, **kwargs)
                emu.after_flip()
                return rv

            flip._dse = True
            disp.flip = flip

        rmod = renpy.display.render
        if not getattr(rmod.render_screen, "_dse", False):
            orig_rs = rmod.render_screen

            def render_screen(*args, **kwargs):
                rv = orig_rs(*args, **kwargs)
                emu = disp._dse_hook
                if emu is not None and emu.active:
                    emu.query_begin()
                return rv

            render_screen._dse = True
            rmod.render_screen = render_screen

        iface = renpy.display.core.Interface
        if not getattr(iface.event_wait, "_dse", False):
            orig_ew = iface.event_wait

            def event_wait(self, *args, **kwargs):
                emu = disp._dse_hook
                if emu is None or not emu.active:
                    return orig_ew(self, *args, **kwargs)
                t0 = _dse_time.perf_counter()
                try:
                    return orig_ew(self, *args, **kwargs)
                finally:
                    emu.add_idle(_dse_time.perf_counter() - t0)

            event_wait._dse = True
            iface.event_wait = event_wait

        ptime = pygame_sdl2.time
        if not getattr(ptime.wait, "_dse", False):
            orig_wait = ptime.wait

            def wait(*args, **kwargs):
                emu = disp._dse_hook
                if emu is None or not emu.active:
                    return orig_wait(*args, **kwargs)
                t0 = _dse_time.perf_counter()
                try:
                    return orig_wait(*args, **kwargs)
                finally:
                    emu.add_idle(_dse_time.perf_counter() - t0)

            wait._dse = True
            ptime.wait = wait


    def dev_spec_select(key):
        DEV_SPEC.select(key)


    def dev_spec_toggle_overlay():
        DEV_SPEC.overlay = not DEV_SPEC.overlay
        renpy.restart_interaction()


    class DevSpecReadout(renpy.Displayable):
        """
        The overlay line. Re-lays its text once a second, no more: every new
        Text is a new texture, and texture churn shows up in the GPU timer as
        1-4ms spikes (measured -- at 4Hz this readout was the ONLY source of
        GPU spikes in Kotonoha's stage). Harness runs switch it off.
        """

        _plate = Solid("#000000b0")

        def __init__(self, **kwargs):
            super(DevSpecReadout, self).__init__(**kwargs)
            self._d = None
            self._at = -1.0

        def render(self, width, height, st, at):
            now = _dse_time.perf_counter()
            if self._d is None or now - self._at >= 1.0:
                self._at = now
                self._d = Text(DEV_SPEC.readout(), font=gui.interface_font,
                    size=13, color="#d8f6ff", line_spacing=1)
            tr = renpy.render(self._d, 1240, 60, st, at)
            w, h = tr.get_size()
            rv = renpy.Render(int(w) + 14, int(h) + 8)
            rv.blit(renpy.render(self._plate, int(w) + 14, int(h) + 8, st, at), (0, 0))
            rv.blit(tr, (7, 4))
            renpy.redraw(self, 1.0)
            return rv


    DEV_SPEC_READOUT = DevSpecReadout()


init 60 python:

    # Two ways in without the hub: the environment (stress harnesses), and a
    # preset left armed across a Shift+R.
    def _dse_boot():
        import os
        import pygame_sdl2

        if not config.developer:
            return

        disp = pygame_sdl2.display
        key = os.environ.get("ENTER_M_SPEC") or getattr(disp, "_dse_key", None)

        if key and dev_spec_preset(key):
            DEV_SPEC.select(key)
        elif getattr(disp, "_dse_hook", None) is not None:
            # Hooks left from before a reload, with the emulator off: point
            # them at this instance so they stop holding the old one.
            _dse_install_hooks()

    _dse_boot()


screen dev_spec_overlay():
    zorder 32001
    if DEV_SPEC.overlay and (DEV_SPEC.active or DEV_SPEC.pending is not None):
        add DEV_SPEC_READOUT xpos 6 yalign 1.0 yoffset -6
