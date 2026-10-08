"""Select the explicitly configured personal daily queue from verified evidence.

Network-free: no GitHub calls, source execution, posting, or ledger writes.
The collector owns complete pagination, commit-delta proof, and final refetches.
"""
import datetime
import json
import sys

REPOSITORY = "ThinkFlowLab/nanodot"
POLICY = "nanodot-daily-high-priority-v1"


def _sha(value):
    return (isinstance(value, str) and len(value) == 40
            and all(c in "0123456789abcdef" for c in value))


def _day(value):
    return (isinstance(value, str)
            and datetime.date.fromisoformat(value).isoformat() == value)


def _number(value):
    return type(value) is int and value > 0


def _labels(value):
    if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
        raise ValueError("unknown labels")
    return set(value)


def _pages(value):
    if not isinstance(value, list) or not value or not all(isinstance(x, list) for x in value):
        raise ValueError("unknown pages")
    return [item for page in value for item in page]


def _select(snapshot):
    if snapshot["repository"] != REPOSITORY:
        raise ValueError("wrong repository")
    for field in ("labels_complete", "prs_complete", "checkpoint_complete", "baseline_confirmed"):
        if snapshot.get(field) is not True:
            raise ValueError("unknown " + field)
    if not _day(snapshot["day"]):
        raise ValueError("invalid Asia/Shanghai day")
    catalog = _labels(_pages(snapshot["label_pages"]))
    prs = _pages(snapshot["pr_pages"])
    history = snapshot["delivered"]
    if not isinstance(history, list):
        raise ValueError("unknown delivery history")
    covered, keys, used = set(), set(), set()
    for item in history:
        if (not isinstance(item["repository"], str) or not item["repository"]
                or not _number(item["number"]) or not _sha(item["head"])
                or not isinstance(item["policy"], str) or not item["policy"]
                or not _day(item["day"])):
            raise ValueError("invalid delivery history")
        key = (item["repository"], item["number"], item["head"], item["policy"])
        keys.add(key)
        covered.add(key[:3])
        if item["repository"] == REPOSITORY and item["day"] == snapshot["day"]:
            used.add(item["number"])

    # Validate the entire collection before yielding any candidate. Conflicting
    # duplicate pages cannot let an earlier, now-stale observation win.
    unique = {}
    for pr in prs:
        if not _number(pr["number"]) or not _sha(pr["head"]) or pr["state"] not in ("open", "closed"):
            raise ValueError("invalid PR identity/head/state")
        labels = _labels(pr["labels"])
        if not labels.issubset(catalog):
            raise ValueError("PR label absent from verified catalog")
        current = pr["current"]
        current_labels = _labels(current["labels"])
        delta = pr.get("new_commits_verified")
        if delta is not None and type(delta) is not bool:
            raise ValueError("invalid new commit evidence")
        observation = (pr["head"], pr["state"], labels,
                       delta, current["head"],
                       current["state"], current_labels)
        previous = unique.get(pr["number"])
        if previous is not None and previous[1] != observation:
            raise ValueError("conflicting paginated PR observations")
        unique[pr["number"]] = (pr, observation)

    required = {"high priority"} | ({"ready"} if "ready" in catalog else set())
    selected, excluded, blocked = [], [], []
    for pr, _ in unique.values():
        number = pr["number"]
        current = pr["current"]
        if (current["head"] != pr["head"] or current["state"] != pr["state"]
                or _labels(current["labels"]) != _labels(pr["labels"])):
            blocked.append({"number": number, "reason": "stale final refetch"})
            continue
        key = (REPOSITORY, number, pr["head"], POLICY)
        if pr["state"] != "open" or not required.issubset(pr["labels"]):
            excluded.append({"number": number, "reason": "not label/state eligible"})
        elif key in keys or key[:3] in covered or pr.get("new_commits_verified") is False:
            excluded.append({"number": number, "reason": "no unreviewed head commits"})
        elif pr.get("new_commits_verified") is not True:
            blocked.append({"number": number, "reason": "new commit delta unknown"})
        elif number not in used and len(used) >= 10:
            excluded.append({"number": number, "reason": "daily cap; leave pending"})
        else:
            selected.append({"repository": REPOSITORY, "number": number,
                             "head": pr["head"], "policy": POLICY})
            used.add(number)
    return {"selected": selected, "excluded": excluded, "blocked": blocked}


def select(snapshot):
    try:
        return _select(snapshot)
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        return {"selected": [], "excluded": [],
                "blocked": ["malformed or incomplete snapshot: " + str(error)]}


if __name__ == "__main__":
    try:
        result = select(json.load(sys.stdin))
    except (ValueError, UnicodeError):
        result = {"selected": [], "excluded": [], "blocked": ["invalid JSON snapshot"]}
    print(json.dumps(result, indent=2))
    raise SystemExit(2 if result["blocked"] else 0)
