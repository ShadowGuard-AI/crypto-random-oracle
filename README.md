![The empty course in early light: numbered starting ends swept and empty with a kneeling pad in one lane and a spray bottle in another, chairs of the early spectators mostly unoccupied, and the steward table at the far end with the lettuce waiting under a glass cover, with no lettering](intro-banner.png)

# crypto-random-oracle

Title block: the name above is set in Bitcount Prop Double in kingfisher teal on a river white race card plate, ruled beneath with a fine line, with a small painted shell beside the first heading only and nowhere repeated as decoration.

![A racing snail in profile before a race, shell high and rounded carrying a painted racing number, eyestalks raised and turned slightly towards the viewer, foot flat on the lane, and a single lettuce leaf laid before it, with the name hand lettered below in the field guide manner](logo.png)

![Race day assembled: lanes running the length of a prepared strip, a crowd with chairs on both sides, a finishing line under a small gantry and the lettuce on the steward table beside it, entrants waiting at the near end, and the largest entrant carrying the only lettering, the name painted along its shell](banner.png)

![The course in three bands: bunting stirring and a bead of condensation gathering on the lettuce cover in the far band, entrants advancing along their lanes at racing pace in the middle band, the steward pencil moving along the results book and one lettuce leaf settling to the table in the near band](scene.svg)

![Major separator](sep-heavy.svg)

# crypto-random-oracle
Simulates a random oracle for cryptographic research and testing, outputting random values based on input with configurable entropy. - Focused on Basic cryptographic operations

> Steward's note, read aloud before the card proceeds: the input is required. A run without an input is refused by the parser before any output exists.

## Install
`git clone https://github.com/ShadowStrikeHQ/crypto-random-oracle`

> Steward's note: under fixed conditions the finishes are identical. Supply a salt, or supply a key, and asking again prints the same line again, which is expected behaviour and not several results standing in a row.

## Usage
`python3 main.py [params]`

> Steward's note: a keyed run has a ceiling. The output is a single digest cut to the requested length, so a length longer than the digest cannot be answered and the run refuses with that reason.

![Minor separator](sep-light.svg)

Without a key the output is HKDF over the chosen hash and can be any
positive length. With `-k` the output is a single HMAC digest cut to
the requested length, so the length cannot exceed the digest size
(32 bytes for SHA256); a longer request fails with that reason instead
of printing a short output. A salt has no effect in HMAC mode and the
tool warns when one is supplied with a key.

> Steward's note, a handling fact: the program logs its configuration as it runs, including the input string itself in plain words, while recording of the key only whether one was provided. Anyone keeping logs should keep that in mind.

## Parameters
- `-h`: Show help message and exit
- `-i`: The input string to the random oracle.
- `-l`: The length of the output in bytes (default: 32).
- `-s`: An optional salt for the random oracle. If not provided, a random salt is generated.
- `-n`: Number of outputs to generate for the same input and configuration.
- `-k`: An optional key for the HMAC. If not provided HMAC will not be used.
- `-a`: Hash algorithm to use (default: SHA256).

## License
Copyright (c) ShadowStrikeHQ

![Minor separator](sep-light.svg)

![Major separator](sep-heavy.svg)

## Facts from the code, stated in the prose

Facts from the code, stated in the prose. This record names: HKDF, HMAC, SHA256, SHA384, SHA512, BLAKE2b, cryptography>=41.0.7, -h, --help, -i, --input, -l, --length, -s, --salt, -n, --num_outputs, -k, --key, -a, --algorithm, exit code 1. The default output length is 32 bytes and the default number of outputs is 1. When no salt is supplied, a random salt of 16 bytes is generated inside each call. For BLAKE2b the code asks that hash for its full 64 byte width whatever length was requested. The program logs its input string in plain words, stated here as a behaviour only; no input value, key, salt value, or output value is printed on this page or in this record.
