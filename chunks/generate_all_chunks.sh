#!/bin/sh

echo "Generating chunks for three approaches. This may take a while..."
echo "Existing files will be skipped. Delete the respective file to re-generate it.\n"

# decomposition approach
echo " - Decomposition..."
[ -e chunk_decomp.txt ] && echo "Skipped. File already exists.\n"
[ -e chunk_decomp.txt ] || python generate_chunk_multimodal.py decomp > chunk_decomp.txt

# reverse engineering approach
echo " - Reverse Engineering..."
[ -e chunk_reveng.txt ] && echo "Skipped. File already exists.\n"
[ -e chunk_reveng.txt ] || python generate_chunk_multimodal.py rev > chunk_reveng.txt

# pypdf approach
echo " - PyPDF..."
[ -e chunk_pypdf.txt ] && echo "Skipped. File already exists.\n"
[ -e chunk_pypdf.txt ] || python generate_chunk_pypdf.py rev > chunk_pypdf.txt

echo "\nDone! Check date/time of the generated files to see which ones are recent:"
ls -l chunk_*.txt | awk '{print $6,$7,$8,$9}'
