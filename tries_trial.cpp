
// an already existing dictionary file and reading from it.

#include<stdio.h>
#include<vector>
#include <string>
#include<iostream>
#include<fstream>
#include <algorithm>
using namespace std;

/*A custom designed data structure. Each node is an array of 26 pointers and a boolean denoting if the word has ended or not*/

struct Node{
    
    Node *links[26];    //every node will have a further reference node created automatically to which it points
    bool flag = false;  //tells if end is reached or not

//function to check if the character we are looking for exists in a reference node or not
    bool containsKey(char ch){
        return (links[ch-'a']!=NULL);   
    }

 //function to insert a letter if it doesnt already exist in the Trie
    void put(char ch, Node *node){
        links[ch-'a'] = node;
        
    }

//this function helps you get the next node your current letter is pointing to. Basically returns the reference node of that letter
    Node *get(char ch){
        return links[ch-'a'];
    }

//this function turns the flag to true if the end of a word has been reached
    void setEnd(){
        flag = true;
    }

//This function helps us to know if this node is the last node. This will help us understand if the word has ended or still remains to be iterated through.
    bool isEnd(){
        return flag;
    }
};



///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

class Trie { 

//initially we define/declare a root that every trie will have
private: Node *root;

public:

    /*Initializing data structure here*/
    //class constructor
    Trie(){
        root = new Node();
    }

    /*Inserting a word into the trie*/
    void insert(string word){

        //COMPLEXITY IS O(length of word)
        
                //whenever we started, we always started from root.
                Node *node = root;  //dummy node
                int size = word.size();
                for(int i=0 ; i<size ; i++){
                    if(!node->containsKey(word[i])){
                        //we enter here if the node does not contain the letter
                        node->put(word[i],new Node()); /*so what this means is, for this node, insert this letter at the position. And assign it 
                                                        a brand new trie node which will be its reference node*/
                    }
                    //moves to the reference trie
                    node = node->get(word[i]);

                }

                //after the last node has been reached
                node->setEnd();

    }

    /*Returns true or false if the word is in trie*/
    bool search(string word){
    
    //COMPLEXITY IS O(length of word)

        //remember we are searching from root node for the word
                Node *node = root;
                int size = word.size();

                for(int i=0 ; i<size ; i++){
                    //IF THE NODE DOES NOT CONTAIN THE LETTER
                    if(!node->containsKey(word[i])){
                        return false; //MEANS THE WORD DOES NOT EXIST
                    }
                    //IF IT DOES CONTAIN THE LETTER
                    node = node->get(word[i]);
                }
                return node->isEnd();

    }

    
    /*Returns true and false if there is any word that starts with prefix in the trie*/
    bool startsWith( string prefix){

        //COMPLEXITY IS O(length of prefix)

                Node *node = root;
                int size = prefix.size();
                for(int i=0 ; i<size ; i++){
                    if(!node->containsKey(prefix[i])){
                        return false;
                    }
                    //else
                    node = node->get(prefix[i]);

                }
                return true;

    }


    void collectWords(Node* node, string currentWord, vector<string>& results) {
                if (node->isEnd()) {
                    results.push_back(currentWord);
                }

                for (char ch ='a'; ch <= 'z'; ch++) {
                    if (node->containsKey(ch)) {
                        collectWords(node->get(ch), currentWord + ch, results);
                    }
                }
    }

    /*Returns a vector that can be printed that will give out words that start with the given prefix*/
    vector<string> getWordsWithPrefix(string prefix) {
                Node* node = root;

                // Traverse to the node representing the last character of prefix
                if(startsWith(prefix)){
                    for (char ch : prefix) {
                    node = node->get(ch);
                    }

                    // Collect all words starting from that node
                    vector<string> all_words_with_prefix;
                    collectWords(node, prefix, all_words_with_prefix);
                    return all_words_with_prefix;
                    
                }

                else{
                    //means the prefix doesnt exist
                    cout<<"Words don't exist with this prefix\n";
                    return {}; //AN EMPTY VECTOR
                }
                
\
    }


    //SUGGESTS NEAREST WORDS : Levensteins distance wagner fischer approach
    int levenshteinDistance(const string& a, const string& b) {
    //first, we find the lengths of words and make a matrix from it
    int m = a.length();
    int n = b.length();
    vector<vector<int>> dp(m+1, vector<int>(n+1));

    //initialize matrix
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;

    //filling in the rest of the matrix
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (a[i-1] == b[j-1]) dp[i][j] = dp[i-1][j-1]; //(we copy the diagonal element if the letters are same)
            else dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
        }
    }

    return dp[m][n];
}


vector<string> suggestClosestWords(string input, int maxSuggestions = 5) {
    if (input.length() < 3) return {};

    string prefix = input.substr(0, 2);  // Could be 3 for better pruning
    //Node* node = (prefix);
    //if (!node) return {};

    vector<string> candidates;
    candidates = getWordsWithPrefix(prefix);
    

    vector<pair<int, string>> distances;
    for (const string& word : candidates) {
        if (abs((int)word.length() - (int)input.length()) > 2) continue;
        int dist = levenshteinDistance(input, word);
        distances.push_back({dist, word});
    }

    //sorting on the basis of shortest edit distance number
    sort(distances.begin(), distances.end());

    vector<string> suggestions;

    for (int i = 0; i < min(maxSuggestions, (int)distances.size()); i++) {
        suggestions.push_back(distances[i].second);
    }

    //this is a cool for loop, we are doing min(maxSuggestions,int(distances.size())) because, we have specified that we want min 5 closest words. so maxSuggestions = 5, now what if the number of autocomplete words is not 5 and is lets say 3. So thats why

    return suggestions;
}


};


