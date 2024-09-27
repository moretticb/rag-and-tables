#!/bin/sh

echo "========== GENERATING CHUNKS ==========\n"

cd chunks
#rm chunks/chunk_*.txt
poetry run ./generate_all_chunks.sh
cd ..

echo "================ DONE =================\n\n"


echo "======= COMPARING  SIMILARITIES =======\n"

cd figs/similarity_comp
poetry run python calc_similarity.py --vendor oai --similarity cosine
cd ../..

