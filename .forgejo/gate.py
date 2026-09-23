"""The org fork's gate (CircuitBoardGames/ClaudeCode#1264): what the hub vendors from this fork.

Agent and skill frontmatter carries name and description, and no agent RUNS a script through
CLAUDE_PLUGIN_ROOT, which is unset outside a plugin install. Kept out of the workflow YAML because
Forgejo parses a dollar-double-brace in a run block as an expression and rejects the file."""
import glob, re, sys
bad = []
files = sorted(glob.glob("plugin/agents/*.md") + glob.glob("plugin/skills/*/SKILL.md"))
if not files:
    sys.exit("gate: no agent or skill files found -- the check would measure nothing")
for f in files:
    text = open(f, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        bad.append(f"{f}: no frontmatter"); continue
    keys = {l.split(":", 1)[0].strip() for l in m.group(1).splitlines() if ":" in l}
    for k in ("name", "description"):
        if k not in keys:
            bad.append(f"{f}: frontmatter has no {k}")
    # A COMMAND through the plugin root: the path followed by a subcommand in backticks.
    # Naming the path as a fallback is fine; running through it is the defect.
    if f.startswith("plugin/agents/") and re.search(r"`\$\{CLAUDE_PLUGIN_ROOT\}/skills/[^`\s]+/scripts/[^`\s]+ [a-z]", text):
        bad.append(f"{f}: runs a script through ${{CLAUDE_PLUGIN_ROOT}}, unset outside a plugin install (ClaudeCode#1264)")
print(f"gate: checked {len(files)} files")
if bad:
    print("\n".join(bad)); sys.exit(1)
