#______________GRAPH______________

class Node :
    
    def __init__(self, idx, data = 0) :
       
        self.id = idx
        self.data = data
        self.connectedTo = dict()

    def addNeighbour(self, neighbour , weight = 0) :
        
        if neighbour.id not in self.connectedTo.keys() :  
            self.connectedTo[neighbour.id] = weight

    
    def setData(self, data) : 
        self.data = data 

    
    def getConnections(self) : 
        return self.connectedTo.keys()

    def getID(self) : 
        return self.id

class Graph : 

    totalV = 0
    
    def __init__(self) : 
        
        self.allNodes = dict()

    def addNode(self, idx) : 
        
        if idx in self.allNodes : 
            return None
        
        Graph.totalV += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node

    def addNodeData(self, idx, data) : 
        
        if idx in self.allNodes : 
            node = self.allNodes[idx]
            node.setData(data)

    def addEdge(self, src, dst, wt = 0) : 
        
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt)
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)
    
    def isNeighbour(self, u, v) : 
        
        if u >=1 and u <= 81 and v >=1 and v<= 81 and u !=v : 
            if v in self.allNodes[u].getConnections() : 
                return True
        return False

    def getNode(self, idx) : 
        if idx in self.allNodes : 
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self) : 
        return self.allNodes.keys()


#______________GRAPH CONNECTIONS ___________________

class SudokuConnections : 
    def __init__(self) :

        self.graph = Graph()

        self.rows = 9
        self.cols = 9
        self.total_blocks = self.rows*self.cols

        self.__generateGraph()
        self.connectEdges()

        self.allIds = self.graph.getAllNodesIds()

        

    def __generateGraph(self) : 
        
        for idx in range(1, self.total_blocks+1) : 
            _ = self.graph.addNode(idx)

    def connectEdges(self) : 
        
        matrix = self.__getGridMatrix()

        head_connections = dict()

        for row in range(9) :
            for col in range(9) : 
                
                head = matrix[row][col]
                connections = self.__whatToConnect(matrix, row, col)
                
                head_connections[head] = connections

        self.__connectThose(head_connections=head_connections)
        
    def __connectThose(self, head_connections) : 
        for head in head_connections.keys() :
            connections = head_connections[head]
            for key in connections :
                for v in connections[key] : 
                    self.graph.addEdge(src=head, dst=v)

 
    def __whatToConnect(self, matrix, rows, cols) :

        connections = dict()

        row = []
        col = []
        block = []

        # ROWS
        for c in range(cols+1, 9) : 
            row.append(matrix[rows][c])
        
        connections["rows"] = row

        # COLS 
        for r in range(rows+1, 9):
            col.append(matrix[r][cols])
        
        connections["cols"] = col

        # BLOCKS
        
        if rows%3 == 0 : 

            if cols%3 == 0 :
                
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])
                block.append(matrix[rows+2][cols+1])
                block.append(matrix[rows+2][cols+2])

            elif cols%3 == 1 :
                
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+2][cols-1])
                block.append(matrix[rows+2][cols+1])
                
            elif cols%3 == 2 :
                
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+2][cols-2])
                block.append(matrix[rows+2][cols-1])

        elif rows%3 == 1 :
            
            if cols%3 == 0 :
                
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])

            elif cols%3 == 1 :
                
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                
            elif cols%3 == 2 :
                
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])

        elif rows%3 == 2 :
            
            if cols%3 == 0 :
                
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-2][cols+2])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])

            elif cols%3 == 1 :
                
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                
            elif cols%3 == 2 :
                
                block.append(matrix[rows-2][cols-2])
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
        
        connections["blocks"] = block
        return connections

    def __getGridMatrix(self) : 
        
        matrix = [[0 for cols in range(self.cols)] 
        for rows in range(self.rows)]

        count = 1
        for rows in range(9) :
            for cols in range(9):
                matrix[rows][cols] = count
                count+=1
        return matrix
        
class SudokuBoard : 
    def __init__(self) : 

        self.board = self.getBoard()
        
        self.sudokuGraph = SudokuConnections()
        self.mappedGrid = self.__getMappedMatrix() # Maps all the ids to the position in the matrix

    def __getMappedMatrix(self) : 
        matrix = [[0 for cols in range(9)] 
        for rows in range(9)]

        count = 1
        for rows in range(9) : 
            for cols in range(9):
                matrix[rows][cols] = count
                count+=1
        return matrix

    def getBoard(self) : 

        board = [
            [0, 0, 7, 0, 4, 3, 0, 1, 0],
            [4, 0, 6, 8, 0, 5, 0, 2, 0],
            [3, 8, 0, 6, 9, 0, 4, 0, 0],
            [5, 0, 0, 0, 1, 6, 0, 9, 3],
            [0, 0, 0, 3, 0, 7, 0, 6, 4],
            [6, 3, 0, 0, 0, 0, 1, 8, 0],
            [0, 0, 0, 0, 2, 8, 0, 0, 6],
            [0, 0, 0, 7, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 3, 1]
        ]
        return board

    def printBoard(self) : 
        
        print("    1 2 3     4 5 6     7 8 9")
        for i in range(len(self.board)) : 
            if i%3 == 0  :
                print("  - - - - - - - - - - - - - - ")

            for j in range(len(self.board[i])) : 
                if j %3 == 0 :
                    print(" |  ", end = "")
                if j == 8 :
                    print(self.board[i][j]," | ", i+1)
                else : 
                    print(f"{ self.board[i][j] } ", end="")
        print("  - - - - - - - - - - - - - - ")

    def is_Blank(self) : 
        
        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    return (row, col)
        return None

    def graphColoringInitializeColor(self):
        
        color = [0] * (self.sudokuGraph.graph.totalV+1)
        given = []
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] != 0 : 
                    
                    idx = self.mappedGrid[row][col]
                    
                    color[idx] = self.board[row][col]
                    
                    given.append(idx)
        return color, given

    def solveGraphColoring(self, m =9) : 
        
        color, given = self.graphColoringInitializeColor()
        if self.__graphColorUtility(m =m, color=color, v =1, given=given) is None :
            print("cannot be solved")
            return False
        count = 1
        for row in range(9) : 
            for col in range(9) :
                self.board[row][col] = color[count]
                count += 1
        return color
    
    def __graphColorUtility(self, m, color, v, given) :
        
        if v == self.sudokuGraph.graph.totalV+1  : 
            return True
        for c in range(1, m+1) : 
            if self.__isSafe2Color(v, color, c, given) == True :
                color[v] = c
                if self.__graphColorUtility(m, color, v+1, given) : 
                    return True
            if v not in given : 
                color[v] = 0

    def __isSafe2Color(self, v, color, c, given) : 
        
        if v in given and color[v] == c: 
            return True
        elif v in given : 
            return False

        for i in range(1, self.sudokuGraph.graph.totalV+1) :
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i) :
                return False
        return True


def main() : 
    s = SudokuBoard()
    print("BEFORE SOLVING ...")
    s.printBoard()
    print("\n\n\nAFTER SOLVING ...")
    print("\n\n")
    s.solveGraphColoring(m=9)
    s.printBoard()

main()

