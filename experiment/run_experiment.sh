#!/bin/sh

cd .. # main project directory

echo "========== GENERATING CHUNKS ==========\n"

cd chunks
[ -e chunk_decomp.txt ] && rm chunk_decomp.txt && echo "Removing current chunk_decomp.txt"
[ -e chunk_pypdf.txt ]  && rm chunk_pypdf.txt  && echo "Removing current chunk_pypdf.txt"
[ -e chunk_reveng.txt ] && rm chunk_reveng.txt && echo "Removing current chunk_reveng.txt"
poetry run ./generate_all_chunks.sh
cd ..

echo "================ DONE =================\n\n"




echo "======= COMPARING  SIMILARITIES =======\n"

cd experiment
poetry run python calc_similarity.py
cd ..

echo "================ DONE =================\n\n"




echo "============== PLOTTING ===============\n"

cd figs/similarity_comp
poetry run python plot_comparison.py --vendor oai --similarity cosine --plot
cd ../..

echo "================ DONE =================\n\n"
