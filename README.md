bIOINFORMATICS @WUST

# UPGMA
An UPGMA phylogenetic‐tree builder in Python, with support for:
- FASTA or precomputed distance‐matrix input  
- Needleman–Wunsch scoring → distance conversion  
- UPGMA clustering → Newick output  
- Optional dendrogram plotting via Matplotlib  
- Editable‐install development with **uv**

## Features
- **Flexible input**: sequences (FASTA) or raw distance matrix (CSV/TSV/TXT)  
- **Customizable scoring**: match/mismatch/gap parameters  
- **Clean API**: `io.py`, `distance.py`, `tree.py`, `upgma.py`, `viz.py`, `cli.py`  
- **Console tool**: `UPGMA` entrypoint  
- **Editable installs**: rapid dev iterations via `uv pip install -e .`

---
## installation
`git clone https://github.com/Karo555/UPGMA` <br>
--> [*] <br>
`uv virtualenv .venv` <br>
`source .venv/bin/activate` <br>
`uv pip install -e .` <br>


## [*]package manager
I am using [uv](https://github.com/astral-sh/uv) as a package manager. Install it by running
`curl -LsSf https://astral.sh/uv/install.sh | sh` <br>
remeber to restart shell after installation.

## usage 
Build a tree from fasta <br>
`UPGMA UPGMA/data/example1.fasta --mode sequences \  
  -o UPGMA/output/tree1.nwk \
  --output-log UPGMA/output/merges1.csv \
  --output-plot UPGMA/output/tree1.png`<br>

use precompted matrix<br>
 `UPGMA UPGMA/data/example_matrix1.csv --mode matrix \
  -o tree.nwk \
  --output-log merges.csv \
  --output-plot tree.png`<br>

`UPGMA --help` for more
