import copy

# hexapawn returns the optimal next move given the boardState, boardSize, maximizer, and searchDepth.
def hexapawn(boardState, boardSize, player, searchDepth):
    hexapawnBoard = Board(boardState, boardSize)
    maxValue, outBoard = max(hexapawnBoard, player, player, float('-inf'), float('inf'), searchDepth)

    return outBoard.toOutput()

# MINIMAX SEARCH

# max is the max function for the minimax implementation. The function has a base case where depth == 0
# or the game is finished and already has a result. Otherwise is will generate moves, then go through
# each move and run min on those moves. It will then update the maxMove if the return value from min is larger. 
# This implementation uses alpha-beta pruning and if the maxValue is larger than beta it will immediately return without
# looking at the other possible moves.
def max(board, maximizer, playerToMove, alpha, beta, depth):

    if(depth == 0 or board.isFinished()):
        return(board.evaluate(maximizer, playerToMove), board)

    possibleMoves = board.generateMoves(playerToMove)
    maxValue = float('-inf')

    if(not possibleMoves):
        return(board.evaluate(maximizer, playerToMove), board)
    
    if(playerToMove == 'w'):
        nextPlayerToMove = 'b'
    else:
        nextPlayerToMove = 'w'


    for move in possibleMoves:
        newBoard = copy.deepcopy(board)
        newBoard.move(move[0],move[1])
        value = newBoard.evaluate(maximizer, playerToMove)
        
        mini, miniBoardState = min(newBoard, maximizer, nextPlayerToMove, alpha, beta, depth-1)

        if mini > maxValue:
            maxValue = mini
            maxMove = newBoard

        if maxValue >= beta:
            return (maxValue, maxMove)

        if maxValue > alpha:
            alpha = maxValue
    
    return (maxValue, maxMove)

# min is the min function for the minimax implementation. The function has a base case where depth == 0
# or the game is finished and already has a result. Otherwise is will generate moves, then go through
# each move and run max on those moves. It will then update the minMove if the return value from max is smaller. 
# This implementation uses alpha-beta pruning and if the minValue is less than alpha it will immediately return without
# looking at the other possible moves.
def min(board, maximizer, playerToMove, alpha, beta, depth):

    if(depth == 0 or board.isFinished()):
        return(board.evaluate(maximizer, playerToMove), board)

    possibleMoves = board.generateMoves(playerToMove)
    minValue = float('inf')

    if(not possibleMoves):
        return(board.evaluate(maximizer, playerToMove), board)

    if(playerToMove == 'w'):
        nextPlayerToMove = 'b'
    else:
        nextPlayerToMove = 'w'


    for move in possibleMoves:
        newBoard = copy.deepcopy(board)
        newBoard.move(move[0],move[1])
        value = newBoard.evaluate(maximizer, playerToMove)

        maxi, maxiBoardState = max(newBoard, maximizer, nextPlayerToMove, alpha, beta, depth-1)

        if maxi < minValue:
            minValue = maxi
            minMove = newBoard  

        if minValue <= alpha:
            return (minValue, minMove)

        if minValue < beta:
            beta = minValue
                
    return (minValue, minMove)


