all: data/compiled/compiled.json data/compiled/manus-expanded.pdf data/compiled/manus-mics.pdf
	echo all



data/compiled/compiled.json: scripts/* data/sources/*
	python3 scripts/compile.py



data/compiled/manus-expanded.pdf: scripts/* data/sources/*
	python3 scripts/compile.py



data/compiled/common/manus-mics.pdf: data/compiled/common/manus-music.pdf data/compiled/showdata.json
	python3 scripts/render.py



publish:
	rm -rf www-test/data
	rm -rf www-test/pdf

	install -d www-test/data
	install -d www-test/pdf

	cp -r data/compiled/showdata/* www-test/data/
	cp -r data/compiled/pdf/*      www-test/pdf/



deploy:
	rm -rf www-deploy/*
	cp -r www-test/* www-deploy/



clean:
	echo clean
