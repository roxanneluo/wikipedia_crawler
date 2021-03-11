#set -exo

list=$1

while read name; do
    echo "${name}"
    python wiki_downloader.py "${name}"
    python downloader.py "${name}"
done < "${list}"


