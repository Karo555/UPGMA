# UPGMA
bIOINFORMATICS @WUST

## installation
git clone [<UPGMA>](https://github.com/Karo555/UPGMA)
uv pip install -e .

# UPGMA

An UPGMA phylogenetic‐tree builder in Python, with support for:

- FASTA or precomputed distance‐matrix input  
- Needleman–Wunsch scoring → distance conversion  
- UPGMA clustering → Newick output  
- Optional dendrogram plotting via Matplotlib  
- Editable‐install development with **uv**

---

## Features

- **Flexible input**: sequences (FASTA) or raw distance matrix (CSV/TSV/TXT)  
- **Customizable scoring**: match/mismatch/gap parameters  
- **Clean API**: `io.py`, `distance.py`, `tree.py`, `upgma.py`, `viz.py`, `cli.py`  
- **Console tool**: `UPGMA` entrypoint  
- **Editable installs**: rapid dev iterations via `uv pip install -e .`

## usage 
Build a tree from fasta <br>
`UPGMA seqs.fasta --mode sequences \
  --match 2 --mismatch -1 --gap -2 \
  --output-newick tree.nwk \
  --output-log merges.csv \
  --output-plot tree.png`

use precompted matrix
`UPGMA matrix.csv --mode matrix \
  --output-newick tree.nwk`