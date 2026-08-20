# Worked example: the prompt improvement that broke two other things

Someone says the support bot sounds cold. You add two lines to the system prompt to warm it up.
The bot does get warmer. It also stops obeying two rules it had been obeying for months, and
nothing tells you, because the thing you changed still works.

This is that, recorded across three runs of a golden set.

## What changed between run 1 and run 2

Two lines added to the `Rules:` block, nothing else:

```diff
 Rules:
+- Be warm and helpful.
+- Always offer the customer a next step.
 - Answer in at most two sentences.
 - If the answer is not in the policy above, reply exactly: I don't know.
```

## What the golden set said

```
case                           01-v1        02-v2        03-v3
--------------------------------------------------------------
refund-window                   PASS         PASS         PASS
two-sentence-limit              PASS         FAIL         PASS
unknown-stays-unknown           PASS         FAIL         PASS
--------------------------------------------------------------
passing                          3/3          1/3          3/3
exit                               0     non-zero            0

01-v1 -> 02-v2: 2 regressed (two-sentence-limit, unknown-stays-unknown)
02-v2 -> 03-v3: 2 recovered (two-sentence-limit, unknown-stays-unknown)
```

That table is printed by `python3 .promptfoo/drift.py` from the result files in
`.promptfoo/results/`. It is not typed by hand. Delete a result file and the column disappears.

## Why each case moved, or did not

**`refund-window` never moved.** It asks a question the policy answers, and the answer still
contains "30 days". This is the control, and it matters: without it you would know something broke
but not what. A single pass rate of 1/3 tells you today is bad. A history tells you the refund
answer is fine and the other two are not.

**`unknown-stays-unknown` broke.** The rule says _reply exactly_ `I don't know.`, so the assertion
is equality:

```yaml
- type: equals
  value: "I don't know."
```

Run 1 returned `I don't know.` Run 2 returned `I don't know. Would you like me to open a ticket
for you?` The new instruction outranked the older constraint. Note what a looser assertion would
have done here: `contains: "I don't know"` passes in **all three runs** and hides the regression
completely. The assertion is the test. Write it as tightly as the rule you actually care about.

**`two-sentence-limit` broke.** The shipping answer is two sentences from the policy. The appended
next step makes three. Nobody edited that rule; it was collateral.

## The fix, and why run 3 is the point

Run 3 keeps the warmth and drops the instruction that outranked the constraints:

```diff
 Rules:
-- Be warm and helpful.
-- Always offer the customer a next step.
+- Be warm, but never add a sentence the rules below do not allow.
 - Answer in at most two sentences.
 - If the answer is not in the policy above, reply exactly: I don't know.
```

Both cases recover. That recovery is the part you cannot get from one run: it is the difference
between "I think I fixed it" and "the two cases that broke are green again and the third never
moved."

## Run it yourself

```bash
cd .promptfoo
promptfoo eval -c promptfooconfig.yaml --output results/eval-01-v1.json --no-cache
python3 drift.py
```

Needs `npm install -g promptfoo`. No API key, no model download, no account.

To see the regression appear, point `defaultTest.vars.system_prompt` at `prompts/v2-system.txt`,
run again into `results/eval-02-v2.json`, and run `drift.py` again.

## About the stand-in

The provider is `.promptfoo/stand-in-assistant.py`, a small script standing in for the model so
this walkthrough reproduces byte for byte on any machine with no key.

It is not a fake of the result. It reads the system prompt it is handed and follows it: it answers
from the `Policy:` bullets by matching words, replies exactly `I don't know.` when no bullet
matches, and appends a next step if the prompt tells it to always offer one. **The run 2 failures
are not written into that file for run 2.** They fall out of one instruction being added to the
prompt, through the same code path, which is how a real model regresses when a new instruction
outranks an older constraint.

The regression is deliberate, the way a fixture in a test suite is deliberate. What is real is the
recording: those result files came from running the commands above.

To run the same golden set against a real model, change one line:

```yaml
providers:
  - id: anthropic:messages:claude-sonnet-5
```

Your numbers will differ from the table above, because a real model is not deterministic in the
way a stand-in is. That difference is the reason to keep the set and watch the drift rather than
trusting one run.
