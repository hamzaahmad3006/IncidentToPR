#!/usr/bin/env bash
# Checks that every commit about to be pushed belongs to hamzaahmad3006 and
# carries no AI co-author trailer. Usage: verify.sh [--all]
set -u

EXPECTED_NAME="hamzaahmad3006"
EXPECTED_EMAIL="hamzaahmad3006@gmail.com"
fail=0

name="$(git config --local user.name || true)"
email="$(git config --local user.email || true)"
if [ "$name" != "$EXPECTED_NAME" ] || [ "$email" != "$EXPECTED_EMAIL" ]; then
  echo "FAIL: repo-local identity is '$name <$email>', expected '$EXPECTED_NAME <$EXPECTED_EMAIL>'"
  echo "      fix with: git config user.name $EXPECTED_NAME && git config user.email $EXPECTED_EMAIL"
  fail=1
fi

if [ "${1:-}" = "--all" ]; then
  range="HEAD"
elif git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
  range="@{u}..HEAD"
else
  # No upstream yet: everything on this branch will be pushed.
  range="HEAD"
fi

if ! git rev-parse --verify -q HEAD >/dev/null; then
  echo "No commits yet."
else
  while IFS=$'\t' read -r sha an ae cn ce; do
    if [ "$an" != "$EXPECTED_NAME" ] || [ "$ae" != "$EXPECTED_EMAIL" ] \
       || [ "$cn" != "$EXPECTED_NAME" ] || [ "$ce" != "$EXPECTED_EMAIL" ]; then
      echo "FAIL: $sha author '$an <$ae>' committer '$cn <$ce>'"
      fail=1
    fi
    if git log -1 --format=%B "$sha" | grep -Eiq 'co-authored-by|claude|anthropic|generated with|bob <|noreply@'; then
      echo "FAIL: $sha message mentions co-authorship or an AI tool:"
      git log -1 --format=%B "$sha" | grep -Ei 'co-authored-by|claude|anthropic|generated with|bob <|noreply@' | sed 's/^/      /'
      fail=1
    fi
  done < <(git log --format='%H%x09%an%x09%ae%x09%cn%x09%ce' $range)
fi

if [ "$fail" -eq 0 ]; then
  echo "OK"
  exit 0
fi
exit 1
