#!/bin/sh
# Pre-push guard: the public repo must stay engine-only.
# Fails if tracked files contain personal names or if content dirs are tracked.
# Run manually before every push, or wire as .git/hooks/pre-push.
set -e
cd "$(dirname "$0")/.."

fail=0

# Scan tracked AND untracked-not-ignored files — a new file is one `git add` away
# from being pushed, so it must meet the bar before it's staged (learned 07-17:
# a README with guarded patterns passed this guard because it wasn't tracked yet).
FILES=$(git ls-files --cached --others --exclude-standard)

if echo "$FILES" | grep -E '^(editions|\.tmp)/' ; then
  echo "FAIL: content files are tracked" >&2; fail=1
fi

# Personal-name / private-detail patterns live OUTSIDE the tracked tree
# (.pii_patterns, gitignored) so the guard itself never leaks what it guards.
if [ ! -f .pii_patterns ]; then
  echo "FAIL: .pii_patterns missing — create it (one extended-regex, e.g. 'name1|name2')" >&2
  exit 1
fi
PATTERNS=$(cat .pii_patterns)
hits=$(grep -n -i -E "$PATTERNS" $FILES 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "FAIL: personal-detail pattern in tracked files:" >&2
  echo "$hits" >&2
  fail=1
fi

[ $fail -eq 0 ] && echo "clean: engine-only, no personal details in tracked files"
exit $fail
