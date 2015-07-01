.PHONY: test install

test:
	nosetests -v test

install:
	python setup.py install
