#!/usr/bin/env python3
"""Grade a deslop eval run against the assertions.

Point ITERATION at a run directory containing results.json — a list of
{"id", "name", "rewrite", "summary"} entries, one per eval — and run this
script. It writes grading.json into the run directory and prints a per-eval
and overall pass summary.
"""

import json
import os
import re
from pathlib import Path

# Run directory to grade: point this at a workspace/results-<date>/ directory
# containing results.json (a list of {id, name, rewrite, summary} entries).
ITERATION = Path(__file__).parent / "results-2026-06-04"

# Originals for the pasted evals come from the fenced block in each eval's prompt.
EVALS_JSON = Path(__file__).parent.parent / "skills/docs-deslop/evals/evals.json"

def absent(needles, cs=False):
    needles_n = needles if cs else [n.lower() for n in needles]
    def check(rewrite, summary, original):
        rl = rewrite if cs else rewrite.lower()
        found = [n for n in needles_n if n in rl]
        if found:
            return False, f"Found in rewrite: {found}"
        return True, "Not present in rewrite"
    return check

def present(needles, name="needles", cs=False):
    needles_n = needles if cs else [n.lower() for n in needles]
    def check(rewrite, summary, original):
        rl = rewrite if cs else rewrite.lower()
        found = [n for n in needles_n if n in rl]
        if not found:
            return False, f"None of {name} found"
        return True, f"Found: {found}"
    return check

def all_present(needles, name="all", cs=False):
    needles_n = needles if cs else [n.lower() for n in needles]
    def check(rewrite, summary, original):
        rl = rewrite if cs else rewrite.lower()
        missing = [n for n in needles_n if n not in rl]
        if missing:
            return False, f"Missing: {missing}"
        return True, f"All present: {needles}"
    return check

def shorter_than_original():
    def check(rewrite, summary, original):
        rw = len(rewrite.split())
        ow = len(original.split())
        if rw < ow:
            return True, f"rewrite {rw} words < original {ow} words"
        return False, f"rewrite {rw} words >= original {ow} words"
    return check

def summary_has_counts():
    def check(rewrite, summary, original):
        s = summary
        bullets = [l for l in s.split("\n") if l.strip().startswith(("-", "*"))]
        has_digits = sum(1 for b in bullets if re.search(r"\d", b))
        if len(bullets) >= 3 and has_digits >= 2:
            return True, f"{len(bullets)} bullets, {has_digits} with counts/numbers"
        return False, f"only {len(bullets)} bullets, {has_digits} with numbers"
    return check

def in_summary(needles, name="summary terms"):
    needles_l = [n.lower() for n in needles]
    def check(rewrite, summary, original):
        sl = summary.lower()
        missing = [n for n in needles_l if n not in sl]
        if missing:
            return False, f"Missing from summary ({name}): {missing}"
        return True, f"In summary: {needles}"
    return check

