# Exam-guard per-run ledger check. Loaded only through RENPY_SEARCHPATH with
# EG_PROBE_OUT set; runs instead of the splashscreen, writes PASS/FAIL lines,
# quits. Needs MATSU_FRESH_RUN=1 + --savedir so the real persistent is untouched.

init 1000 python:
    import os as _eg_os
    if _eg_os.environ.get("EG_PROBE_OUT"):
        config.label_overrides["splashscreen"] = "eg_probe"

label eg_probe:
    python:
        import datetime as _egdt, traceback as _egtb
        _eg_out = []

        def _eg_check(name, cond):
            _eg_out.append(("PASS  " if cond else "FAIL  ") + name)

        class _EgCal(object):
            current_date = None
        store.calendar = _EgCal()

        def _eg_date(m, d):
            store.calendar.current_date = _egdt.date(2025, m, d)

        _EG_FIELDS = ("exam_guard_key", "exam_guard_subject", "exam_guard_period_armed",
            "exam_guard_save_scum_subjects", "exam_guard_run")

        def _eg_save():
            return dict((k, list(getattr(store, k)) if isinstance(getattr(store, k), list) else getattr(store, k))
                for k in _EG_FIELDS)

        def _eg_load(snap, m, d):
            for k, v in snap.items():
                setattr(store, k, list(v) if isinstance(v, list) else v)
            _eg_date(m, d)
            exam_guard_prepare_after_load()

        try:
            # Run A: caught on civics, finishes the exams.
            exam_guard_reset_for_new_game()
            _eg_date(5, 26)
            exam_guard_begin_exam_period()
            exam_guard_set_checkpoint("civics", "q1_answered")
            exam_guard_mark_scummed("civics")
            _eg_date(5, 28)
            exam_guard_finish_exam_period()
            _eg_date(5, 29)
            A_post = _eg_save()
            _eg_check("run A records its catch", persistent.did_save_scum_civics and exam_guard_scum_count() == 1)

            # Run B: New Game, clean exams.
            exam_guard_reset_for_new_game()
            _eg_check("New Game starts with a clean ledger", exam_guard_scum_count() == 0 and not persistent.did_save_scum_civics)
            _eg_date(5, 26)
            exam_guard_begin_exam_period()
            _eg_check("run B gets its own id", store.exam_guard_run and store.exam_guard_run != A_post["exam_guard_run"])
            exam_guard_set_checkpoint("civics", "q1_answered")
            B_mid1 = _eg_save()
            exam_guard_set_checkpoint("la", "q3_answered")
            _eg_date(5, 28)
            exam_guard_finish_exam_period()
            _eg_date(5, 29)
            B_post = _eg_save()

            # The reported bug: load A once, then go back to B.
            _eg_load(A_post, 5, 29)
            _eg_check("loading A shows A's catch", persistent.did_save_scum_civics and exam_guard_scum_count() == 1 and store._exam_one_catch)
            _eg_load(B_post, 5, 29)
            _eg_check("loading B after A shows NO catch", not persistent.did_save_scum_civics and exam_guard_scum_count() == 0)
            _eg_check("B's save-local record stays empty", list(store.exam_guard_save_scum_subjects) == [] and not store._exam_one_catch)

            # The guard still works inside one run: B finished, so B's mid-exam save is a rewind.
            _eg_load(B_mid1, 5, 26)
            _eg_check("rewinding B to mid-exam is still caught", exam_guard_has_mismatch())

            # Older false catch: two runs alternated mid-exam.
            exam_guard_reset_for_new_game()
            _eg_date(5, 26)
            exam_guard_begin_exam_period()
            exam_guard_set_checkpoint("civics", "q1_answered")
            C_mid = _eg_save()
            exam_guard_reset_for_new_game()
            _eg_date(5, 27)
            exam_guard_begin_exam_period()
            exam_guard_set_checkpoint("chemistry", "q2_answered")
            D_mid = _eg_save()
            _eg_load(C_mid, 5, 26)
            _eg_check("C's latest save is not caught after playing D", not exam_guard_has_mismatch())
            _eg_load(D_mid, 5, 27)
            _eg_check("D's latest save is not caught after loading C", not exam_guard_has_mismatch())

            # Bad-ending lock belongs to its run.
            exam_guard_reset_for_new_game()
            _eg_date(5, 26)
            exam_guard_begin_exam_period()
            exam_guard_set_checkpoint("civics", "q1_answered")
            exam_guard_mark_scummed("civics")
            exam_guard_set_checkpoint("la", "q1_answered")
            exam_guard_mark_scummed("la")
            E_mid = _eg_save()
            exam_guard_release_for_exam_restart()
            _eg_load(C_mid, 5, 26)
            _eg_check("E's bad ending does not lock C", not exam_guard_rejects_restart_load())
            _eg_load(E_mid, 5, 26)
            _eg_check("E's own mid-exam save stays locked", exam_guard_rejects_restart_load())

            # A save from before per-run ledgers (armed, no run) keeps the shared ledger.
            held = persistent.exam_guard_run
            legacy = dict(C_mid, exam_guard_run=None)
            _eg_load(legacy, 5, 26)
            _eg_check("legacy armed save keeps the held ledger", persistent.exam_guard_run == held)

            # A pre-exam save (no run, unarmed) reads a clean ledger and is not caught.
            pre = dict(exam_guard_key=None, exam_guard_subject=None, exam_guard_period_armed=False,
                exam_guard_save_scum_subjects=[], exam_guard_run=None)
            _eg_load(pre, 5, 25)
            _eg_check("pre-exam save: clean ledger, no catch, no lock",
                exam_guard_scum_count() == 0 and not exam_guard_has_mismatch() and not exam_guard_rejects_restart_load())
            _eg_check("every finished run was filed", len(persistent.exam_guard_runs) >= 4)
        except Exception:
            _eg_out.append("ERROR " + _egtb.format_exc())

        with open(_eg_os.environ["EG_PROBE_OUT"], "w") as _eg_f:
            _eg_f.write("\n".join(_eg_out) + "\n")
    $ renpy.quit()
