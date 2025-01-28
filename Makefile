.PHONY: all
all: publish



.PHONY: manus
manus: data/compiled/pdf/manus-mics



data/sources/manus.json: data/originals/manus-nytt.pdf
	python3 scripts/analyze_pdf.py

data/compiled/showdata/shows.json: $(wildcard data/sources/*)
	python3 scripts/compile.py



data/compiled/pdf/manus-empty.pdf: data/compiled/showdata/shows.json
	python3 scripts/render.py "$(SHOW)" empty

data/compiled/pdf/manus-music.pdf: data/compiled/pdf/manus-empty.pdf
	python3 scripts/render.py "$(SHOW)" music

data/compiled/pdf/manus-mics.pdf: data/compiled/pdf/manus-music.pdf
	python3 scripts/render.py "$(SHOW)" mics



data/compiled/pdf/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "actor:mic/role"

data/compiled/pdf/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "role:mic/actor"

data/compiled/pdf/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "mic:actor/role"

data/compiled/pdf/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "mic:role/actor"






.PHONY: publish
publish: data/compiled/showdata/shows.json data/compiled/pdf/manus-mics.pdf data/compiled/pdf/actor-mic-role.pdf data/compiled/pdf/role-mic-actor.pdf data/compiled/pdf/mic-actor-role.pdf data/compiled/pdf/mic-role-actor.pdf
	rsync -r -v -c --delete data/compiled/showdata/ www-test/data/
	rsync -r -v -c --delete data/compiled/pdf/      www-test/pdf/



.PHONY: deploy
deploy: publish
	rsync -r -v -c --delete www-test/ www-deploy/
