#set -exo

list=$1
list_name="${list%.*}"
list_name="${list_name##*/}"

while read name; do
    echo "${name}"
    python wiki_downloader.py "${name}" --subdir "${list_name}"
done < "${list}"

for name in "json/${list_name}/"*; do
    name="${name%.*}"
    name="${name##*/}"
    python single_downloader.py "${name}" --subdir "${list_name}"
done


