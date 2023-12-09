all:
	python setup.py bdist bdist_wheel

test_run:
	cd graphite && python setup_custom.py --prover_toml_name tryprover --proof_output tryoutput
