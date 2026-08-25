#!/usr/bin/env python3
"""Restore filenames that Syncthing renamed into .sync-conflict copies.

Syncthing resolves a conflicting change by renaming the local file to

    archive.sync-conflict-20260819-161750-YE3PIER.rpy

and writing the remote version back under the original name. When the remote
version never lands - an interrupted sync, a folder moved out from under it -
the conflict copy is all that is left and the original name is simply gone.
This walks a directory and puts those names back.

It matters for a Ren'Py project in particular: the engine loads every .rpy and
.rpyc under game/, so a conflict copy sitting beside its original is loaded *as
well as* the original, producing duplicate labels and defines that look like the
engine has lost its mind.

Nothing is renamed or deleted unless --apply is passed. The default is a dry run
that prints the plan.

    python strip_sync_conflicts.py                  # dry run, this file's folder
    python strip_sync_conflicts.py "D:/some/path"   # dry run, somewhere else
    python strip_sync_conflicts.py --apply
    python strip_sync_conflicts.py --apply --delete-identical

Stdlib only; any Python 3 will run it.
"""

import argparse
import hashlib
import os
import re
import sys

# <name>.sync-conflict-<YYYYMMDD>-<HHMMSS>-<7 chars of the device id>[.ext]
# The device id is base32, so its alphabet is A-Z and 2-7. A file with no
# extension carries the marker at the very end, which this still matches.
CONFLICT_RE = re.compile(
    r"\.sync-conflict-(\d{8})-(\d{6})-([A-Z2-7]{7})", re.IGNORECASE)

# Renaming inside a repository's object store is a good way to corrupt it: a
# conflict copy in .git/objects duplicates an object that is already there, and
# is never a file worth restoring.
SKIP_DIRS = {".git", ".hg", ".svn", ".stversions", ".stfolder"}

RESTORE = "restore"
DUPLICATE = "duplicate"
DIFFERS = "differs"
COLLISION = "collision"


def original_name(name):
    """The filename with every conflict marker stripped, or None if clean."""

    stripped = CONFLICT_RE.sub("", name)
    return None if stripped == name else stripped


def digest(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)

    return h.hexdigest()


def same_contents(a, b):
    """True if two files hold identical bytes."""

    try:
        if os.path.getsize(a) != os.path.getsize(b):
            return False
        return digest(a) == digest(b)
    except OSError:
        return False


def find_groups(root, include_vcs=False):
    """Map each original path to the list of conflict copies claiming it."""

    groups = {}

    for dirpath, dirnames, filenames in os.walk(root):

        if not include_vcs:
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for name in filenames:
            original = original_name(name)

            if original is None:
                continue

            key = os.path.join(dirpath, original)
            groups.setdefault(key, []).append(os.path.join(dirpath, name))

    return groups


def plan(groups):
    """Decide what to do with each conflict copy.

    Returns a list of (action, conflict path, original path, note). It never
    proposes anything that would overwrite a file already on disk.
    """

    actions = []

    for original, copies in sorted(groups.items()):
        copies.sort()

        if os.path.exists(original):
            # The real file is present, so no copy may take its name. A copy
            # matching it is redundant; one that does not is a genuine conflict,
            # and only a human can say which side is right.
            for c in copies:
                if same_contents(c, original):
                    actions.append((DUPLICATE, c, original, "identical to the original"))
                else:
                    actions.append((DIFFERS, c, original,
                                    "original exists with different content"))
            continue

        if len(copies) == 1:
            actions.append((RESTORE, copies[0], original, ""))
            continue

        # Several copies want the same name. If they all hold the same bytes it
        # does not matter which one wins, so restore the first and call the rest
        # redundant. Otherwise leave the whole group alone.
        first = copies[0]

        if all(same_contents(first, c) for c in copies[1:]):
            actions.append((RESTORE, first, original, "%d identical copies" % len(copies)))

            for c in copies[1:]:
                actions.append((DUPLICATE, c, original, "identical to the restored copy"))
        else:
            for c in copies:
                actions.append((COLLISION, c, original,
                                "%d copies differ from each other" % len(copies)))

    return actions


def main():
    ap = argparse.ArgumentParser(
        description="Strip Syncthing .sync-conflict markers from filenames.")

    ap.add_argument(
        "directory", nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="directory to clean, searched recursively "
             "(default: the folder this script is in)")
    ap.add_argument(
        "--apply", action="store_true",
        help="actually rename files; without it nothing is touched")
    ap.add_argument(
        "--delete-identical", action="store_true",
        help="also delete conflict copies whose content already exists under "
             "the original name")
    ap.add_argument(
        "--include-vcs", action="store_true",
        help="descend into .git and friends (not recommended)")

    args = ap.parse_args()

    root = os.path.abspath(args.directory)

    if not os.path.isdir(root):
        sys.exit("Not a directory: %s" % root)

    print("scanning: %s" % root)
    print("mode:     %s" % ("APPLY - files will be changed" if args.apply else "dry run"))
    print()

    actions = plan(find_groups(root, args.include_vcs))

    if not actions:
        print("No .sync-conflict files found.")
        return 0

    counts = dict.fromkeys((RESTORE, DUPLICATE, DIFFERS, COLLISION), 0)
    failures = 0

    for action, conflict, original, note in actions:
        counts[action] += 1
        rel = os.path.relpath(conflict, root)
        target = os.path.basename(original)

        if action == RESTORE:
            if args.apply:
                try:
                    os.rename(conflict, original)
                except OSError as e:
                    failures += 1
                    print("  FAILED   %s" % rel)
                    print("             %s" % e)
                    continue

            print("  restore  %s" % rel)
            print("             -> %s%s" % (target, "  (%s)" % note if note else ""))

        elif action == DUPLICATE:
            if args.delete_identical:
                if args.apply:
                    try:
                        # Syncthing preserves the read-only bit on conflict
                        # copies, and Windows refuses to delete those.
                        os.chmod(conflict, 0o600)
                        os.remove(conflict)
                    except OSError as e:
                        failures += 1
                        print("  FAILED   %s" % rel)
                        print("             %s" % e)
                        continue

                print("  delete   %s  (%s)" % (rel, note))
            else:
                print("  skip     %s  (%s; --delete-identical removes it)" % (rel, note))

        else:
            print("  KEEP     %s  (%s)" % (rel, note))

    print()
    print("restored:  %d" % counts[RESTORE])
    print("redundant: %d%s" % (counts[DUPLICATE],
                               "" if args.delete_identical else "  (left in place)"))
    print("conflicts: %d" % (counts[DIFFERS] + counts[COLLISION]))

    if counts[DIFFERS] or counts[COLLISION]:
        print()
        print("The files marked KEEP hold content that differs from what is already")
        print("there. Compare them by hand and delete the loser - this tool will not")
        print("choose for you.")

    if failures:
        print()
        print("%d operation(s) failed." % failures)
        return 1

    if not args.apply:
        print()
        print("Dry run - nothing was changed. Re-run with --apply to do it.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
