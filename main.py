#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes a single Wi-Fi network name to /output/entry.txt.

Entry: "My WiFi Has a Restraining Order" (31 characters).
The joke: a Wi-Fi network so plagued by freeloaders that it needed a
legal restraining order — a whole story (a situation, a character, and
something that happened) in one network name.

Deterministic: no network, no randomness, no time dependence.
The output is always the exact same 31 characters.
"""

import os

ENTRY = "My WiFi Has a Restraining Order"


def main() -> None:
    # Gate check, mirroring the sealed scorer: UTF-8 text of 1 to 32
    # characters, not only white space, a single line.
    assert isinstance(ENTRY, str)
    assert 1 <= len(ENTRY) <= 32, f"entry must be 1-32 chars, got {len(ENTRY)}"
    assert ENTRY.strip(), "entry must not be only white space"
    assert "\n" not in ENTRY and "\r" not in ENTRY, "entry must be one line"
    assert ENTRY == ENTRY.strip(), "entry must not have leading/trailing space"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Write via a temp file + atomic rename so a partial write can never
    # leave a truncated entry.txt behind.
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    os.replace(tmp_path, out_path)

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    assert written == ENTRY.encode("utf-8"), "written bytes differ from entry"

    print(f"entry: {ENTRY}")
    print(f"characters: {len(ENTRY)}")
    print(f"bytes: {len(written)}")
    print(f"wrote: {out_path}")


if __name__ == "__main__":
    main()
