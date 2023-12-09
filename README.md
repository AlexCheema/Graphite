# Graphite - Write Succinct Proofs for Graphs easily!

## Value Proposition
 - **ZKPs Accessible via Python:** You can generate Succinct proofs for any graph algorithms, easily using just python without knowing any ZKP-domain specific languages
 - **Save gas on contracts:** Create succinct proofs for properties about graphs based on public data, without running the entire computation on the gas-expensive smart contracts
 - **Optimizable:** Since each graph algorithm is updated individually, the lower-level implementation can be optimized for each algorithm, and optimized extensively
 

# Getting Started

## Quick Run

`make test_run`

## Playing around

Take a look at `graphite/setup_custom.py`:
```python
def main(args=None):
    if args is None:
        args = parse_args()
...
```

Essentially, just need to put the `networkx` graph `G` and `u_index` which is the index of the graph `G` to run BFS from.

## Make sure:
 - `G` is indexed by indicies `[0,1,2,3,...]`
 - `G` is at most `10` nodes (Prototype only, will be fixed)



# Demo

Try out `demo.ipynb`! Shows you how to create a succinct proof easily in the notebook.
