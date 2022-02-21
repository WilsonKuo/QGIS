# dependency
acstw OracleInterface requires cx_Oracle module
# packaging
https://packaging.python.org/tutorials/packaging-projects/
# build
- python -m pip install --user --upgrade setuptools wheel
- python setup.py sdist bdist_wheel
# wheel file
Wheel file will be in the ~/dist folder in root of project
# install
pip install {wheel_file_name}.whl