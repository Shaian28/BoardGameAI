# BoardGameAI
The project is divideded into three files. The Tree.py makes the AI tree calculation with depth-limited minimax, checkers.py is the board made for the AI and the player to play and PlayGame.py is the game that is the game, with the AI starting.

To run the game, open bash terminal, go to the directory with `cd` and type the following line: \
`python3 PlayGame.py`

The bash terminal will then display a checkerboard with the pieces, with `b` as black piece for man `B` as black piece for king, `r` as red piece for man and `R` as red piece for king. The AI controls the black pieces and the player will control the red pieces.

The first is done by the AI and will shortly update once the AI is done thinking. The input will now appear for the player with the following line in the bash terminal:\
`Choose the piece you want to move as (column, row):`\
This message means that you have to choose the red piece, that you want to move. If the red piece is in column 2 and row 5, then type `2, 5`, with comma seperating the input. Then the next line will appear in the bash terminal:\
`Choose the move you want to make as (column, row):`\
This message mean that you to choose where the red piece should land. If the red piece should go to coloumn 3 and row 4, them type `3, 4`, with comma seperating the input.

The board will process to see if the move is valid. If invalid, the bash terminal will claim `Invalid move` and the previous sentences will repeat.\
If everything goes as it should, then the board will update with the new placement of the piece.