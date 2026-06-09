#!/usr/bin/env bash
# author: deadc0de6 (https://github.com/deadc0de6)
# Copyright (c) 2017, deadc0de6
#
# ensure update keeps symlink children without dereferencing
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

################################################################
# this is the test
################################################################

# working directories
basedir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)
dotpath="${basedir}/dotfiles"
dst_dir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)
target_dir=$(mktemp -d --suffix='-dotdrop-tests' || mktemp -d)

clear_on_exit "${basedir}"
clear_on_exit "${dst_dir}"
clear_on_exit "${target_dir}"

# prepare dotpath content
mkdir -p "${dotpath}/whatever"
echo "existing" > "${dotpath}/whatever/existing"

target_file="${target_dir}/tgt"
echo "fromdest" > "${target_file}"

# config
cfg="${basedir}/config.yaml"
cat > "${cfg}" << _EOF
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  d_whatever:
    src: whatever
    dst: ${dst_dir}
    link: link_children
profiles:
  p1:
    dotfiles:
    - d_whatever
_EOF

# install
cd "${ddpath}" | ${bin} install -f -c "${cfg}" -p p1 -V

# user adds a new symlink in destination
ln -s "${target_file}" "${dst_dir}/newlink"

# update should copy the symlink itself (not dereference)
cd "${ddpath}" | ${bin} update -f -c "${cfg}" -p p1 -V "${dst_dir}"

src_link="${dotpath}/whatever/newlink"
[ ! -L "${src_link}" ] && echo "missing symlink in dotpath" && exit 1
[ ! -L "${dst_dir}/newlink" ] && echo "missing symlink in dst" && exit 1
if [ "$(readlink "${src_link}")" != "$(readlink "${dst_dir}/newlink")" ]; then
  echo "symlink targets differ"
  exit 1
fi

echo "OK"
exit 0
