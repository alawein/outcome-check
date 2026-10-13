.PHONY: bench check
bench:
	uv run python benchmarks/run.py --fetch
check:
	just check
