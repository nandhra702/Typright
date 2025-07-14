#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>              // for memset
#include <unistd.h>            // for close()
#include <sys/socket.h>        // for socket(), bind(), listen(), accept(), read(), write()
#include <netinet/in.h>        // for sockaddr_in
#include "tries_trial.cpp"     // Your Trie implementation

const int PORT = 4000;
const int BUFFER_SIZE = 1024;

int main() {
    // Build Trie once
    Trie trie;
    std::ifstream file("wordlist.txt");
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) trie.insert(line);
    }
    std::cout << "Trie loaded, starting server on port " << PORT << "\n";

    // Create socket
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    sockaddr_in address;
    std::memset(&address, 0, sizeof(address));  // Clear struct
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind socket
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen
    if (listen(server_fd, 5) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    // Accept loop
    while (true) {
        int client_fd = accept(server_fd, nullptr, nullptr);
        if (client_fd < 0) {
            perror("Accept failed");
            continue;
        }

        char buffer[BUFFER_SIZE] = {0};
        read(client_fd, buffer, BUFFER_SIZE);

        // buffer format: "mode word\n"
        std::string request(buffer);
        auto spacePos = request.find(' ');
        std::string mode = request.substr(0, spacePos);
        std::string word = request.substr(spacePos + 1);
        if (!word.empty() && word.back() == '\n') word.pop_back();

        std::vector<std::string> output;
        if (mode == "autocomplete") {
            output = trie.getWordsWithPrefix(word);
        } else if (mode == "spellcheck") {
            output = trie.suggestClosestWords(word);
        }

        for (const auto& s : output) {
            write(client_fd, s.c_str(), s.size());
            write(client_fd, "\n", 1);
        }
        close(client_fd);
    }

    close(server_fd);
    return 0;
}
