"""Offline System1 daily-brief selection; never fetches, posts, or writes checkpoints.

Input is an already verified snapshot, not raw GitHub API output. The collector
must supply complete pages, verified commit-delta evidence and a final refetch.
Missing evidence is blocked, never interpreted as an empty catalog.
"""
import json
import sys

REPOSITORY = "ThinkFlowLab/system1-omni"
POLICY = "system1-daily-high-priority-space-v1"
SYSTEM1_POLICY = "system1-nondraft-new-commits-v1"
REPOSITORY_ALIASES = {REPOSITORY, "InferMatrixLab/system1-omni"}


def _repository(value):
    return REPOSITORY if value in REPOSITORY_ALIASES else value


def _select(snapshot):
    blocked = []
    selected = []
    excluded = []
    policy = snapshot.get("policy", POLICY)
    system1 = policy == SYSTEM1_POLICY
    if policy not in (POLICY, SYSTEM1_POLICY):
        return {"selected": [], "blocked": ["unknown policy"], "excluded": []}
    if _repository(snapshot.get("repository")) != REPOSITORY:
        return {"selected": [], "blocked": ["repository identity"], "excluded": []}
    fields = ("prs_complete", "checkpoint_complete")
    if not system1:
        fields += ("labels_complete",)
    for field in fields:
        if snapshot.get(field) is not True:
            blocked.append(field)
    if not isinstance(snapshot.get("day"), str) or not snapshot["day"]:
        blocked.append("Asia/Shanghai day required")
    pages = snapshot.get("label_pages")
    pr_pages = snapshot.get("pr_pages")
    if not system1 and (not isinstance(pages, list) or not all(isinstance(p, list) for p in pages)):
        blocked.append("label pages unavailable")
    if not isinstance(pr_pages, list) or not all(isinstance(p, list) for p in pr_pages):
        blocked.append("PR pages unavailable")
    if system1 and snapshot.get("first_run") is True and snapshot.get("first_run_baseline_verified") is not True:
        blocked.append("first-run baseline unknown")
    if blocked:
        return {"selected": [], "blocked": blocked, "excluded": []}
    labels = set() if system1 else {x for p in pages for x in p}
    if not system1 and "high priority" not in labels:
        return {"selected": [], "blocked": [], "excluded": ["catalog lacks high priority"]}
    required = set() if system1 else {"high priority"} | ({"ready"} if "ready" in labels else set())
    delivered = snapshot["delivered"]
    if not isinstance(delivered, list):
        raise ValueError("delivery history unavailable")
    keys = {(_repository(x["repository"]), x["number"], x["head"], x["policy"]) for x in delivered}
    covered_heads = {(_repository(x["repository"]), x["number"], x["head"]) for x in delivered}
    used = {x["number"] for x in delivered
            if _repository(x["repository"]) == REPOSITORY and x["day"] == snapshot["day"]}
    seen = set()
    for pr in (x for page in pr_pages for x in page):
        number = pr["number"]
        if (type(number) is not int or number <= 0 or
                not isinstance(pr.get("head"), str) or not pr["head"] or
                (not system1 and not isinstance(pr.get("labels"), list))):
            blocked.append({"number": number, "reason": "invalid PR identity/head/labels"})
            continue
        key = (REPOSITORY, number, pr["head"], policy)
        if key in seen:
            continue
        seen.add(key)
        current = pr.get("current")
        refetch_fields = ("head", "state", "draft") if system1 else ("head", "state", "labels")
        if not current or any(current.get(k) != pr.get(k) for k in refetch_fields):
            blocked.append({"number": number, "reason": "stale or missing final refetch"})
            continue
        if system1 and type(pr.get("draft")) is not bool:
            blocked.append({"number": number, "reason": "draft state unknown"})
            continue
        if (pr["state"] != "open" or (system1 and pr["draft"]) or
                (not system1 and not required.issubset(pr["labels"]))):
            excluded.append(number)
            continue
        if key in keys or key[:3] in covered_heads or pr.get("new_commits_verified") is False:
            excluded.append(number)
            continue
        if pr.get("new_commits_verified") is not True:
            blocked.append({"number": number, "reason": "new commit delta unknown"})
            continue
        if system1 and snapshot.get("first_run") is True and pr.get("verified_activity_last24h") is not True:
            blocked.append({"number": number, "reason": "first-run verified push activity unknown"})
            continue
        if number not in used and len(used) >= 10:
            excluded.append({"number": number, "reason": "daily cap; leave pending"})
            continue
        selected.append({"repository": REPOSITORY, "number": number,
                         "head": pr["head"], "policy": policy})
        used.add(number)
    return {"selected": selected, "blocked": blocked, "excluded": excluded}


def select(snapshot):
    try:
        return _select(snapshot)
    except (KeyError, TypeError, ValueError, AttributeError):
        return {"selected": [], "blocked": ["malformed snapshot; evidence unknown"], "excluded": []}


if __name__ == "__main__":
    print(json.dumps(select(json.load(sys.stdin)), indent=2))
