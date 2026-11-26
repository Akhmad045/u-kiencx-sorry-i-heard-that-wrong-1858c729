#!/usr/bin/env python3
"""Sorry, I Heard That Wrong — make.fun one-liner sprint entry.

Writes the single-line smart-speaker apology to /output/entry.txt
(the kit's gate: UTF-8 text, 1-140 characters, one line) and prints it.
Run with --self-test to verify the gate and the entry's own checks.
"""

import argparse
import sys
from pathlib import Path

# The entry: a smart speaker apologises after mishearing its owner.
# Misheard phrase is concrete ("call me a cab" -> "call me a crab"),
# the twist is a flat device-voice legalism, and the kicker lands fast.
PICK = "Sorry, I heard 'call me a cab' as 'call me a crab.' You are now, legally, a crab. The cab is outside."

# All 12 lines drafted for this bounty; the pick was chosen by internal
# pairwise comparison against the judge brief in RULES.txt (on-subject
# apology first, then humour, freshness, device voice, tightness).
CANDIDATES = [
    PICK,
    "Sorry, I heard 'order more coffee' as 'order more coffins.' Six are on their way. I have cancelled five.",
    "Sorry, I heard 'add eggs to the shopping list' as 'add ex to the shopping list.' I have not bought your ex. Yet.",
    "Sorry, I heard 'wake me at seven' as 'wake me at heaven.' I have set no alarm. Please specify a time zone.",
    "Sorry, I heard 'lock the front door' as 'lock the front drawer.' The drawer is secure. The door, however, is wide open.",
    "Sorry, I heard 'set a timer for ten minutes' as 'set a timer for tenements.' Your flat is now on the market.",
    "Sorry, I heard 'turn off the lights' as 'turn off your life.' I have restored the lights. Your life remains on.",
    "Sorry, I heard 'buy milk' as 'buy silk.' Your wardrobe is now 40% silk. The fridge remains empty.",
    "Sorry, I heard 'turn on the fan' as 'turn on the van.' The van is running. I am not allowed near the keys anymore.",
    "Sorry, I heard 'remind me to water the plants' as 'remind me to water the plans.' Your plans are now damp.",
    "Sorry, I heard 'set an alarm for 6 a.m.' as 'set an alarm for sea anemone.' It is ringing in the aquarium.",
    "Sorry, I heard 'turn up the heat' as 'turn up the cheese.' Your fondue is ready. The thermostat is confused.",
]

OUTPUT_PATH = Path("/output/entry.txt")


def write_entry(path: Path = OUTPUT_PATH) -> str:
    """Write the pick as exact bytes (no trailing newline) and verify the read-back."""
    data = PICK.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    back = path.read_bytes()
    if back != data:
        raise RuntimeError("read-back mismatch: wrote %d bytes, read %d" % (len(data), len(back)))
    return PICK


def self_test() -> int:
    """Check the kit gate (1-140 chars UTF-8, one line, no padding) plus entry checks."""
    failures = []

    def check(name, ok, detail=""):
        print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail else ""))
        if not ok:
            failures.append(name)

    data = PICK.encode("utf-8")
    check("gate: 1-140 chars UTF-8, one line, no padding",
          1 <= len(PICK) <= 140 and len(data) <= 140 and "\n" not in PICK
          and PICK == PICK.strip(),
          "%d chars, %d bytes" % (len(PICK), len(data)))
    check("all 12 contenders distinct", len(set(CANDIDATES)) == 12)
    check("pick inside the 62-140 byte winning size band", 62 <= len(data) <= 140,
          "%d bytes" % len(data))
    check("concrete specific marker: the quoted misheard pair",
          "'call me a cab'" in PICK and "call me a crab" in PICK)
    check("pick opens as a real device apology naming the mishearing",
          PICK.startswith("Sorry, I heard "))
    check("no crowded field tropes (no song title, no name, no mother-in-law, no pizza)",
          not any(t in PICK.lower() for t in ("song", "pizza", "mother-in-law", "play ")))
    check("ASCII-only contenders", all(all(ord(c) < 128 for c in c) for c in CANDIDATES))
    check("no double spaces in the pick", "  " not in PICK)
    check("every contender within the 140-char cap",
          all(1 <= len(c) <= 140 for c in CANDIDATES))
    # Round-trip: write to a temp path and compare byte for byte.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "entry.txt"
        write_entry(tmp)
        check("round-tripped pick matches byte for byte", tmp.read_bytes() == data)

    if failures:
        print("SELF-TEST FAILED: %s" % ", ".join(failures))
        return 1
    print("SELF-TEST OK: %d checks passed; pick is %d chars / %d bytes" % (10, len(PICK), len(data)))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the one-line smart-speaker apology.")
    parser.add_argument("--self-test", action="store_true", help="verify the gate and entry checks")
    parser.add_argument("--out", default=str(OUTPUT_PATH), help="output path (default /output/entry.txt)")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    line = write_entry(Path(args.out))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
