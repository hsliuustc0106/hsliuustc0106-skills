---
name: setup-server-project
description: Set up a workspace in an existing server account with repos, models, llm_wiki, and envs directories, clone requested repositories, and install project dependencies. Use when moving development to a new server or preparing a fresh workspace; excludes account creation and general server administration.
---

# Set Up a Server Project

Prepare a usable project workspace in the requested server account. Scope the
work to project directories, repository checkouts, isolated dependencies, and
focused verification. Do not treat a fresh account as a request to configure the
whole machine.

## Workspace Layout

Use this layout under the user's chosen workspace root unless they specify a
different arrangement:

```text
<workspace>/
├── repos/
│   ├── hsliuustc0106-skills/  # Shared agent skills and project rules
│   ├── vllm-project/
│   │   ├── vllm/
│   │   ├── vllm-omni/
│   │   ├── router/
│   │   └── afd-plugin/
│   └── ThinkFlowLab/         # All repositories accessible in this organization
├── models/      # Model weights and related model assets
├── llm_wiki/    # LLM wiki content and knowledge notes
└── envs/        # Isolated environments, named by project or purpose
```

Create all four directories for a fresh workspace. Creating the layout does not
require repository URLs or model identifiers; ask for those only when cloning
or downloading is requested. Leave unspecified content empty. Do not infer that
`llm_wiki` names a particular remote repository, generate wiki content, or download
models merely because their directories exist.

Group organization repositories under `repos/<org>/<repo-name>`, preserving the
organization's spelling. Keep the skills checkout directly under `repos/`.
Default separately managed Python or Conda environments to `envs/<project-name>`;
include the organization in the environment name when project names collide.
Honor repository tooling
that requires an in-checkout environment and report that exception. Keep model
downloads under `models/` when requested; do not relocate existing caches or
change account-wide cache settings implicitly.

## Include the Skills Repository

For normal workspace setup, clone or reuse
`https://github.com/hsliuustc0106/hsliuustc0106-skills.git` at
`<workspace>/repos/hsliuustc0106-skills`. This is the default repository even
when the user has not supplied additional project URLs. Honor explicit
directory-only, offline, or skip-cloning requests instead.

Apply the existing-checkout checks below before reusing it. Verify its remote
and checked-out revision, and read its README for current usage. Cloning makes
the skill sources available; it does not install them into agent discovery
directories or apply project rules automatically.

When the user requests project-rule installation, use the checkout's documented
`scripts/sync-project.sh` workflow with the selected project, target directory,
and agent tools. Inspect its current supported options first. Preserve existing
instructions, resolve conflicts without implicitly using `--force`, and report
which rules and skill dependencies were installed. Do not copy rules into the
account home or every repository merely because the skills checkout exists.

## Default Organization Repositories

For normal workspace setup, include these groups alongside the skills checkout:

- `vllm-project`: clone `vllm`, `vllm-omni`, `router`, and `afd-plugin` from
  `https://github.com/vllm-project/<repo>.git` into `repos/vllm-project/<repo>`.
  This is a selected list, not a request to clone the entire organization.
- `ThinkFlowLab`: discover and clone all accessible repositories into
  `repos/ThinkFlowLab/<repo>`. Fetch the current list instead of hard-coding the
  six repositories present when this skill was created.

Honor narrower requests: directory-only or offline setup skips network cloning;
a request for one organization or an explicit repository list applies only to
that scope. Cloning alone does not request dependency installation for every
repository.

For organization discovery, prefer existing authenticated GitHub access. With
`gh` available, use the paginated endpoint:

```bash
gh api --paginate 'orgs/ThinkFlowLab/repos?per_page=100&type=all' \
  --jq '.[] | {name, clone_url, default_branch, archived, private}'
```

If `gh` is unavailable, query the GitHub REST API using an available HTTP client
and follow pagination until exhausted. Unauthenticated discovery lists only
public repositories; state that limitation rather than claiming all private
repositories were included. Do not install or configure a CLI just to list
public repositories. Report authentication, rate-limit, or listing failures as
incomplete discovery rather than interpreting them as an empty organization.

For an all-repositories request, include dot-prefixed repositories such as
`.github`, forks, and archived repositories unless excluded by the user. Use the
returned clone URLs and default branches; do not assume every repository uses
`main`. Reuse matching existing checkouts without automatically pulling or
switching branches. Track individual clone failures, continue independent
clones, and report successful and unresolved repositories. Empty repositories
have no HEAD; report them as empty instead of treating that as clone failure.