EVALS = {
    "eval-1-file-release-notes": {
        "original_words": 378,
        "assertions": [
            ("Removes marketing intro (absolutely thrilled, significant milestone, most powerful)",
             absent(["absolutely thrilled", "significant milestone", "most powerful"])),
            ("Removes 'In conclusion' / 'quantum leap'",
             absent(["in conclusion", "quantum leap"])),
            ("Removes 'fundamentally transform', 'blazing fast', 'rapidly evolving'",
             absent(["fundamentally transform", "blazing fast", "rapidly evolving"])),
            ("Includes specific perf numbers (12s, 4s, p99)",
             all_present(["12s", "4s", "p99"], "perf specifics")),
            ("Includes issue numbers (#1842, #1856, #1871)",
             all_present(["#1842", "#1856", "#1871"], "issue numbers")),
            ("Names security mechanisms (SAML, OIDC, RBAC)",
             all_present(["saml", "oidc", "rbac"], "security mechanisms")),
            ("Mentions WORM audit logging",
             present(["worm"], "WORM")),
            ("Documents breaking change (--token, --output)",
             all_present(["--token", "--output"], "breaking change details")),
            ("Links to migration guide URL",
             present(["docs.seqera.io/platform-cloud/migrate/24.1"], "migration URL")),
            ("Rewrite is shorter than the original",
             shorter_than_original()),
            ("Change summary has bullets with counts",
             summary_has_counts()),
        ]
    },
    "eval-2-phrases-rule-family": {
        "original_words": 297,
        "assertions": [
            ("Removes throat-clearing and meta openers (here's the thing, it's worth noting, keep in mind, in this section, let's dive, in conclusion)",
             absent(["here's the thing", "it's worth noting", "keep in mind", "in this section", "let's dive", "in conclusion"])),
            ("Removes marketing adjectives and AI vocabulary (powerful, comprehensive, best-in-class, cutting-edge, game-changer, cornerstone, ecosystem, supercharge, delve, tapestry)",
             absent(["powerful", "comprehensive", "best-in-class", "cutting-edge", "game-changer", "cornerstone", "ecosystem", "supercharge", "delve", "tapestry"])),
            ("Removes sales verbs (empower, leverage, democratize, streamline)",
             absent(["empower", "leverage", "democratize", "streamline"])),
            ("Removes padding and nominalizations (in order to, due to the fact that, basically, perform the configuration, and so on)",
             absent(["in order to", "due to the fact that", "basically", "perform the configuration", "and so on"])),
            ("Removes vague attributions and declaratives (experts argue, industry reports suggest, it is widely believed, the implications are significant)",
             absent(["experts argue", "industry reports suggest", "it is widely believed", "the implications are significant"])),
            ("Rewrites product-as-subject phrasing (allows you to, enables you to, gives you the ability)",
             absent(["allows you to", "enables you to", "gives you the ability"])),
            ("Removes non-inclusive terms (sanity check, dummy value, whitelist, master branch)",
             absent(["sanity check", "dummy value", "whitelist", "master branch"])),
            ("Keeps the credential sentences rewritten with inclusive replacements (placeholder, allowlist, main branch)",
             all_present(["placeholder", "allowlist", "main branch"], "inclusive replacements")),
            ("States the two real release changes (cost reporting, bulk relaunch)",
             all_present(["cost reporting", "bulk relaunch"], "release facts")),
            ("Names the execution backends (AWS Batch, Azure Batch, Google Cloud Batch, Kubernetes, HPC)",
             all_present(["aws batch", "azure batch", "google cloud batch", "kubernetes", "hpc"], "backends")),
            ("Replaces 'click here' with descriptive link text",
             absent(["click here"])),
            ("Rewrite is shorter than the original",
             shorter_than_original()),
            ("Change summary has bullets with counts",
             summary_has_counts()),
        ]
    },
    "eval-3-structures-rule-family": {
        "original_words": 253,
        "assertions": [
            ("Removes false drama (binary contrast, negative listing, dramatic fragmentation, self-posed questions)",
             absent(["this isn't a bug", "not slow", "not broken", "that's it.", "the result?", "why does retry behavior matter"])),
            ("Removes anaphora and the tricolon (it retries fast / resilient, reliable, robust)",
             absent(["it retries fast", "resilient, reliable, robust"])),
            ("Removes formulas (despite these challenges, false range, invented concept label, dead metaphor, participle tag)",
             absent(["despite these challenges", "from small scripts", "observability gap", "conductor", "orchestra", "underscoring"])),
            ("Removes historical analogy stacking (AWS/Google/Stripe didn't solve this)",
             absent(["didn't solve this"])),
            ("Removes the fractal summary (in this section we'll cover / as discussed in this section)",
             absent(["in this section", "as discussed"])),
            ("Replaces lazy extremes (every user always, nobody wants)",
             absent(["every user always", "nobody wants"])),
            ("Collapses the one-point dilution (fast/quick/speedy runs)",
             absent(["quick runs save", "speedy runs"])),
            ("States the real retry behavior (3 times, exponential backoff, 30 seconds)",
             all_present(["3 times", "exponential backoff", "30 seconds"], "retry facts")),
            ("States the quota-check behavior (vCPU quota, queues the run)",
             all_present(["vcpu quota", "queue"], "quota behavior")),
            ("Keeps the token expiry and schema-restart facts (1 hour, restart)",
             all_present(["1 hour", "restart"], "token/schema facts")),
            ("Removes the unicode arrow and decorative em-dash aside",
             absent(["→", "— yes, automatically —"])),
            ("Removes the semicolon join",
             absent(["; "])),
            ("Puts the flag in backticks (`--profile`)",
             present(["`--profile`"], "backticked flag")),
            ("Adds the Oxford comma in the settings list",
             present(["work directory, and"], "Oxford comma")),
            ("Removes the terminal period from the heading",
             absent(["token handling."])),
            ("Removes bold-first bullet leads",
             absent(["**performance**", "**reliability**", "**security**"])),
            ("Rewrite is shorter than the original",
             shorter_than_original()),
            ("Change summary has bullets with counts",
             summary_has_counts()),
        ]
    },
    "eval-4-style-terminology-clarity-rule-family": {
        "original_words": 246,
        "assertions": [
            ("Applies the word-choice cheatsheet (utilize, e.g., can not, log in, click all removed)",
             absent(["utilize", "e.g.", "can not", "log in", "click"])),
            ("Uses the preferred terms (sign in, cannot, select)",
             all_present(["sign in", "cannot", "select"], "preferred terms")),
            ("Replaces vague claims with specifics (12s, 4s, Google Cloud Batch)",
             all_present(["12s", "4s", "google cloud batch"], "specifics")),
            ("Converts passive to active voice (is submitted by, will be generated, should be run, is performed)",
             absent(["is submitted", "will be generated", "should be run", "is performed"])),
            ("Removes subject-hiding constructions (there are several, it is recommended)",
             absent(["there are several", "it is recommended"])),
            ("Cuts culture-specific idioms (rocket science, don't sweat it)",
             absent(["rocket science", "don't sweat"])),
            ("Replaces the real-looking token and email with placeholders",
             absent(["sk-1a2b3c", "acme-corp"])),
            ("Uses placeholder values (<your_access_token>, example.com)",
             all_present(["<your_access_token>", "example.com"], "placeholders")),
            ("Fixes the gerund title (Configuring The Compute Environment)",
             absent(["configuring the compute environment"])),
            ("Removes bold from headings and the skipped H4 level",
             absent(["**step", "#### "])),
            ("Bolds the Launch button label",
             present(["**Launch**"], "bold UI label", cs=True)),
            ("Breaks up the noun string (project integration custom settings)",
             absent(["project integration custom settings"])),
            ("Uses long forms over contractions in the Notes",
             absent(["don't", "it's"])),
            ("Replaces 'Tower' with Seqera Platform",
             absent(["Tower"], cs=True)),
            ("Uses the product name Seqera Platform",
             present(["seqera platform"], "product name")),
            ("Corrects product casing (NextFlow -> Nextflow, multiQC -> MultiQC)",
             absent(["NextFlow", "multiQC"], cs=True)),
            ("Uses the correct product names (Nextflow, MultiQC)",
             all_present(["Nextflow", "MultiQC"], "product names", cs=True)),
            ("Lowercases the feature nouns (Credentials, Compute Environments, Workspace)",
             absent(["your Credentials", "Compute Environments", "per Workspace"], cs=True)),
            ("Spells out abbreviations on first use (HPC, GCP)",
             all_present(["high-performance computing (hpc)", "google cloud platform (gcp)"], "spelled-out abbreviations")),
            ("Puts the environment variable in backticks",
             present(["`tower_access_token`"], "backticked env var")),
            ("Defines 'executor' on first use with examples (AWS Batch, Kubernetes)",
             all_present(["executor", "aws batch", "kubernetes"], "executor definition")),
            ("Fixes pipeline vs workflow (the pipeline failed/fails to launch)",
             present(["pipeline failed to launch", "pipeline fails to launch"], "pipeline term")),
            ("Removes the mistyped workflow/executions/job terms",
             absent(["workflow failed", "executions", "each job"])),
            ("Corrects and bolds the UI names (Launchpad, Data Explorer, Runs)",
             all_present(["**Launchpad**", "**Data Explorer**", "**Runs**"], "bold UI names", cs=True)),
            ("Removes the wrong UI names (Launch Pad, data explorer)",
             absent(["Launch Pad", "data explorer"], cs=True)),
            ("Puts code identifiers in backticks (--profile, nextflow.config)",
             all_present(["`--profile`", "`nextflow.config`"], "backticked identifiers")),
            ("Summary names the terminology fixes",
             in_summary(["terminolog"], "terminology")),
            ("Change summary has bullets with counts",
             summary_has_counts()),
        ]
    },
    "eval-5-topic-types-rule-family": {
        "original_words": 169,
        "assertions": [
            ("Retitles the Concept with a noun title (Workspaces, not Overview)",
             present(["# Workspaces"], "Concept noun title", cs=True)),
            ("Removes the Overview framing and the Summary section",
             absent(["this overview", "that's how workspaces work", "## summary"])),
            ("Splits out a Task (Create a workspace) with a prerequisites list",
             all_present(["create a workspace", "prerequisite"], "Task + prerequisites")),
            ("Uses imperative numbered steps (not 'you should click')",
             present(["1. "], "numbered steps")),
            ("Removes the hedged step phrasing (you should click, you navigate, you can enter)",
             absent(["you should click", "you navigate", "you can enter"])),
            ("Replaces 'click' with 'select' and bolds the UI labels",
             absent(["click"])),
            ("Bolds the New and Add buttons",
             all_present(["**New**", "**Add**"], "bold buttons", cs=True)),
            ("Converts the settings into a table with the 256 default",
             all_present(["|", "256"], "settings table")),
            ("Removes the prose narrative between settings rows",
             absent(["really important", "as mentioned"])),
            ("Moves the error into the troubleshooting title with an Error: prefix",
             all_present(["error:", "accessdenied"], "Error title")),
            ("Names the single cause and drops the hedging and chat",
             absent(["don't worry", "a variety of factors", "sometimes things go wrong"])),
            ("Gives a numbered resolution with the s3:PutObject fix",
             all_present(["s3:putobject", "resolv"], "resolution")),
            ("Uses the Tutorial: title prefix",
             present(["tutorial:"], "Tutorial: prefix")),
            ("Removes the inflated tutorial title and journey framing",
             absent(["complete and exhaustive", "in today's", "embark", "exciting"])),
            ("Includes a Before you begin section",
             present(["before you begin"], "Before you begin")),
            ("Uses active-verb tutorial section headings",
             all_present(["set up the compute environment", "review the"], "tutorial headings")),
            ("Uses an active-verb launch heading",
             present(["launch the pipeline", "launch nf-core/rnaseq"], "launch heading")),
            ("Folds in or relinks the More info stub",
             absent(["see the other page", "## more info"])),
            ("Summary names all five topic types",
             in_summary(["concept", "task", "reference", "troubleshooting", "tutorial"], "all five types")),
            ("Change summary has bullets with counts",
             summary_has_counts()),
        ]
    }
}

