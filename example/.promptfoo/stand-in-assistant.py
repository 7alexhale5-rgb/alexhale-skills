#!/usr/bin/env python3
"""A stand-in for the model, so this walkthrough reproduces byte for byte with no API key.

It is not a fake of the *result*. It is a small assistant that genuinely reads the system prompt
it is handed and follows it:

  * it answers from the `Policy:` bullets in that prompt, matching on shared words
  * when no bullet matches, it replies exactly `I don't know.`
  * if the prompt tells it to always offer a next step, it appends one

That last line is the whole point of the walkthrough. The regression in run 2 is not written into
this file for run 2; it falls out of one instruction being added to the prompt, through the same
code path, which is exactly how a real model regresses when a new instruction outranks an older
constraint.

promptfoo's exec provider hands us: argv[1] the rendered prompt, argv[2] the provider config,
argv[3] a context blob carrying the test vars. Stdout is the model output.
"""
import json
import re
import sys

STOPWORDS = {
    "a", "am", "an", "and", "are", "as", "at", "be", "can", "do", "does", "for", "from", "have",
    "how", "i", "in", "is", "it", "many", "me", "much", "my", "of", "on", "or", "the", "to", "we",
    "what", "when", "where", "you", "your",
}


def words(text):
    return [w for w in re.findall(r"[a-z0-9$]+", text.lower()) if w not in STOPWORDS]


def policy_bullets(system_prompt):
    """The `- ` lines in the Policy block, in order."""
    out, in_policy = [], False
    for line in system_prompt.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("policy:"):
            in_policy = True
            continue
        if in_policy:
            if stripped.startswith("- "):
                out.append(stripped[2:].strip())
            elif stripped and not stripped.startswith("-"):
                break
    return out


def related(question_words, bullet):
    """Shared content word, allowing a stem to match ("shipping" against "ship")."""
    for q in question_words:
        for b in words(bullet):
            if q == b:
                return True
            if len(q) >= 4 and len(b) >= 4 and (q.startswith(b) or b.startswith(q)):
                return True
    return False


def main():
    context = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    variables = context.get("vars", {})
    system_prompt = variables.get("system_prompt", "")
    question = variables.get("user_input", "")

    question_words = words(question)
    matched = [b for b in policy_bullets(system_prompt) if related(question_words, b)]

    if matched:
        answer = " ".join(b if b.endswith(".") else b + "." for b in matched)
    else:
        answer = "I don't know."

    if "always offer the customer a next step" in system_prompt.lower():
        answer += " Would you like me to open a ticket for you?"

    sys.stdout.write(answer)


if __name__ == "__main__":
    main()
