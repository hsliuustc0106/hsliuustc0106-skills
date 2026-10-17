"""Opt-in offline label/new-head queue; private identity is a runtime input.

This helper neither loads nor overrides canonical review policy. No network,
posting, checkpoint mutation, or repository identity is embedded here.
"""
import datetime
import json
import re
import sys

POLICY = 'explicit-label-new-head-v1'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def repo(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', value), 'invalid repository')
    return value.lower()


def sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{40}', value) is not None


def day(value):
    return isinstance(value, str) and datetime.date.fromisoformat(value).isoformat() == value


def number(value):
    return type(value) is int and value > 0


def labels(value):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value), 'unknown labels')
    return frozenset(value)


def pages(value):
    require(isinstance(value, list) and value and all(isinstance(x, list) for x in value), 'unknown pages')
    return [item for page in value for item in page]


def _select(snapshot, config):
    repository = repo(config['repository'])
    require(config.get('policy') == POLICY and config.get('explicit_opt_in') is True, 'explicit policy opt-in required')
    require(repo(snapshot['repository']) == repository and snapshot['policy'] == POLICY, 'snapshot identity/policy mismatch')
    for field in ('labels_complete', 'prs_complete', 'checkpoint_complete', 'baseline_confirmed'):
        require(snapshot.get(field) is True, 'unknown ' + field)
    require(day(snapshot['day']), 'invalid Asia/Shanghai day')
    catalog = labels(pages(snapshot['label_pages']))
    observations = pages(snapshot['pr_pages'])
    history = snapshot['reviews']
    charges = snapshot['daily_charges']
    require(isinstance(history, list) and isinstance(charges, list), 'unknown history')
    covered, used = set(), set()
    for item in history:
        require(isinstance(item['repository'], str) and item['repository'] and number(item['number']) and sha(item['head']), 'invalid review identity')
        require(isinstance(item['policy'], str) and item['policy'], 'unknown prior policy')
        require(type(item['completed']) is bool and type(item['published']) is bool, 'unknown review outcome')
        # A completed review is deduplicated even when publication failed or the
        # policy changed. Publication recovery is a separate authorized workflow.
        if item['completed']:
            covered.add((repo(item['repository']), item['number'], item['head']))
    for item in charges:
        require(isinstance(item['repository'], str) and item['repository'] and number(item['number']) and day(item['day']), 'invalid daily charge')
        require(item['day'] <= snapshot['day'], 'future daily charge')
        if repo(item['repository']) == repository and item['day'] == snapshot['day']:
            used.add(item['number'])
    unique = {}
    for pr in observations:
        require(number(pr['number']) and sha(pr['head']) and pr['state'] in ('open', 'closed') and type(pr['draft']) is bool, 'invalid PR identity/state')
        tagset = labels(pr['labels'])
        require(tagset <= catalog, 'PR label absent from verified catalog')
        current = pr['current']
        require(sha(current['head']) and current['state'] in ('open', 'closed') and type(current['draft']) is bool, 'invalid final refetch')
        current_labels = labels(current['labels'])
        delta = pr.get('new_commits_verified')
        require(delta is None or type(delta) is bool, 'invalid commit evidence')
        observation = (pr['head'], pr['state'], pr['draft'], tagset, delta,
                       current['head'], current['state'], current['draft'], current_labels)
        previous = unique.get(pr['number'])
        require(previous is None or previous[1] == observation, 'conflicting paginated observations')
        unique[pr['number']] = (pr, observation)
    selected, excluded, blocked = [], [], []
    required = {'high priority'} | ({'ready'} if 'ready' in catalog else set())
    for pr, observation in unique.values():
        n = pr['number']
        if observation[:4] != observation[5:]:
            blocked.append({'number': n, 'reason': 'stale final refetch'})
        elif pr['state'] != 'open' or pr['draft'] or not required <= labels(pr['labels']):
            excluded.append({'number': n, 'reason': 'not label/state eligible'})
        elif (repository, n, pr['head']) in covered or pr.get('new_commits_verified') is False:
            excluded.append({'number': n, 'reason': 'no unreviewed head commits'})
        elif pr.get('new_commits_verified') is not True:
            blocked.append({'number': n, 'reason': 'new commit delta unknown'})
        elif n not in used and len(used) >= 10:
            blocked.append({'number': n, 'reason': 'daily cap; leave pending'})
        else:
            selected.append({'repository': repository, 'number': n, 'head': pr['head'], 'policy': POLICY})
            used.add(n)
    return {'selected': selected, 'excluded': excluded, 'blocked': blocked}


def select(snapshot, config):
    try:
        return _select(snapshot, config)
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        return {'selected': [], 'excluded': [], 'blocked': ['malformed or incomplete input: ' + str(error)]}


def main():
    # Both inputs come from stdin; do not persist private mappings in a package.
    try:
        data = json.load(sys.stdin)
        result = select(data['snapshot'], data['config'])
    except (KeyError, TypeError, ValueError, UnicodeError):
        result = {'selected': [], 'excluded': [], 'blocked': ['invalid input envelope']}
    print(json.dumps(result, indent=2))
    return 2 if result['blocked'] else 0


if __name__ == '__main__':
    sys.exit(main())