class Board:

    # init for Board which sets the boardState to the given boardState and initializes
    # the pawn position lists.
    def __init__(self, boardState, boardSize):
        self.boardState = []
        self.boardSize = boardSize
        self.blackPawns = []
        self.whitePawns = []

        for i in range(self.boardSize):
            row = []
            for j in range(self.boardSize):
                row.append(boardState[i][j])

            self.boardState.append(row)

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if(boardState[i][j] == 'b'):
                    self.blackPawns.append((j,i))
                elif(boardState[i][j] == 'w'):
                    self.whitePawns.append((j,i))


    # BOARD EVALUATION

    # evaluate returns the score of a given board based on the perspective of player
    # and the context of the next player to move being playerToMove.
    # It evaluates based on number of pawn advantage, clear paths, and winning board states.
    #
    # Pawn Advantage will take the player pawns - enemy pawns and add that to the score.
    #
    # Clear Paths will take the player pawns with clear paths - enemy pawns with clear paths and add that to the score.
    #
    # If playerToMove has no moves given in generateMoves, if player is playerToMove the board is assigned -10 otherwise,
    # the board is assigned 10.
    #
    # If a white pawn is found on the bottom of the board and the player is white, the board is assigned a 10, otherwise it is assigned a -10.
    # If a black pawn if found on the top of the board and the player is black, the board is assigned a 10, otherwise it is assigned a -10.
    #
    # The win condition in which there are no pawns left is covered by the no possible moves win condition because if there are no pawns then there are no moves.

    def evaluate(self, player, playerToMove):

        score = 0

        if(player == 'w'):
            score += (len(self.whitePawns) - len(self.blackPawns))
        elif(player == 'b'):
            score += (len(self.blackPawns) - len(self.whitePawns))

        for i in range(self.boardSize):
            clearPath = 1
            column = ''
            for j in range(self.boardSize):
                column += self.boardState[j][i]

            currentChar = '-'
            for j in range(self.boardSize):
                if(column[j].isalpha() and currentChar.isalpha() and currentChar != column[j]):
                    clearPath = 0
                
                if(column[j].isalpha()):
                    currentChar = column[j]
            if(currentChar == player):
                score += clearPath
            elif(currentChar.isalpha()):
                score -= clearPath

        for i in range(self.boardSize):
            if(player == 'w'):
                if(self.boardState[self.boardSize-1][i] == 'w'):
                    return 10
                elif(self.boardState[0][i] == 'b'):
                    return -10
            elif(player == 'b'):
                if(self.boardState[self.boardSize-1][i] == 'w'):
                    return -10
                elif(self.boardState[0][i] == 'b'):
                    return 10

        if(not self.generateMoves(playerToMove)):
            if(playerToMove == player):
                return -10
            else:
                return 10

        return score


    # syncBoardState updates the boardState of this board to by filling the board with '-'
    # then replacing the correct '-' based on the locations given in the pawn position lists.
    def syncBoardState(self):

        self.boardState = []
        for i in range(self.boardSize):
            row = []

            for j in range(self.boardSize):
                row.append('-')

            self.boardState.append(row)

        for whitePawn in self.whitePawns:
            self.boardState[whitePawn[1]][whitePawn[0]] = 'w'

        for blackPawn in self.blackPawns:
            self.boardState[blackPawn[1]][blackPawn[0]] = 'b'

    # MOVE GENERATION

    # generateMoves returns the list of all possible moves that a player can make.
    # It takes the parameter of playerToMove as which player's turn is being taken.
    # It then generates a list of all possible forward moves and all possible diagonal moves
    # and concatenates them, then returns.
    def generateMoves(self, playerToMove):

        possibleMoves = self.generateForwardMoves(playerToMove) + self.generateDiagonalMoves(playerToMove)

        return possibleMoves


    # generateForwardMoves returns the possible forward moves that a player can make.
    # It takes the parameter of playerToMove to determine which player's pawn list to search.
    # It will look at every pawn in the corresponding color's pawn position list and cross reference
    # the opposite color's pawn position list and it's own to see if there is an enemy or friendly pawn in front.
    # If there is not then it will add the move as a possible move.
    def generateForwardMoves(self, playerToMove):

        possibleMoves = []

        if(playerToMove == 'w'):
            for whitePawn in self.whitePawns:
                if((whitePawn[0],whitePawn[1]+1) not in self.blackPawns and (whitePawn[0],whitePawn[1]+1) not in self.whitePawns and whitePawn[1]+1 < self.boardSize):

                    temp = [(whitePawn[0],whitePawn[1]),(whitePawn[0],whitePawn[1]+1)]

                    possibleMoves.append(temp)

        elif(playerToMove == 'b'):
            for blackPawn in self.blackPawns:
                if((blackPawn[0],blackPawn[1]-1) not in self.whitePawns and (blackPawn[0],blackPawn[1]-1) not in self.blackPawns and blackPawn[1]-1 < self.boardSize):

                    temp = [(blackPawn[0],blackPawn[1]),(blackPawn[0],blackPawn[1]-1)]

                    possibleMoves.append(temp)

        return possibleMoves


    # generateDiagonalMoves returns the possible diagonal moves that a player can make.
    # It takes the parameter of playerToMove to determine which player's pawn list to search.
    # It will look at each pawn in the corresponding color's pawn position list and cross 
    # reference the opposite color's pawn position list to see if there is an enemy pawn on the diagonal.
    # If there is then it will add the move as a possible move.
    def generateDiagonalMoves(self, playerToMove):

        possibleMoves = []

        if(playerToMove == 'w'):
            for whitePawn in self.whitePawns:
                if((whitePawn[0]+1,whitePawn[1]+1) in self.blackPawns):
                    temp = [(whitePawn[0],whitePawn[1]),(whitePawn[0]+1,whitePawn[1]+1)]
                    possibleMoves.append(temp)
                elif((whitePawn[0]-1,whitePawn[1]+1) in self.blackPawns):
                    temp = [(whitePawn[0],whitePawn[1]),(whitePawn[0]-1,whitePawn[1]+1)]
                    possibleMoves.append(temp)
        
        elif(playerToMove == 'b'):
            for blackPawn in self.blackPawns:
                if((blackPawn[0]+1,blackPawn[1]-1) in self.whitePawns):
                    temp = [(blackPawn[0],blackPawn[1]),(blackPawn[0]+1,blackPawn[1]-1)]
                    possibleMoves.append(temp)
                if((blackPawn[0]-1,blackPawn[1]-1) in self.whitePawns):
                    temp = [(blackPawn[0],blackPawn[1]),(blackPawn[0]-1,blackPawn[1]-1)]
                    possibleMoves.append(temp)

        return possibleMoves


    # move makes a move on the board given an origin and destination position
    # The function will check which color piece is currently at the origin then
    # update the list of pawn locations of the corresponding pawn color type. If
    # there is an enemy pawn on that position is will remove it. It will then call 
    # syncBoardState in order to update the board state based on pawn position lists.
    # 
    # move will have unaccounted for issues if moving a pawn onto a position where a
    # friendly pawn is. 
    def move(self, origin, destination):

        pieceType = self.boardState[origin[1]][origin[0]]

        if(pieceType == 'w'):
            if(origin in self.whitePawns):
                self.whitePawns[self.whitePawns.index(origin)] = destination

            if(destination in self.blackPawns):
                self.blackPawns.remove(destination)
        elif(pieceType == 'b'):
            if(origin in self.blackPawns):
                self.blackPawns[self.blackPawns.index(origin)] = destination

            if(destination in self.whitePawns):
                self.whitePawns.remove(destination)

        self.syncBoardState()

    # toOutput returns the boardState in the desired format by the assignment.
    def toOutput(self):
        output = []
        for line in self.boardState:
            output.append("".join(line))

        return output
    

    # isFinished returns true if the board is in a state where either player has won and false otherwise.
    def isFinished(self):
        return self.evaluate('w', 'w') == 10 or self.evaluate('w', 'w') == -10