# File-based evals read their original from the test-input file; pasted evals
# fall back to the fenced block extracted from their prompt in evals.json.
INPUT_FILES = {
    "eval-1-file-release-notes": str(Path(__file__).parent.parent / "skills/docs-deslop/evals/test-inputs/release-notes.md"),
}

def read(p):
    try:
        return Path(p).read_text()
    except FileNotFoundError:
        return ""

def load_originals():
    """Extract each pasted eval's original text (the first fenced block in its prompt)."""
    originals = {}
    try:
        data = json.loads(EVALS_JSON.read_text())
    except FileNotFoundError:
        return originals
    for e in data["evals"]:
        m = re.search(r"```\n(.*?)\n```", e["prompt"], re.DOTALL)
        if m:
            originals[f"eval-{e['id']}-{e['name']}"] = m.group(1)
    return originals

def grade_run(rewrite, summary, original, conf):
    """Grade one (rewrite, summary) pair against an eval's assertions. Returns the grading dict."""
    expectations = []
    passed_count = 0
    for assertion_text, checker in conf["assertions"]:
        passed, evidence = checker(rewrite, summary, original)
        if passed:
            passed_count += 1
        expectations.append({"text": assertion_text, "passed": passed, "evidence": evidence})
    total = len(expectations)
    return {
        "summary": {
            "pass_rate": passed_count / total if total else 0.0,
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
        },
        "expectations": expectations,
    }

