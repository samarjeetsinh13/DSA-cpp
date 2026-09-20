#include <iostream>
#include <cstdio>
using namespace std;

int main() {
    // Complete the code.
    int a, b;
    cin >> a >> b;
    
    string nums[] = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "even", "odd"};
    
    for(int i = a; i <= b; i++){
        if(i>=1 && i<=9){
            cout << nums[i-1] << endl;
        }else{
            if(i%2 == 0){
                cout << nums[9] << endl;
            }else{
                cout << nums[10] << endl;
            }
        }
    }
    return 0;
}