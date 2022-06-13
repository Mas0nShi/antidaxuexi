all: install_dependency package

install_dependency:
	pip install -r requirements.txt

package: antidxx/template/message.txt
	python3 setup.py sdist bdist_wheel