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

This turns your prompts into a golden test set you can re-run. Capture the cases that matter,
run them after every change, and see which ones moved. It will not write your prompts. It tells
you which change broke which case, before you ship it.

Four commands: `init`, `add`, `run`, `report`. It scaffolds its own config, so there is nothing
to wire up first.

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
