all: data/compiled/manus-mics.pdf
	echo all



data/compiled/compiled.json: scripts/* data/sources/*
	python3 scripts/compile.py



data/compiled/manus-expanded.pdf: scripts/* data/sources/*
	python3 scripts/compile.py



data/compiled/manus-mics.pdf: data/compiled/manus-expanded.pdf data/compiled/compiled.json
	python3 scripts/annotate.py



clean:
	echo clean