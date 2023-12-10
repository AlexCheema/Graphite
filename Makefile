pypi:
	python setup.py bdist bdist_wheel
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    twine upload dist/*


bfs:
	cd graphite && python3 setup_custom.py --prover_toml_name tryprover --proof_output tryoutput --algorithm bfs

no_cycle:
	cd graphite && python3 setup_custom.py --prover_toml_name tryprover --proof_output tryoutput --algorithm no_cycle

pagerank:
	cd graphite && python3 setup_custom.py --prover_toml_name tryprover --proof_output tryoutput --algorithm pagerank