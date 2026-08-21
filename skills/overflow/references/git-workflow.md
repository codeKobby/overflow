# Git Exercise Workflow

Use this contract during `/setup-learning`, `/exercise`, `/assess`, `/progress`, and `/help git`. Git isolation is optional. Never create, switch, stage, commit, push, merge, delete, or open a pull request without the learner’s explicit confirmation for that action.

## Setup choice

During setup, ask one selectable question:

> How should Overflow isolate coding exercises?
>
> **A. Local exercise branch (recommended)** — create `overflow/exercise/<slug>` from the current clean branch.
>
> **B. Separate Git worktree** — create a linked directory and branch for parallel or protected main work.
>
> **C. Use the current branch** — do not create a branch; keep exercise work here.
>
> **D. Decide later** — store no Git preference and ask when the first code exercise starts.

The default recommendation is a local branch when the worktree is clean. Recommend a worktree when the learner wants to keep the main checkout untouched or work in parallel. Do not assume a branch is appropriate for chat-only proof questions.

## Inspect before changing Git state

Run the read-only inspection first:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . --mode inspect --output json
```

Inspect the Git root, current branch, default branch when discoverable, HEAD, status, untracked and staged paths, remotes, existing branches, and worktrees. Show dirty paths before offering a branch. If uncommitted changes exist, offer:

- continue without branching;
- commit the existing changes, with a proposed message and confirmation;
- stash them with a named entry and confirmation;
- cancel and let the learner resolve them.

Never silently stash, reset, clean, amend, rebase, or discard changes. A clean working state is the safe starting point for branch creation.

## Plan before applying

Create a proposal without changing the repository:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . --mode plan --slug day-01-q03 --output json
```

Show the target branch, base branch and commit, worktree path if applicable, collision status, exact command, and warnings. Use sanitized names such as:

```text
overflow/exercise/day-01-q03
overflow/exercise/parser-basics
overflow/lesson/auth-flow
```

Do not include secrets, tokens, private data, or long natural-language prompts in branch names. Check for existing branch and worktree collisions. Ask before applying the proposal.

## Apply branch or worktree creation

Only after confirmation, run the helper with `--apply`:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . \
  --mode branch \
  --slug day-01-q03 \
  --apply
```

For a linked worktree:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . \
  --mode worktree \
  --slug parser-basics \
  --worktree ../project-overflow-parser-basics \
  --apply
```

The helper refuses to apply when the tree is dirty, the branch already exists, or the current HEAD is detached. It writes `.learning/git-workflow.json` only after successful creation.

## Durable Git state

Store branch metadata in `.learning/git-workflow.json` and link it from exercise manifests, attempts, assessments, and progress:

```json
{
  "version": 1,
  "mode": "branch",
  "base_branch": "main",
  "base_commit": "<sha>",
  "exercise_branch": "overflow/exercise/day-01-q03",
  "worktree_path": null,
  "created_at": "<timestamp>",
  "commit_status": "not-requested",
  "push_status": "not-requested",
  "pull_request_status": "not-requested"
}
```

Record current branch, base branch, base commit, worktree path, changed paths, commit SHAs, remote, push status, and optional pull-request URL. Preserve the original branch and base commit so `/assess` can compare the learner’s diff without guessing.

## Commit, push, and review permissions

These are separate learner choices:

1. **Stage** only declared exercise or assessment files after showing the path list.
2. **Commit** with a descriptive message such as `learn: attempt day-01 q03` or `learn: revise parser exercise q03`.
3. **Push** only after confirming the remote, branch name, and that the learner has permission.
4. **Open a draft pull request** only after confirming base branch, head branch, title, body, and reviewers. Use a draft when the learner wants feedback before completion.
5. **Merge, delete, or switch back** only after separate confirmation.

Do not claim a commit, push, or pull request exists until the command output or GitHub response confirms it. Never force-push, delete a branch, or rewrite history as part of ordinary learning setup.

## Assessment integration

When a branch or worktree is active, `/assess` may use the base commit and branch diff as evidence. It still asks permission before running checks. A branch does not replace proof questions: after implementation and verification, ask due native or inferred `Prove it` questions and Finish line gates. Commit and push status are Git evidence, not learning mastery.

## Cleanup

Do not remove a worktree or branch merely because an exercise is assessed. Offer cleanup only after showing its path, branch, unpushed commits, and linked learning artifacts. Use `git worktree remove <path>` for a linked worktree and ordinary branch deletion only after the learner confirms that no unpushed work or future review depends on it.
