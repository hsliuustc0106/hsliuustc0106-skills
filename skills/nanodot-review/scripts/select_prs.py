#!/usr/bin/env python3
"""Read-only, fail-closed selection for ThinkFlowLab/nanodot (Python 3.8+).

select_prs(label_pages, pull_pages, ledger, day, policy_version) is network-free.
Each page is {"items": [...], "next_page": 2} (null on the final page).
Pages must form a complete consecutive chain starting at 1. Unknown/error pages
are errors, never empty results. REST label objects use {"name": "ready"}; PRs
use number, state, labels and head.sha. Whole label names are case-insensitive;
whitespace and substrings are NOT aliases. "ready" in the complete repository
catalog requires both "high priority" and "ready" on each open PR. Its confirmed
absence requires only "high priority". There is no creation-date restriction.

The ledger is a JSON array of CONFIRMED completed reviews, each containing repo,
number, head_sha, policy_version and timezone-aware reviewed_at. Initialize []
explicitly on first use; a missing/corrupt ledger is an error. Any reviewed head
is excluded across all policy versions. Duplicate repo/PR/head/policy jobs count
once per day, across policies, toward the limit of 10 completed review jobs.
Days use Asia/Shanghai (UTC+08:00 for contemporary review dates).

CLI: select_prs.py --ledger ledger.json [--day YYYY-MM-DD] [--input fixture.json]
Fixtures contain repo, label_pages and pull_pages using the page schema above.
Live mode calls only `gh api` GETs and follows every Link rel=next page. Output
is a JSON object with capacity, label policy and candidates; errors exit 1 with
no candidates on stdout. No selection writes/reserves/marks a review completed.
Serialize review sessions, refresh the ledger/cap before posting, revalidate the
head immediately before posting, and append to the ledger only after confirmed
completion. This read-only helper cannot make posting or concurrency atomic.

Stale-head guard: --revalidate NUMBER HEAD [--input fixture.json], where an
offline fixture supplies repo and current_pr (a fresh REST PR object). A changed
head, closed PR or unknown response fails. This checks identity/head, not a new
label/ledger snapshot; callers must also rerun eligibility before posting.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

REPO = "ThinkFlowLab/nanodot"
POLICY_VERSION = "nanodot-review-v1"
DAILY_LIMIT = 10
REVIEW_TZ = timezone(timedelta(hours=8), "Asia/Shanghai")


class SelectionError(ValueError):
    """Required evidence is unknown, inconsistent or stale; do not proceed."""


def nonempty_string(value, field):
    if not isinstance(value, str) or not value.strip():
        raise SelectionError("Missing/invalid " + field)
    return value


def pr_number(value):
    if type(value) is not int or value < 1:
        raise SelectionError("Missing/invalid PR number")
    return value


def complete_records(pages, resource):
    """Flatten explicitly terminated pages, preserving no partial success."""
    if not isinstance(pages, list) or not pages:
        raise SelectionError(resource + ": complete page sequence required")
    records = []
    for number, page in enumerate(pages, 1):
        if not isinstance(page, dict) or "error" in page:
            raise SelectionError(resource + ": unknown/error page")
        if page.get("status", 200) != 200:
            raise SelectionError(resource + ": unsuccessful page")
        if not isinstance(page.get("items"), list) or "next_page" not in page:
            raise SelectionError(resource + ": malformed/incomplete page")
        following = page["next_page"]
        if number == len(pages):
            if following is not None:
                raise SelectionError(resource + ": incomplete pagination")
        elif type(following) is not int or following != number + 1:
            raise SelectionError(resource + ": broken pagination chain")
        records.extend(page["items"])
    return records


def label_names(labels):
    if not isinstance(labels, list):
        raise SelectionError("Missing/invalid label list")
    names = set()
    for label in labels:
        if not isinstance(label, dict):
            raise SelectionError("Missing/invalid label object")
        names.add(nonempty_string(label.get("name"), "label name").casefold())
    return names


def read_pr(pr):
    if not isinstance(pr, dict):
        raise SelectionError("Missing/invalid PR object")
    number = pr_number(pr.get("number"))
    if pr.get("state") not in ("open", "closed"):
        raise SelectionError("Missing/invalid PR state")
    head = pr.get("head")
    if not isinstance(head, dict):
        raise SelectionError("Missing/invalid PR head")
    sha = nonempty_string(head.get("sha"), "PR head SHA")
    names = label_names(pr.get("labels"))
    return number, sha, names


def review_day(value=None):
    if value is None:
        return datetime.now(REVIEW_TZ).date()
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise SelectionError("Day must be YYYY-MM-DD in Asia/Shanghai")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise SelectionError("Invalid review day") from error


def ledger_state(ledger, day):
    if not isinstance(ledger, list):
        raise SelectionError("Ledger must be an array of confirmed reviews")
    reviewed_heads, jobs_today = set(), set()
    for entry in ledger:
        if not isinstance(entry, dict):
            raise SelectionError("Malformed ledger entry")
        repo = nonempty_string(entry.get("repo"), "ledger repo").casefold()
        number = pr_number(entry.get("number"))
        sha = nonempty_string(entry.get("head_sha"), "ledger head_sha")
        policy = nonempty_string(entry.get("policy_version"), "ledger policy_version")
        timestamp = nonempty_string(entry.get("reviewed_at"), "ledger reviewed_at")
        try:
            reviewed_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as error:
            raise SelectionError("Invalid ledger reviewed_at") from error
        if reviewed_at.tzinfo is None or reviewed_at.utcoffset() is None:
            raise SelectionError("Ledger reviewed_at requires a timezone")
        if repo != REPO.casefold():
            continue
        reviewed_heads.add((number, sha))
        if reviewed_at.astimezone(REVIEW_TZ).date() == day:
            jobs_today.add((repo, number, sha, policy))
    return reviewed_heads, len(jobs_today)


def select_prs(label_pages, pull_pages, ledger, day=None, policy_version=POLICY_VERSION):
    """Return eligible candidates and budget without mutating any input/state."""
    policy_version = nonempty_string(policy_version, "policy version")
    day = review_day(day)
    catalog = label_names(complete_records(label_pages, "label catalog"))
    ready_exists = "ready" in catalog
    required = {"high priority", "ready"} if ready_exists else {"high priority"}
    reviewed, reviewed_today = ledger_state(ledger, day)
    capacity = max(0, DAILY_LIMIT - reviewed_today)
    prs = {}
    for pr in complete_records(pull_pages, "open PRs"):
        number, sha, names = read_pr(pr)
        fingerprint = (sha, pr["state"], names)
        if number in prs and prs[number][0] != fingerprint:
            raise SelectionError("Conflicting duplicate PR {}; refresh snapshot".format(number))
        prs[number] = (fingerprint, pr)
    candidates = []
    for number in sorted(prs):
        (sha, state, names), pr = prs[number]
        if state != "open" or not required.issubset(names) or (number, sha) in reviewed:
            continue
        candidates.append({
            "repo": REPO,
            "number": number,
            "head_sha": sha,
            "policy_version": policy_version,
            "dedupe_key": [REPO, number, sha, policy_version],
            "title": pr.get("title", ""),
            "url": "https://github.com/{}/pull/{}".format(REPO, number),
        })
    return {
        "repo": REPO,
        "day": day.isoformat(),
        "timezone": "Asia/Shanghai",
        "policy_version": policy_version,
        "ready_label_exists": ready_exists,
        "required_labels": sorted(required),
        "reviews_today": reviewed_today,
        "remaining_capacity": capacity,
        "candidates": candidates[:capacity],
    }


def revalidate_head(current_pr, number, expected_head):
    """Reject a stale/closed/unknown PR immediately before a separate posting step."""
    number = pr_number(number)
    expected_head = nonempty_string(expected_head, "expected head SHA")
    actual_number, actual_head, _ = read_pr(current_pr)
    if actual_number != number or current_pr["state"] != "open":
        raise SelectionError("PR identity/state changed; do not post")
    if actual_head != expected_head:
        raise SelectionError("PR head changed; discard stale review and reselect")
    return {"repo": REPO, "number": number, "head_sha": actual_head, "current": True}


def gh_response(endpoint):
    """Read one successful REST response, retaining pagination evidence."""
    try:
        result = subprocess.run(
            ["gh", "api", "--hostname", "github.com", "--method", "GET", "--include", endpoint],
            capture_output=True, text=True, check=False, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise SelectionError("Cannot run gh: " + str(error)) from error
    if result.returncode:
        raise SelectionError("GitHub API failed: " + result.stderr.strip())
    response = result.stdout.replace("\r\n", "\n")
    headers, separator, body = response.partition("\n\n")
    lines = headers.splitlines()
    if not separator or not lines or not re.match(r"^HTTP/\S+ 200(?:\s|$)", lines[0]):
        raise SelectionError("Unknown GitHub HTTP response; cannot prove success")
    parsed_headers = {}
    for line in lines[1:]:
        key, colon, value = line.partition(":")
        if not colon:
            raise SelectionError("Malformed GitHub HTTP headers")
        key = key.lower().strip()
        if key in parsed_headers:
            raise SelectionError("Duplicate GitHub HTTP header: " + key)
        parsed_headers[key] = value.strip()
    try:
        return json.loads(body), parsed_headers
    except ValueError as error:
        raise SelectionError("Invalid GitHub JSON response") from error


def next_page(headers, resource, current_page):
    link = headers.get("link")
    if link is None:
        return None
    relations = {}
    for part in link.split(","):
        match = re.fullmatch(r'\s*<([^>]+)>;\s*rel="([a-z]+)"\s*', part)
        if not match:
            raise SelectionError("Malformed pagination Link header")
        url, relation = match.groups()
        if relation not in ("first", "prev", "next", "last") or relation in relations:
            raise SelectionError("Unknown/duplicate pagination relation")
        parsed = urlsplit(url)
        query = parse_qs(parsed.query)
        expected_path = "/repos/{}/{}".format(REPO, resource)
        # GitHub may canonicalize Link paths to /repositories/<numeric-id>/...
        # Only the page number is reused; every request remains pinned to REPO.
        valid_path = (parsed.path.casefold() == expected_path.casefold()
                      or re.fullmatch(r"/repositories/[1-9][0-9]*/" + resource, parsed.path))
        if (parsed.scheme != "https" or parsed.netloc != "api.github.com"
                or not valid_path or query.get("per_page") != ["100"]):
            raise SelectionError("Unexpected pagination target")
        page = query.get("page", [])
        if len(page) != 1 or not page[0].isdigit() or int(page[0]) < 1:
            raise SelectionError("Malformed pagination page number")
        relations[relation] = int(page[0])
    following = relations.get("next")
    if following is not None and following != current_page + 1:
        raise SelectionError("Incomplete/cyclic pagination")
    if (relations.get("first", 1) != 1
            or relations.get("prev", current_page - 1) >= current_page
            or relations.get("last", current_page) < current_page):
        raise SelectionError("Inconsistent pagination relations")
    if following is None and relations.get("last", current_page) > current_page:
        raise SelectionError("Missing next link before last page")
    if following is not None and relations.get("last", following) < following:
        raise SelectionError("Next link beyond last page")
    return following


def fetch_pages(resource):
    pages, number = [], 1
    while True:
        query = "per_page=100&page={}".format(number)
        if resource == "pulls":
            query += "&state=open"
        body, headers = gh_response("repos/{}/{}?{}".format(REPO, resource, query))
        if not isinstance(body, list):
            raise SelectionError(resource + ": expected a page array")
        following = next_page(headers, resource, number)
        pages.append({"items": body, "next_page": following})
        if following is None:
            return pages
        number = following


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SelectionError("Cannot read JSON {}: {}".format(path, error)) from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", help="User-supplied confirmed-review JSON ledger (read-only)")
    parser.add_argument("--day", help="Asia/Shanghai calendar day, YYYY-MM-DD")
    parser.add_argument("--policy-version", default=POLICY_VERSION)
    parser.add_argument("--input", help="Offline complete-page JSON fixture; never calls gh")
    parser.add_argument("--revalidate", nargs=2, metavar=("NUMBER", "HEAD"))
    args = parser.parse_args(argv)
    if not args.revalidate and not args.ledger:
        parser.error("--ledger is required for selection")
    try:
        fixture = read_json(args.input) if args.input else None
        if args.input and (not isinstance(fixture, dict) or fixture.get("repo") != REPO):
            raise SelectionError("Fixture must identify repo " + REPO)
        if args.revalidate:
            try:
                number = int(args.revalidate[0])
            except ValueError as error:
                raise SelectionError("Invalid PR number") from error
            current = fixture.get("current_pr") if fixture is not None else gh_response(
                "repos/{}/pulls/{}".format(REPO, pr_number(number))
            )[0]
            result = revalidate_head(current, number, args.revalidate[1])
        else:
            ledger = read_json(args.ledger)
            labels = fixture.get("label_pages") if fixture is not None else fetch_pages("labels")
            pulls = fixture.get("pull_pages") if fixture is not None else fetch_pages("pulls")
            result = select_prs(labels, pulls, ledger, args.day, args.policy_version)
        print(json.dumps(result, indent=2))
        return 0
    except SelectionError as error:
        print("Selection blocked: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
