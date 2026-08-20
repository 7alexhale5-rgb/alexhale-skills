# Privacy

Regression Test has no server, account, analytics, or telemetry. It does not send
data to Alex Hale.

The skill reads and writes Promptfoo files inside your project. These include
test prompts, golden cases, and result files under `.promptfoo/`.

Promptfoo may send prompts and test inputs to the model provider you choose.
That provider handles the data under its own terms. The included worked example
uses a local stand-in. It needs no API key and sends no model data over the web.

Do not put passwords, API keys, or private customer data in golden cases. Review
result files before you commit or share them.

For a privacy problem, open a GitHub issue without private data. Use a private
security report if the report contains sensitive details.
