#!/usr/bin/env bash
# author: deadc0de6 (https://github.com/deadc0de6)
# Copyright (c) 2017, deadc0de6
#
# ensure update relinks absolute symlinks to dotpath target
# returns 1 in case of error
#

## start-cookie
set -eu -o errtrace -o pipefail
cur=$(cd "$(dirname "${0}")" && pwd)
ddpath="${cur}/../"
PPATH="{PYTHONPATH:-}"
export PYTHONPATH="${ddpath}:${PPATH}"
altbin="python3 -m dotdrop.dotdrop"
if hash coverage 2>/dev/null; then
  mkdir -p coverages/
  altbin="coverage run -p --data-file coverages/coverage --source=dotdrop -m dotdrop.dotdrop"
fi
bin="${DT_BIN:-${altbin}}"
# shellcheck source=tests-ng/helpers
source "${cur}"/helpers
echo -e "$(tput setaf 6)==> RUNNING $(basename "${BASH_SOURCE[0]}") <==$(tput sgr0)"
## end-cookie

basedir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)
dotpath="${basedir}/dotfiles"
dst_dir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)
clear_on_exit "${basedir}"
clear_on_exit "${dst_dir}"

# dotpath content
mkdir -p "${dotpath}"
echo "dotdrop" > "${dotpath}/afile"

# alternative target (should be ignored after update)
alt_target=$(mktemp -t dotdrop-alt.XXXXXX)
echo "other" > "${alt_target}"
clear_on_exit "${alt_target}"

cfg="${basedir}/config.yaml"
cat > "${cfg}" << _EOF
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  d_abs:
    src: afile
    dst: ${dst_dir}/afile
    link: absolute
profiles:
  p1:
    dotfiles:
    - d_abs
_EOF

# install
cd "${ddpath}" | ${bin} install -f -c "${cfg}" -p p1 -V

# tamper: point deployed link elsewhere
rm "${dst_dir}/afile"
ln -s "${alt_target}" "${dst_dir}/afile"

# update should relink to dotpath target
cd "${ddpath}" | ${bin} update -f -c "${cfg}" -p p1 -V "${dst_dir}/afile"

[ ! -L "${dst_dir}/afile" ] && echo "dst not symlink" && exit 1
if [ "$(readlink "${dst_dir}/afile")" != "${dotpath}/afile" ]; then
  echo "dst symlink target wrong"
  exit 1
fi

echo "OK"
exit 0
