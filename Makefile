all:
	python setup.py bdist bdist_wheel

bfs:
	cd graphite && python3 setup_custom.py --prover_toml_name tryprover --proof_output tryoutput --algorithm bfs

no_cycle:
	cd graphite && python3 setup_custom.py --prover_toml_name tryprover --proof_output tryoutput --algorithm no_cycle