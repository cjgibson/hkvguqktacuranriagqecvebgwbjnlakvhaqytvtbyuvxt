#! /bin/bash

#---#---#---#---#---#---#---#---#---#---#
# Code courtesy of jilles via StackOverflow:
# http://stackoverflow.com/a/3951175
case $1 in
  ''|*[!0-9]*) echo "Argument 1 must be an integer value." >&2 ; exit 2 ;;
  *) ;;
esac
#---#---#---#---#---#---#---#---#---#---#

# Note: Only checks that a filename is valid for ext4 filesystems.
#   Not guaranteed to ensure filenames are valid on other filesystems.
#   Admittedly, it might not even ensure valid filenames on ext4.
for i in ${@:2}; do
  case $i in
    ''|*[/]*) echo "'$i' is not a valid filename." >&2 ; exit 2 ;;
    *[![:print:]]*) echo "'$i' is not a valid filename." >&2 ; exit 2 ;;
    *) gen_files=${@:2} ;;
  esac
done

format_length=${#1}

echo "This script will create ${1} folders, numbered from `printf "%0${format_length}d" 1` to ${1}."

if [ $# -ge 2 ]; then
  echo "Additionally, the following empty files will be created in each folder:"
  file_list="  "
  for i in ${@:2}; do
    file_list+="  $i"
    if [ ${#file_list} -ge 80 ]; then
      echo $file_list
      file_list="  "
    fi
  done
  if [ ${#file_list} -gt 2 ]; then
    echo $file_list
  fi
fi

read -p "Is the above information correct? [y/n]" ans
case $ans in
  [Yy]* ) ;;
  *) echo "Program terminated by user." >&2 ; exit 1 ;;
esac

range={`printf "%0${format_length}d" 1`..$1}

for d in `eval echo $range`; do
  mkdir $d
  cd $d
  for f in $gen_files; do
    touch $f
  done
  cd ..
done
