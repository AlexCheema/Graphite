# Graphite - Python 1 liner for Graph Algorithm Succinct Proofs!

## Value Proposition
 - **ZKPs Accessible via Python:** You can generate succinct proofs for any graph algorithms, easily using just python without knowing any ZKP-domain specific languages
 - **Save gas on contracts:** Create succinct proofs for properties about graphs based on public data, without running the entire computation on gas-expensive smart contracts
 - **Optimizable:** Since each graph algorithm is updated individually, the lower-level implementation can be optimized for each algorithm, and optimized extensively
 

# Getting Started

## Requirements:
 - `python`, `pip`
 - `nargo`: Easiest way is via option 1 for `noirup`: https://noir-lang.org/getting_started/nargo_installation#option-1-noirup
 - (Optional) VSCode Noir Language Extension 


## Quick Run

`make bfs`

`make no_cycle`

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


# Internal

To build and deploy a verifier contract for a graph algorithm implemented as a noir package, do the following
1. In the noir package, run `nargo codegen-verifier`
2. Rename `plonk_vk.sol` to `some_unique_name.sol` and move it to `graphite/contracts`
3. Delete the `contract` directory generated by nargo in the noir package itself
4. In the `graphite` directory, run `source deploy.sh --rpc-url RPC_URL --verifier-contract some_unique_name.sol`, where the RPC_URL is for the testnet of the chain you want to deploy on
