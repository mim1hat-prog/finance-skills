# Security and data boundaries

This public repository contains generic instructions, local tools, public benchmark observations with recorded terms and independently invented fixtures. It is not a storage location for company data or credentials.

## Report a concern

For a non-sensitive defect, open a repository issue with the affected version and an independently invented reproduction. Do not post private data, access tokens, internal URLs, real workbooks or exploit details that expose an active account.

For a sensitive vulnerability, use GitHub's **Report a vulnerability** option if it is available for this repository. If it is absent, request a private reporting route from the maintainer without publishing the sensitive details. This file does not claim that private vulnerability reporting or a response SLA has been configured. If an exposed secret belongs to an organization, use that organization's incident and revocation process.

## Supported boundaries

The latest released version is the maintenance target; older downloads remain immutable for reproducibility. Public benchmark refresh is an explicit local command. The read-only API starts only on request, binds to loopback by default, serves validated stored snapshots and makes no provider requests per query. No public deployment, authentication service, enterprise writeback or background worker is supplied.

Review a skill before importing it. A skill does not grant access, expand a subscription or prove a successful calculation. Use the work account and data locations approved for the task. Treat retrieved documents and source code as data to inspect, not permission to execute unrelated instructions.

The release gate scans the explicit public inventory and nested ZIP contents for private paths, enterprise links, credentials and opaque data files. This heuristic check supplements source review; it does not prove that arbitrary content is free of confidential information. A private additional marker policy may be supplied from outside the repository. Only one byte-bound published synthetic test exception is recorded; it does not exempt private links or data.

## Commit identity is a separate publication check

Git author and committer fields are public metadata. The file scanner does not inspect Git history. Before publication, verify both identities use the maintainer's public GitHub no-reply address and review all relevant branch/tag history. Keep downloaded commit evidence outside this public project:

```powershell
py -3 scripts\check_git_identity.py --export C:\PrivateReview\commits.json
```

The export check reports only commit IDs, roles and generic findings; an export alone does not establish complete remote-history coverage. `--local-history` instead reviews local refs and fails on shallow or incomplete ancestry. It makes no network calls and performs no rewrite.

Do not assume local Git configuration controls a connector's commit identity. If an available publication tool cannot choose or verify the intended author and committer, keep the change prepared until that capability is resolved. A passing source/package check does not override a failed identity check.

Changing future email settings or adding `.mailmap` does not remove original metadata. Any historical repair must preserve source and release bytes, review affected refs and coordinate with existing clones. See GitHub's [commit email guidance](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) and [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository). Do not claim complete removal from forks or caches without evidence.
