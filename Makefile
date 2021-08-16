IMAGE := ponylang/pony-lldb-tester:latest

all: build

build: Dockerfile pony_lldb.py
	docker build --pull -t "${IMAGE}" .
	touch $@

pylint: build
	docker run --entrypoint pylint --rm "${IMAGE}" /pony_lldb.py

.PHONY: pylint