## Establish the Target

Use context and read-only inspection to determine:

- Whether execution is already on the target server or requires an existing SSH
  connection; identify the target host and account before making changes.
- The workspace root and repository URLs, plus requested branches, tags, or
  commits. Resolve home-relative paths on the target, not on the local machine.
- Any deviations from the workspace layout, including existing checkouts,
  environments, or model storage that should be reused.
- The intended outcome: dependency installation, editable development setup,
  or a specific example or test that should run.

Ask only for missing destination or repository choices that cannot be inferred.
Do not invent a server address, repository URL, or storage path. Reuse existing
authentication; if access fails, report the missing access and ask the user to
establish it without requesting private keys or tokens in chat. Do not disable
SSH host verification to work around a connection failure.

Inspect the target OS, architecture, available disk space, directory ownership,
and installed runtimes or package managers. Check GPU and accelerator details
only when the project needs them. On shared servers, account for allocated
resources and storage constraints before starting builds or downloads.

Briefly state the resolved destination, repositories, and dependency approach.
Proceed with authorized setup without adding a separate approval gate for
ordinary directory creation, cloning, or isolated dependency installation.

## Create or Reuse the Workspace

- Create missing directories under the requested root. Check existing paths and
  symlink targets before writing; do not repurpose a populated directory.
- Clone each requested repository into its intended destination. Honor the
  requested revision; avoid shallow clones when project versioning or the task
  requires history. Initialize submodules or Git LFS assets when needed by the
  documented workflow.
- If a destination already contains a checkout, inspect its remote, revision,
  and worktree status. Reuse a matching checkout; preserve local edits and do
  not reset, clean, switch revisions, or pull over changes merely to normalize it.
  Resolve conflicting destinations or revisions with the user.
- A repeated invocation should reuse completed work. Inspect a partial clone or
  environment after failure instead of deleting it or repeatedly retrying an
  unchanged failing command.

## Install the Project's Dependencies

Read the checkout's `AGENTS.md`, relevant local instructions, README, contributor
setup documentation, manifests, and lockfiles before choosing commands. Apply
matching project skills when available. Treat the repository's supported setup
as authoritative; do not assume every project uses the same Python or Node tool.

- Use the documented runtime version and package manager. Preserve lockfiles
  and dependency constraints; do not upgrade packages or rewrite manifests to
  make installation pass without investigating the cause.
- Prefer an isolated environment under `envs/`, or the repository's documented
  environment location when required. Reuse a compatible existing environment. Avoid global
  package installation, shell startup edits, and global Git configuration unless
  explicitly included in the request.
- If a required runtime or system library is missing, identify it precisely.
  Use a supported user-local installation when it fits the authorized task;
  otherwise report the prerequisite and seek authorization before system-wide
  changes. Do not assume sudo access or install drivers as part of project setup.
- For GPU projects, check the compatibility of the available driver, toolkit,
  framework, and required extensions before installing or compiling. Avoid large
  model downloads or long GPU jobs unless needed for the requested outcome and
  authorized scope.
- Use explicit working directories and environment-specific executables so
  later commands run in the environment actually created. Keep credentials out
  of command output and handoff notes.

## Verify and Hand Off

Verify that the four workspace directories exist and are accessible to the target
account. For layout-only requests, this completes verification. For clone-only
requests, verify each origin, branch, revision when present, and worktree status;
compare the destinations against the selected or discovered repository list.
For dependency setup, also verify the environment interpreter/runtime, then run the
smallest meaningful project check: an import, CLI help command, documented smoke
test, or focused test appropriate to the intended outcome. Dependency resolution
alone does not establish runtime readiness. Avoid launching persistent services
unless requested.

Report:

- Target host/account and absolute paths for the workspace, its four directories,
  and any repository checkouts.
- Checked-out revisions and environment locations.
- Exact commands to enter the project, activate its environment when applicable,
  and run the verified entry point or check.
- Checks that passed, checks not run, and any remaining prerequisites.

If installation is blocked, preserve completed work and distinguish a prepared
directory from a working environment. State the failing step and the concrete
action needed to resume; do not claim setup is complete.
