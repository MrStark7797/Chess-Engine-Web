#include <iostream>
#include <string>
using namespace std;
class peices {
    public:
    const int None = 0;
    const int Pawn = 1;
    const int King = 2;
    const int Queen = 3;
    const int Rook = 4;
    const int Bishop = 5;
    const int Knight = 6;

    const int White = 8;
    const int Black = 16;

}

class Board {
    public:
    Board(){

        float board[8][8] = 
        {
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
            {0, 0, 0, 0, 0, 0, 0, 0,},
        }

    }
}

int main() {





    return 0;

}