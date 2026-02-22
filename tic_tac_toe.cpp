#include <chrono>
#include <iostream>
#include <limits>
#include <string>
#include <thread>
#include <vector>

using namespace std;

const string RESET = "\033[0m";
const string BLUE = "\033[34m";
const string RED = "\033[31m";
const string GREEN = "\033[32m";
const string YELLOW = "\033[33m";
const string CYAN = "\033[36m";
const string MAGENTA = "\033[35m";

string coloredIcon(char symbol) {
    if (symbol == 'X') {
        return BLUE + "●" + RESET;
    }
    return RED + "●" + RESET;
}

void clearScreen() {
    cout << "\033[2J\033[H";
}

void pauseMs(int ms) {
    this_thread::sleep_for(chrono::milliseconds(ms));
}

void printHeader(int xScore, int oScore, int round, int totalRoundsToWin, int maxRounds) {
    cout << CYAN << "================ TIC TAC TOE (LOCAL MULTIPLAYER) ================\n" << RESET;
    cout << "Round: " << round << " / " << maxRounds << "\n";
    cout << "First to " << totalRoundsToWin << " wins the series\n\n";
    cout << BLUE << "Player 1 " << coloredIcon('X') << RESET << "  Score: " << xScore << "\t";
    cout << RED << "Player 2 " << coloredIcon('O') << RESET << "  Score: " << oScore << "\n";
    cout << "-----------------------------------------------------------------\n";
}

void printBoard(const vector<char>& board) {
    auto cellText = [&](int i) -> string {
        if (board[i] == 'X') return coloredIcon('X');
        if (board[i] == 'O') return coloredIcon('O');
        return to_string(i + 1);
    };

    cout << "\n"
         << " " << cellText(0) << " | " << cellText(1) << " | " << cellText(2) << "\n"
         << "---+---+---\n"
         << " " << cellText(3) << " | " << cellText(4) << " | " << cellText(5) << "\n"
         << "---+---+---\n"
         << " " << cellText(6) << " | " << cellText(7) << " | " << cellText(8) << "\n\n";
}

bool isWinningLine(const vector<char>& b, int a, int c, int d) {
    return b[a] != ' ' && b[a] == b[c] && b[c] == b[d];
}

char getWinner(const vector<char>& board) {
    static const int wins[8][3] = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
        {0, 4, 8}, {2, 4, 6}
    };

    for (const auto& w : wins) {
        if (isWinningLine(board, w[0], w[1], w[2])) {
            return board[w[0]];
        }
    }
    return ' ';
}

bool isBoardFull(const vector<char>& board) {
    for (char c : board) {
        if (c == ' ') return false;
    }
    return true;
}

int requestSeriesLength() {
    while (true) {
        cout << "Choose series format:\n";
        cout << "1) Best of 3\n";
        cout << "2) Best of 5\n";
        cout << "3) Best of 7\n";
        cout << "Enter choice (1-3): ";

        int choice;
        if (!(cin >> choice)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << YELLOW << "Invalid input. Please enter a number from 1 to 3.\n\n" << RESET;
            continue;
        }

        switch (choice) {
            case 1: return 3;
            case 2: return 5;
            case 3: return 7;
            default:
                cout << YELLOW << "Please choose 1, 2, or 3.\n\n" << RESET;
        }
    }
}

int requestMove(const vector<char>& board, char currentPlayer) {
    while (true) {
        cout << (currentPlayer == 'X' ? BLUE : RED)
             << "Player " << (currentPlayer == 'X' ? "1" : "2")
             << " " << coloredIcon(currentPlayer)
             << " - choose a cell (1-9): " << RESET;

        int move;
        if (!(cin >> move)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << YELLOW << "Invalid input. Enter a number from 1 to 9.\n" << RESET;
            continue;
        }

        if (move < 1 || move > 9) {
            cout << YELLOW << "Cell must be between 1 and 9.\n" << RESET;
            continue;
        }

        if (board[move - 1] != ' ') {
            cout << YELLOW << "That cell is already taken. Pick another one.\n" << RESET;
            continue;
        }

        return move - 1;
    }
}

void celebrationAnimation(char winner) {
    string color = (winner == 'X') ? BLUE : RED;
    string player = (winner == 'X') ? "Player 1" : "Player 2";

    vector<string> frames = {
        "   *        *        *   ",
        " *   *    *   *    *   * ",
        "   *   *  WIN!  *   *   ",
        " *   *    *   *    *   * ",
        "   *        *        *   "
    };

    for (int i = 0; i < 3; ++i) {
        clearScreen();
        cout << color << "\n\n";
        cout << "      " << player << " " << coloredIcon(winner) << " WINS THIS ROUND!\n\n";
        for (const auto& line : frames) {
            cout << "      " << line << "\n";
        }
        cout << RESET;
        pauseMs(350);
    }
}

void drawAnimation() {
    vector<string> msg = {
        "No winner this round.",
        "Board is full.",
        "It's a DRAW!"
    };

    for (const auto& line : msg) {
        cout << MAGENTA << line << RESET << "\n";
        pauseMs(280);
    }
}

void seriesWinnerAnimation(char winner, int xScore, int oScore) {
    string color = (winner == 'X') ? BLUE : RED;
    string player = (winner == 'X') ? "Player 1" : "Player 2";

    clearScreen();
    cout << color << "\n";
    cout << "#############################################################\n";
    cout << "#                                                           #\n";
    cout << "#   " << player << " " << coloredIcon(winner) << " IS THE SERIES CHAMPION!                 #\n";
    cout << "#                                                           #\n";
    cout << "#############################################################\n";
    cout << RESET;
    cout << "Final Score -> "
         << BLUE << "Player 1: " << xScore << RESET << " | "
         << RED << "Player 2: " << oScore << RESET << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    clearScreen();
    int maxRounds = requestSeriesLength();
    int roundsToWin = maxRounds / 2 + 1;

    int xScore = 0;
    int oScore = 0;
    int round = 1;

    while (xScore < roundsToWin && oScore < roundsToWin && round <= maxRounds) {
        vector<char> board(9, ' ');
        char currentPlayer = (round % 2 == 1) ? 'X' : 'O';

        bool roundDone = false;
        while (!roundDone) {
            clearScreen();
            printHeader(xScore, oScore, round, roundsToWin, maxRounds);
            printBoard(board);

            int idx = requestMove(board, currentPlayer);
            board[idx] = currentPlayer;

            char winner = getWinner(board);
            if (winner == 'X' || winner == 'O') {
                if (winner == 'X') {
                    ++xScore;
                } else {
                    ++oScore;
                }

                clearScreen();
                printHeader(xScore, oScore, round, roundsToWin, maxRounds);
                printBoard(board);
                celebrationAnimation(winner);
                roundDone = true;
            } else if (isBoardFull(board)) {
                clearScreen();
                printHeader(xScore, oScore, round, roundsToWin, maxRounds);
                printBoard(board);
                drawAnimation();
                roundDone = true;
            } else {
                currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            }
        }

        ++round;
    }

    if (xScore == oScore) {
        clearScreen();
        cout << MAGENTA << "\nSeries ended in an overall draw!" << RESET << "\n";
        cout << "Final Score -> "
             << BLUE << "Player 1: " << xScore << RESET << " | "
             << RED << "Player 2: " << oScore << RESET << "\n";
    } else {
        char seriesWinner = (xScore > oScore) ? 'X' : 'O';
        seriesWinnerAnimation(seriesWinner, xScore, oScore);
    }

    return 0;
}
