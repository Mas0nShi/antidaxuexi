all: package

package: antidxx/template/message.txt
	python3 setup.py sdist bdist_wheel