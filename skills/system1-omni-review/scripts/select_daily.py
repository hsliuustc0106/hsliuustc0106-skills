"""Offline System1 daily-brief selection; never fetches, posts, or writes checkpoints.

Input is an already verified snapshot, not raw GitHub API output. The collector
must supply complete pages, verified commit-delta evidence and a final refetch.
Missing evidence is blocked, never interpreted as an empty catalog.
"""
import json
import sys

REPOSITORY = "ThinkFlowLab/system1-omni"
POLICY = "system1-daily-high-priority-space-v1"


def _select(snapshot):
    blocked = []
    selected = []
    excluded = []
    if snapshot.get("repository") != REPOSITORY:
        return {"selected": [], "blocked": ["repository identity"], "excluded": []}
    for field in ("labels_complete", "prs_complete", "checkpoint_complete"):
        if snapshot.get(field) is not True:
            blocked.append(field)
    if not isinstance(snapshot.get("day"), str) or not snapshot["day"]:
        blocked.append("Asia/Shanghai day required")
    pages = snapshot.get("label_pages")
    pr_pages = snapshot.get("pr_pages")
    if not isinstance(pages, list) or not all(isinstance(p, list) for p in pages):
        blocked.append("label pages unavailable")
    if not isinstance(pr_pages, list) or not all(isinstance(p, list) for p in pr_pages):
        blocked.append("PR pages unavailable")
    if blocked:
        return {"selected": [], "blocked": blocked, "excluded": []}
    labels = {x for p in pages for x in p}
    if "high priority" not in labels:
        return {"selected": [], "blocked": [], "excluded": ["catalog lacks high priority"]}
    required = {"high priority"} | ({"ready"} if "ready" in labels else set())
    delivered = snapshot["delivered"]
    if not isinstance(delivered, list):
        raise ValueError("delivery history unavailable")
    keys = {(x["repository"], x["number"], x["head"], x["policy"]) for x in delivered}
    covered_heads = {(x["repository"], x["number"], x["head"]) for x in delivered}
    used = {x["number"] for x in delivered
            if x["repository"] == REPOSITORY and x["day"] == snapshot["day"]}
    seen = set()
    for pr in (x for page in pr_pages for x in page):
        number = pr["number"]
        if (type(number) is not int or number <= 0 or
                not isinstance(pr.get("head"), str) or not pr["head"] or
                not isinstance(pr.get("labels"), list)):
            blocked.append({"number": number, "reason": "invalid PR identity/head/labels"})
            continue
        key = (REPOSITORY, number, pr["head"], POLICY)
        if key in seen:
            continue
        seen.add(key)
        current = pr.get("current")
        if not current or any(current.get(k) != pr.get(k) for k in ("head", "state", "labels")):
            blocked.append({"number": number, "reason": "stale or missing final refetch"})
            continue
        if pr["state"] != "open" or not required.issubset(pr["labels"]):
            excluded.append(number)
            continue
        if key in keys or key[:3] in covered_heads or pr.get("new_commits_verified") is False:
            excluded.append(number)
            continue
        if pr.get("new_commits_verified") is not True:
            blocked.append({"number": number, "reason": "new commit delta unknown"})
            continue
        if number not in used and len(used) >= 10:
            excluded.append({"number": number, "reason": "daily cap; leave pending"})
            continue
        selected.append({"repository": REPOSITORY, "number": number,
                         "head": pr["head"], "policy": POLICY})
        used.add(number)
    return {"selected": selected, "blocked": blocked, "excluded": excluded}


def select(snapshot):
    try:
        return _select(snapshot)
    except (KeyError, TypeError, ValueError, AttributeError):
        return {"selected": [], "blocked": ["malformed snapshot; evidence unknown"], "excluded": []}


if __name__ == "__main__":
    print(json.dumps(select(json.load(sys.stdin)), indent=2))
