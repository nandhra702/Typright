#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "tries_trial.cpp"

namespace py = pybind11;

PYBIND11_MODULE(triemodule, m) {
    py::class_<Trie>(m, "Trie")
        .def(py::init<>())
        .def("insert", &Trie::insert, "Insert a word into the Trie")
        .def("search", &Trie::search, "Check if word exists in the Trie")
        .def("startsWith", &Trie::startsWith, "Check if any word starts with a given prefix")
        .def("getWordsWithPrefix", &Trie::getWordsWithPrefix, "Get words with a prefix")
        .def("suggestClosestWords", &Trie::suggestClosestWords, "Suggest nearest words (spellcheck)");
}
