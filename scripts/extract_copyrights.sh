set -exo

#FLAGS="--reload"
SUPP="/projects/grail/www/projects/xuanspace/portrait-rephotography/SIGGRAPH_Asia_Supplement_fullsize/full_results/"

for list in "showcase_photos" "historical_wiki_face_dataset"; do
    python extract_copyright.py\
        --url_json "json/19th century.json" "json/20th century.json"\
        --meta "meta/${list}.json"\
        --copyright "copyright/${list}.tsv"\
        --names "${SUPP}/${list}/data/input/"*.png --reload
done

