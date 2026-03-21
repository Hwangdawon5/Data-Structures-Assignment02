#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <thread> 
#include <chrono> 
#include <locale>

using namespace std;

const int FRAME_DELAY_MS = 600;

class StackAnimation {
private:
    vector<string> stack;
    int max_size;

public:
    StackAnimation(int size = 10) : max_size(size) {}

    void draw(const string& current_operation) {
#ifdef _WIN32
        system("cls");
#else
        system("clear");
#endif

        cout << "================================================" << endl;
        cout << " [현재 연산] " << current_operation << endl;
        cout << " [스택 상태] " << (int)stack.size() << " / " << max_size << endl;
        cout << "================================================" << endl;
        cout << endl;

        cout << "\t\t   [ STACK ]" << endl;
        cout << "\t\t+-----------+" << endl;

        if (stack.empty()) {
            cout << "\t\t|   Empty   |" << endl;
            cout << "\t\t+-----------+" << endl;
        }
        else {
            for (int i = (int)stack.size() - 1; i >= 0; --i) {
                printf("\t\t| %-9s |", stack[i].substr(0, 15).c_str());
                if (i == (int)stack.size() - 1) cout << " <- TOP";
                cout << "\n\t\t+-----------+" << endl;
            }
        }
        cout << endl;
        this_thread::sleep_for(chrono::milliseconds(FRAME_DELAY_MS));
    }

    bool isFull() { return (int)stack.size() >= max_size; }
    bool isEmpty() { return stack.empty(); }

    void push(const string& item) {
        if ((int)stack.size() < max_size) {
            stack.push_back(item);
            draw("PUSH: " + item);
        }
    }

    void pop() {
        if (!stack.empty()) {
            string item = stack.back();
            stack.pop_back();
            draw("POP: " + item);
        }
    }
};

vector<string> loadKeywords(const string& filename) {
    vector<string> keywords;
    ifstream file(filename);
    if (!file.is_open()) return keywords;

    string line;
    getline(file, line); // 헤더 스킵

    while (getline(file, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        string name, id, word;
        getline(ss, name, ',');
        getline(ss, id, ',');
        while (getline(ss, word, ',')) {
            word.erase(0, word.find_first_not_of(" \t\r\n\""));
            word.erase(word.find_last_not_of(" \t\r\n\"") + 1);
            if (!word.empty()) keywords.push_back(word);
        }
    }
    file.close();
    return keywords;
}

int main() {
    setlocale(LC_ALL, "");
    vector<string> all_keywords = loadKeywords("Team5_keywords.csv");
    if (all_keywords.empty()) {
        cout << "CSV 파일을 찾을 수 없습니다!" << endl;
        return 1;
    }

    StackAnimation myStack(10);
    for (const string& k : all_keywords) {
        if (myStack.isFull()) {
            for (int i = 0; i < 5; i++) myStack.pop();
        }
        myStack.push(k);
    }
    while (!myStack.isEmpty()) myStack.pop();

    cout << "\n[완료] 총 " << (int)all_keywords.size() << "개 처리 완료!" << endl;
    return 0;
}