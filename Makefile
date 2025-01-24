.PHONY: all
.PHONY: manus



all: publish

manus: data/compiled/pdf/manus-mics



data/compiled/showdata/shows.json: $(wildcard data/sources/*)
	python3 scripts/compile.py

data/compiled/pdf/manus-mics: data/compiled/showdata/shows.json
	python3 scripts/render.py

data/compiled/pdf/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 1"







publish: data/compiled/showdata/shows.json data/compiled/pdf/actor-mic-role.pdf
	rsync -r -v -c --delete data/compiled/showdata/ www-test/data/
	rsync -r -v -c --delete data/compiled/pdf/      www-test/pdf/



deploy: publish
	rsync -r -v -c --delete www-test/ www-deploy/
