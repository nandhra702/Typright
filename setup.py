from setuptools import setup, Extension
from pybind11.setup_helpers import build_ext
import pybind11

ext_modules = [
    Extension(
        "triemodule",
        sources=["bindings.cpp"],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True)
        ],
        language="c++"
    ),
]

setup(
    name="triemodule",
    version="0.0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},  # Needed for pybind11
)
