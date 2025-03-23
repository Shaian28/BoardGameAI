# BoardGameAI
The project is divideded into three files. The Tree.py makes the AI tree calculation with depth-limited minimax, checkers.py is the board made for the AI and the player to play and PlayGame.py is the game that is the game, with the AI starting.

To run the game, open bash terminal, go to the directory with `cd` and type the following line: \
`python3 PlayGame.py`

The bash terminal will then display a checkerboard with the pieces, with `b` as black piece for man `B` as black piece for king, `r` as red piece for man and `R` as red piece for king. The AI controls the black pieces and the player will control the red pieces.

The first is done by the AI and will shortly update once the AI is done thinking. The input will now appear for the player with the following line in the bash terminal:\
`Move a piece (Format: Row1 Column2 Row1 Column1 ...): `\
This message means that you have to choose the red piece, that you want to move and place it in the square you want to be in. If multiple kills happens, then also include the in between steps.\
If the red piece is in row 5 and column 2 and you want to move the piece to row 4 and column 3, then type `5 2 4 3`. If multiple kills happens from row 5 and column 2 to row 3 and column 0 and then again to row 1 column 2, then type `5 2 3 0 1 2`.

The board will process to see if the move is valid. If invalid, the bash terminal will claim `Invalid move! Try again.` and the previous sentence will repeat.\
If everything goes as it should, then the board will update with the new placement of the piece.