def main():
    results_file = ITERATION / "results.json"
    if not results_file.exists():
        raise SystemExit(f"No results.json in {ITERATION} — point ITERATION at a run directory.")
    results = json.loads(results_file.read_text())
    originals = load_originals()

    gradings = {}
    total_passed = total = 0
    for entry in results:
        key = f"eval-{entry['id']}-{entry['name']}"
        conf = EVALS.get(key)
        if conf is None:
            print(f"{key}: no assertion set — skipped")
            continue

        original = read(INPUT_FILES[key]) if key in INPUT_FILES else originals.get(key, "")
        if not original:
            original = "x " * conf["original_words"]

        grading = grade_run(entry.get("rewrite", ""), entry.get("summary", ""), original, conf)
        gradings[key] = grading
        s = grading["summary"]
        total_passed += s["passed"]
        total += s["total"]
        print(f"{key}: {s['passed']}/{s['total']}")
        for e in grading["expectations"]:
            if not e["passed"]:
                print(f"  FAIL: {e['text']}  ->  {e['evidence']}")

    (ITERATION / "grading.json").write_text(json.dumps(gradings, indent=2))
    print(f"\nTotal: {total_passed}/{total} assertions pass "
          f"({total_passed / total:.0%})" if total else "\nNo evals graded.")
    print(f"Wrote {ITERATION / 'grading.json'}")

if __name__ == "__main__":
    main()
