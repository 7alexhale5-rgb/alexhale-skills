# Alex Hale — Agent Skills

Original agent skills, source-checked before release. This marketplace holds the free tier.

## Install

As a Claude Code plugin:

```
/plugin marketplace add 7alexhale5-rgb/alexhale-skills
/plugin install regression-test@alexhale-skills
```

Run `/reload-plugins` after an update.

Or with the `skills` CLI, which works across Claude Code, Cursor, Codex CLI, Gemini CLI and
Copilot:

```
npx skills add 7alexhale5-rgb/alexhale-skills@regression-test
```

Both paths install the same file. The `skills/` and `plugins/` folders are generated from one
source, so they cannot drift apart.

## What is here

### Regression Test

You improved the prompt. Something else got worse, and you found out from a user.

It keeps a golden set of the cases that matter, committed next to your code, and shows which
ones moved across your last five runs. One score tells you about today. A history tells you what
your change did.

Four commands: `init`, `add`, `run`, `report`. It scaffolds its own config, so there is nothing
to wire up first.

It exits clean when the set passes and non-zero when it does not, so a build can fail on a
prompt the way it fails on a test. Checked by running it: a passing set exited `0`, and breaking
one case took the same set to exit `100`, with a JSON result file written both times.

There are good skills for authoring and running a single promptfoo eval, including one from
promptfoo themselves. This one is for the other job: keeping the set, committing it, and reading
the drift between runs.

### See it before you build your own set

[`example/`](example/) is a recorded three-run walkthrough. Two lines get added to a support
bot's prompt to make it warmer; two unrelated rules quietly break; a third case never moves, which
is how you can tell what actually changed.

```
case                          run 1        run 2        run 3
------------------------------------------------------------
refund-window                  PASS         PASS         PASS
two-sentence-limit             PASS         FAIL         PASS
unknown-stays-unknown          PASS         FAIL         PASS
------------------------------------------------------------
passing                         3/3          1/3          3/3
exit                              0     non-zero            0
```

It runs on your machine with no API key and no model download, and that table is printed from the
result files rather than typed.

Needs [promptfoo](https://promptfoo.dev): `npm install -g promptfoo`.

## Why the list is short

Every skill here passed a source and name review: we checked it against public projects with
file hashes and text comparison, checked the name, and recorded the result. Work that failed
that review is not published, whatever it cost to build. Eight skills are held back right now
for exactly that reason.

A short list of work we own outright is worth more than a long list we cannot stand behind.

## Terms

Free to use, on your own work, on as many machines as you like. Do not resell it or republish it
as your own. That is the whole of it, in plain language rather than legal language.

## Problems

Open an issue. `claude plugin validate --strict plugins/<name>` checks a local copy.

More, including the paid skills, at [skillfactory.prettyflyforai.com](https://skillfactory.prettyflyforai.com).
