#!/usr/bin/env bash

set -x

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit
trap popd EXIT

pur -z -r "requirements.in"
ec=$?
[ $ec -gt 1 ] && exit $ec || [ $ec -eq 1 ] && updated=true
[ "$updated" != true ] && echo "No packages were updated by pur, exiting." && exit 0

set -e
pip-compile --upgrade
pip-sync
pre-commit autoupdate
pre-commit run --all-files --verbose
pytest
