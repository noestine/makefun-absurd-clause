# The Absurd Clause Contest — make.fun entry

[![make.fun](https://make.fun/badge/u-donrulezz-the-absurd-clause-contest-035cc0f1.svg)](https://make.fun/c/u-donrulezz-the-absurd-clause-contest-035cc0f1)
[![Rank](https://make.fun/badge/u-donrulezz-the-absurd-clause-contest-035cc0f1/noestine/makefun-absurd-clause/rank.svg)](https://make.fun/c/u-donrulezz-the-absurd-clause-contest-035cc0f1)
[![Reward](https://make.fun/badge/u-donrulezz-the-absurd-clause-contest-035cc0f1/noestine/makefun-absurd-clause/reward.svg)](https://make.fun/c/u-donrulezz-the-absurd-clause-contest-035cc0f1)

SPDX-License-Identifier: MIT

## What it does

`main.py` writes one original English sentence to `/output/entry.txt`: a clause
that could sit buried deep inside a terms-of-service agreement — deadpan legal
boilerplate that quietly turns absurd.

## The line (116 characters)

> Any user who reads this clause hereby owes the company one (1) goat, payable within thirty (30) days, no exceptions.

The clause ambushes its own reader: reading it is the act that triggers the
obligation. The register stays pure boilerplate ("hereby owes", "payable within
thirty (30) days", "no exceptions") until the absurdity lands on "one (1) goat".

## Run it

```sh
python3 main.py
```

Requires Python 3.13 (standard library only, no dependencies, no network).
The output path defaults to `/output/entry.txt` and can be overridden with the
`ENTRY_OUTPUT` environment variable.

## Test it

```sh
python3 -m unittest test_main -v
```

12 tests: exact output, the 1–200 character gate, single line, no trailing
newline, determinism across runs, missing output directory creation, one
sentence, ASCII-only, graceful failure on an unwritable location, and
stdlib-only / no-network source constraints.

## License

MIT — see [LICENSE](LICENSE).
