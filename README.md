# Improved-CKY-Parser

# Modifications

1. Horizontal Markovization:
I. If we store only sibling’s label along with the nodes’s label in the tree after binarization and removing single child parent relationship, it
increases the F1 score by 1.05% from Vanilla PCKY.
II. Horizontal binarization is done to make the grammar a bit specific so as to restrict the grammar to give better results.

2. Vertical Markovization on top of Horizontal Markovization:
I. The F1 score increases by 0.23% if we do Vertical Markovization on top of Horizontal Markovization.
II. Again, it is done to decrease non-specificity of the grammar.

3. Changing the heuristic for right binarization:I. If we add NP to the list of labels on which right binarization takes place, then it increases the F1 Score by 0.2%
II. Currently, the heuristic used is to right binarize if the node’s label is SQ. I added NP to it too.
III. NP being the highest used Non-terminal, right binarizing the tree on it increases the score.

# The current F1 score is 0.8956

## How to run:
./runme train.trees dev.strings dev.parses.post

## For evaluation purposes:
python evalb.py dev.parses.post dev.trees
