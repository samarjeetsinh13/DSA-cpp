#include <bits/stdc++.h> 
using namespace std; 

string ltrim(const string &); 
string rtrim(const string &); 

int main() { 
    string n_temp; 
    getline(cin, n_temp); 
    int n = stoi(ltrim(rtrim(n_temp))); 

    string arr[] = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "Greater than 9"}; 

    if(n <= 9){ 
        cout << arr[n-1] << endl; 
    } else { 
        cout << arr[9] << endl; 
    } 

    return 0; 
} 

// FIXED: Replaced std::not1 and std::ptr_fun with a modern C++ lambda expression
string ltrim(const string &str) { 
    string s(str); 
    s.erase( 
        s.begin(), 
        find_if(s.begin(), s.end(), [](unsigned char ch) { return !isspace(ch); }) 
    ); 
    return s; 
} 

// FIXED: Replaced std::not1 and std::ptr_fun with a modern C++ lambda expression
string rtrim(const string &str) { 
    string s(str); 
    s.erase( 
        find_if(s.rbegin(), s.rend(), [](unsigned char ch) { return !isspace(ch); }).base(), 
        s.end() 
    ); 
    return s; 
}