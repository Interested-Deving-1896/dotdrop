#!/usr/bin/env bash
# author: deadc0de6 (https://github.com/deadc0de6)
# Copyright (c) 2017, deadc0de6
#
# ensure update relinks relative symlinks to dotpath target
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
alt_target_dir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)
alt_target="${alt_target_dir}/other"
echo "other" > "${alt_target}"
clear_on_exit "${alt_target_dir}"

cfg="${basedir}/config.yaml"
cat > "${cfg}" << _EOF
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  d_rel:
    src: afile
    dst: ${dst_dir}/afile
    link: relative
profiles:
  p1:
    dotfiles:
    - d_rel
_EOF

# install
cd "${ddpath}" | ${bin} install -f -c "${cfg}" -p p1 -V

# capture expected relative target (from installed link)
expected_target=$(readlink "${dst_dir}/afile")

# tamper: point deployed link elsewhere
rm "${dst_dir}/afile"
ln -s "${alt_target}" "${dst_dir}/afile"

# update should relink to dotpath target (relative)
cd "${ddpath}" | ${bin} update -f -c "${cfg}" -p p1 -V "${dst_dir}/afile"

[ ! -L "${dst_dir}/afile" ] && echo "dst not symlink" && exit 1
new_target=$(readlink "${dst_dir}/afile")
if [ "${new_target}" != "${expected_target}" ]; then
  echo "dst relative target changed: ${new_target} (expected ${expected_target})"
  exit 1
fi

# ensure it resolves to the dotpath file
resolved=$(realpath "${dst_dir}/afile")
if [ "${resolved}" != "${dotpath}/afile" ]; then
  echo "dst symlink real target wrong"
  exit 1
fi

echo "OK"
exit 0
