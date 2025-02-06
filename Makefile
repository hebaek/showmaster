.PHONY: all
all: compile publish



.PHONY: gp
gp: compile_gp publish



.PHONY: manus
manus: data/compiled/manus/manus-mics.pdf






data/sources/manus.json: data/originals/manus-nytt.pdf scripts/analyze_pdf.py
	python3 scripts/analyze_pdf.py

data/compiled/showdata/shows.json: $(wildcard data/sources/*)
	python3 scripts/compile.py



data/compiled/manus/manus-empty.pdf: data/compiled/showdata/shows.json
	python3 scripts/render.py GP empty

data/compiled/manus/manus-music.pdf: data/compiled/manus/manus-empty.pdf
	python3 scripts/render.py GP music

data/compiled/manus/manus-mics.pdf: data/compiled/manus/manus-music.pdf
	python3 scripts/render.py GP mics



data/compiled/showdata/GP/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "GP" "actor:mic/role"

data/compiled/showdata/Show\ 1/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 1" "actor:mic/role"

data/compiled/showdata/Show\ 2/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 2" "actor:mic/role"

data/compiled/showdata/Show\ 3/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 3" "actor:mic/role"

data/compiled/showdata/Show\ 4/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 4" "actor:mic/role"

data/compiled/showdata/Show\ 5/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 5" "actor:mic/role"

data/compiled/showdata/Show\ 6/actor-mic-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 6" "actor:mic/role"



data/compiled/showdata/GP/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "GP" "role:mic/actor"

data/compiled/showdata/Show\ 1/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 1" "role:mic/actor"

data/compiled/showdata/Show\ 2/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 2" "role:mic/actor"

data/compiled/showdata/Show\ 3/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 3" "role:mic/actor"

data/compiled/showdata/Show\ 4/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 4" "role:mic/actor"

data/compiled/showdata/Show\ 5/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 5" "role:mic/actor"

data/compiled/showdata/Show\ 6/role-mic-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 6" "role:mic/actor"

data/compiled/showdata/GP/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "GP" "mic:actor/role"

data/compiled/showdata/Show\ 1/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 1" "mic:actor/role"

data/compiled/showdata/Show\ 2/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 2" "mic:actor/role"

data/compiled/showdata/Show\ 3/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 3" "mic:actor/role"

data/compiled/showdata/Show\ 4/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 4" "mic:actor/role"

data/compiled/showdata/Show\ 5/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 5" "mic:actor/role"

data/compiled/showdata/Show\ 6/mic-actor-role.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 6" "mic:actor/role"

data/compiled/showdata/GP/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "GP" "mic:role/actor"

data/compiled/showdata/Show\ 1/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 1" "mic:role/actor"

data/compiled/showdata/Show\ 2/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 2" "mic:role/actor"

data/compiled/showdata/Show\ 3/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 3" "mic:role/actor"

data/compiled/showdata/Show\ 4/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 4" "mic:role/actor"

data/compiled/showdata/Show\ 5/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 5" "mic:role/actor"

data/compiled/showdata/Show\ 6/mic-role-actor.pdf: data/compiled/showdata/shows.json
	python3 scripts/create.py "Show 6" "mic:role/actor"






.PHONY: compile_gp
compile_gp:                                       \
data/compiled/showdata/shows.json                 \
data/compiled/manus/manus-empty.pdf               \
data/compiled/manus/manus-music.pdf               \
data/compiled/manus/manus-mics.pdf                \
data/compiled/showdata/GP/actor-mic-role.pdf      \
data/compiled/showdata/GP/role-mic-actor.pdf      \
data/compiled/showdata/GP/mic-actor-role.pdf      \
data/compiled/showdata/GP/mic-role-actor.pdf






.PHONY: compile
compile:                                          \
data/compiled/showdata/shows.json                 \
data/compiled/manus/manus-empty.pdf               \
data/compiled/manus/manus-music.pdf               \
data/compiled/manus/manus-mics.pdf                \
data/compiled/showdata/GP/actor-mic-role.pdf      \
data/compiled/showdata/Show\ 1/actor-mic-role.pdf \
data/compiled/showdata/Show\ 2/actor-mic-role.pdf \
data/compiled/showdata/Show\ 3/actor-mic-role.pdf \
data/compiled/showdata/Show\ 4/actor-mic-role.pdf \
data/compiled/showdata/Show\ 5/actor-mic-role.pdf \
data/compiled/showdata/Show\ 6/actor-mic-role.pdf \
data/compiled/showdata/GP/role-mic-actor.pdf      \
data/compiled/showdata/Show\ 1/role-mic-actor.pdf \
data/compiled/showdata/Show\ 2/role-mic-actor.pdf \
data/compiled/showdata/Show\ 3/role-mic-actor.pdf \
data/compiled/showdata/Show\ 4/role-mic-actor.pdf \
data/compiled/showdata/Show\ 5/role-mic-actor.pdf \
data/compiled/showdata/Show\ 6/role-mic-actor.pdf \
data/compiled/showdata/GP/mic-actor-role.pdf      \
data/compiled/showdata/Show\ 1/mic-actor-role.pdf \
data/compiled/showdata/Show\ 2/mic-actor-role.pdf \
data/compiled/showdata/Show\ 3/mic-actor-role.pdf \
data/compiled/showdata/Show\ 4/mic-actor-role.pdf \
data/compiled/showdata/Show\ 5/mic-actor-role.pdf \
data/compiled/showdata/Show\ 6/mic-actor-role.pdf \
data/compiled/showdata/GP/mic-role-actor.pdf      \
data/compiled/showdata/Show\ 1/mic-role-actor.pdf \
data/compiled/showdata/Show\ 2/mic-role-actor.pdf \
data/compiled/showdata/Show\ 3/mic-role-actor.pdf \
data/compiled/showdata/Show\ 4/mic-role-actor.pdf \
data/compiled/showdata/Show\ 5/mic-role-actor.pdf \
data/compiled/showdata/Show\ 6/mic-role-actor.pdf






.PHONY: publish
publish:
	rsync -r -v -c --delete data/compiled/showdata/ www-test/data/
	rsync -r -v -c --delete data/compiled/manus/    www-test/manus/



.PHONY: deploy
deploy: publish
	rsync -r -v -c --delete www-test/ www-deploy/
