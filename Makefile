.PHONY: all
all:
	make publish SHOW="GP"
	make publish SHOW="Show 1"
	make publish SHOW="Show 2"
	make publish SHOW="Show 3"
	make publish SHOW="Show 4"
	make publish SHOW="Show 5"
	make publish SHOW="Show 6"



.PHONY: manus
manus: data/compiled/manus/manus-mics



data/sources/manus.json: data/originals/manus-nytt.pdf
	python3 scripts/analyze_pdf.py

data/compiled/showdata/shows.json: $(wildcard data/sources/*)
	python3 scripts/compile.py



data/compiled/manus/manus-empty.pdf: data/compiled/showdata/shows.json
	python3 scripts/render.py "$(SHOW)" empty

data/compiled/manus/manus-music.pdf: data/compiled/manus/manus-empty.pdf
	python3 scripts/render.py "$(SHOW)" music

data/compiled/manus/manus-mics.pdf: data/compiled/manus/manus-music.pdf
	python3 scripts/render.py "$(SHOW)" mics



"data/compiled/showdata/$(SHOW)/actor-mic-role.pdf": data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "actor:mic/role"

"data/compiled/showdata/$(SHOW)/role-mic-actor.pdf": data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "role:mic/actor"

"data/compiled/showdata/$(SHOW)/mic-actor-role.pdf": data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "mic:actor/role"

"data/compiled/showdata/$(SHOW)/mic-role-actor.pdf": data/compiled/showdata/shows.json
	python3 scripts/create.py "$(SHOW)" "mic:role/actor"






.PHONY: publish
publish: \
data/compiled/showdata/shows.json \
data/compiled/manus/manus-mics.pdf \
"data/compiled/showdata/$(SHOW)/actor-mic-role.pdf" \
"data/compiled/showdata/$(SHOW)/role-mic-actor.pdf" \
"data/compiled/showdata/$(SHOW)/mic-actor-role.pdf" \
"data/compiled/showdata/$(SHOW)/mic-role-actor.pdf"
	rsync -r -v -c --delete data/compiled/showdata/ www-test/data/
	rsync -r -v -c --delete data/compiled/manus/    www-test/manus/



.PHONY: deploy
deploy: publish
	rsync -r -v -c --delete www-test/ www-deploy/
