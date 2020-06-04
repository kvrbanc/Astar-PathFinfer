import heapq
import tkinter as tk
from tkinter import messagebox


class Node:

    def __init__(self, parentNode=None, position=None):

        self.parentNode = parentNode  
        self.currentPosition = position

        self.g = 0  # g - distance to start node
        self.h = 0  # h - estimated distance to end node
        self.f = 0  # f = g + h  - total cost 

    def __eq__(self, other):
        return self.currentPosition == other.currentPosition
    
    # heapq needs 'less than' implementation
    def __lt__(self, other):
        # compare over total cost
        return self.f < other.f
    
    # heapq needs 'greater than' implementation
    def __gt__(self, other):
        # compare over total cost
        return self.f > other.f



def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.currentPosition)
        current = current.parentNode
    #return reversed path
    return list(reversed(path))


def astar(maze, start, end):

    # create start and end node
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0

    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0 # doesn't matter

    # initializing 'open' and 'closed' lists
    openList = []
    closedList = []

    # heapify the 'openList' and add the 'startNode'
    heapq.heapify(openList) 
    heapq.heappush(openList, startNode)

    # defining the squares that will be searched ( "8-neighbourhood" )
    adjacentSquares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

    # Loop until the 'endNode' is found
    while len(openList) > 0:

        # get the current node
        currentNode = heapq.heappop(openList)
        closedList.append(currentNode)

        # if the 'endNode' is reached
        if currentNode == endNode:
            # return path to the 'endNode'
            return return_path(currentNode)

        # generating children nodes
        childrenNodes = []
        
        # search adjacent squares
        for childrenPosition in adjacentSquares:

            # get node position
            x = currentNode.currentPosition[0] + childrenPosition[0]
            y = currentNode.currentPosition[1] + childrenPosition[1]
            nodePosition = ( x , y )

            # check if it's within range
            if x > (len(maze) - 1) or x < 0 or x > (len(maze[len(maze)-1]) -1) or y < 0:
                continue

            # check if it's "walkable"
            if maze[y][x] == 1 :
                continue

            # create new node and append it to 'childrenNodes'
            newNode = Node(currentNode, nodePosition)
            childrenNodes.append(newNode)

        # loop through all children nodes
        for childNode in childrenNodes:

            # if 'childNode' is already in the 'closedList'
            if childNode in closedList:
                continue

            # create the new 'g','h' and 'f' values
            childNode.g = currentNode.g + 1  
            childNode.h = ((childNode.currentPosition[0] - endNode.currentPosition[0]) ** 2) + ((childNode.currentPosition[1] - endNode.currentPosition[1]) ** 2) 
            childNode.f = childNode.g + childNode.h

            # if 'childNode' is already in 'openList'
            if childNode in openList:
                continue
        
            # add the 'childNode' to 'openList'
            heapq.heappush(openList, childNode)
    
    return None




class GUI():
    
    def __init__(self, root, parameters):
        self.root = root

        # store the parameters
        self.window_title = parameters["title"]
        self.width = parameters["width"]
        self.height = parameters["height"]
        self.borderwidth = parameters["borderwidth"]
        self.background_color = parameters["background_color"]
        self.col_num = parameters["num_of_cols"]
        self.row_num = parameters["num_of_rows"]

        self.root.title(self.window_title)
        # make a canvas
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, borderwidth=self.borderwidth, background=self.background_color)
        self.canvas.pack()

        # make a start button
        self.start_button = tk.Button( self.root, text="  Find the path!  " , command=self.callback_start  , padx=5)
        self.start_button.pack(side='left')

        # make a clear button
        self.clear_button = tk.Button( self.root, text="  Clear the grid  " , command=self.callback_clear , padx=5)
        self.clear_button.pack(side='right')

        # initialize an empty grid that will store displayed widgets
        self.grid = [[None for _ in range(self.col_num)] for _ in range(self.col_num)]

        # initialize a "maze" that will be used for A* pathfinding 
        self.maze = [[0 for _ in range(self.col_num)] for _ in range(self.row_num)]

        # for keeping "start" and "end" point
        self.end_points=list()

    def start(self):
        # run the main window loop
        self.root.mainloop()
    

    def draw_grid(self):
        # calculate rectangle dimensions and store
        self.rectangle_width = self.width / self.col_num
        self.rectangle_height = self.height / self.row_num

        # draw rectangles on a canvas
        self.grid = [[self.canvas.create_rectangle( col*self.rectangle_width, row*self.rectangle_height, (col+1)*self.rectangle_width, (row+1)*self.rectangle_height, fill=self.background_color , outline="white") for col in range(self.col_num)] for row in range(self.row_num)]


    def callback_drag_left(self,event):
        # get x , y coordinates
        x,y = event.x , event.y 

        # convert coordinates to interval [0 - col_num] and [0 - row_num]
        x = int( ( x / self.width) * self.col_num )
        y = int( ( y / self.height) * self.row_num )
        
        # jump over start/end point
        if (x ,y) in self.end_points:
            return

        # draw the "obstacle"
        self.grid[y][x] = self.canvas.create_rectangle( x*self.rectangle_width, y*self.rectangle_height, (x+1)*self.rectangle_width, (y+1)*self.rectangle_height, fill='#6A686B' , outline="#535154")
        
        # record the "obsticle" in the maze matrix
        self.maze[y][x] = 1
    

    def callback_drag_right(self,event):
        # get x , y coordinates
        x,y = event.x , event.y 

        # convert coordinates to interval [0 - col_num] and [0 - row_num]
        x = int( ( x / self.width) * self.col_num )
        y = int( ( y / self.height) * self.row_num )

        # jump over start/end point
        if (x ,y) in self.end_points:
            return

        # delete the "obstacle"
        self.canvas.delete( self.grid[y][x] )
        self.grid[y][x] = self.canvas.create_rectangle( x*self.rectangle_width, y*self.rectangle_height, (x+1)*self.rectangle_width, (y+1)*self.rectangle_height, fill=self.background_color , outline="white")
        # set the grid to None and record the removal in the maze matrix
        self.grid[y][x] = None
        self.maze[y][x] = 0


    def callback_middle(self,event):
        # get x , y coordinates
        x,y = event.x , event.y 

        # convert coordinates to interval [0 - col_num] and [0 - row_num]
        x = int( ( x / self.width) * self.col_num )
        y = int( ( y / self.height) * self.row_num )

        # record the "start" or "end" point
        if len(self.end_points) == 2:
            # remove the last point and add in a new one
            old_point = self.end_points[1]
            self.end_points[1] = self.end_points[0]
            self.end_points[0] = ( x, y )
            # remove the old point and display a new one
            self.canvas.delete( self.grid[y][x] )
            self.grid[old_point[0]][old_point[1]] = self.canvas.create_rectangle( old_point[0]*self.rectangle_width, old_point[1]*self.rectangle_height, (old_point[0]+1)*self.rectangle_width, (old_point[1]+1)*self.rectangle_height, fill=self.background_color , outline="white")
            self.grid[y][x] = self.canvas.create_rectangle( x*self.rectangle_width, y*self.rectangle_height, (x+1)*self.rectangle_width, (y+1)*self.rectangle_height, fill="#7E10F2" , outline="#B016F8")
        else:
            self.end_points.append( (x , y) )
            # display the point
            self.grid[y][x] = self.canvas.create_rectangle( x*self.rectangle_width, y*self.rectangle_height, (x+1)*self.rectangle_width, (y+1)*self.rectangle_height, fill="#7E10F2" , outline="#B016F8")

    
    def callback_start(self):
        # find the path using A*
        if len(self.end_points) == 2:
            start = self.end_points[0]
            end = self.end_points[1]
            path = astar ( self.maze , start, end )
            # if the path is None - cannot find the path
            if path is None:
                messagebox.showwarning("Error","The path cannot be found.")
            else:
                # display the path
                index=0
                for location in path:
                    index += 1
                    if index == 1 or index == (len(path)):
                        continue
                    x = location[0]
                    y = location[1]
                    self.grid[y][x] = self.canvas.create_rectangle( x*self.rectangle_width, y*self.rectangle_height, (x+1)*self.rectangle_width, (y+1)*self.rectangle_height, fill="#9BF05C" , outline="#B7F48B")
        else:
            messagebox.showinfo("Info","You haven't provided starting and ending point.")
    

    def callback_clear(self):
        # clear the grid and reinitialize everything
        self.grid = [[None for _ in range(self.col_num)] for _ in range(self.col_num)]
        self.maze = [[0 for _ in range(self.col_num)] for _ in range(self.row_num)]
        self.end_points=list()

        # disply the clear grid
        self.draw_grid()

    def bind_keys(self):
        # bind the interaction keys with callback functions
        self.canvas.bind("<B1-Motion>", self.callback_drag_left) # drag with left button
        self.canvas.bind("<B3-Motion>", self.callback_drag_right) # drag with right button
        self.canvas.bind("<Button-2>", self.callback_middle) # middle button for "start" and "end"


if __name__ == "__main__":
    
    # defint the window parameters
    parameters = {
        "title" : " A* pathfinding",
        "width" : 700,
        "height" : 700,
        "borderwidth" : 0,
        "background_color" : '#BBC2C2',
        "num_of_cols" : 50,
        "num_of_rows" : 50
    }

    #defining window
    root = tk.Tk()
    gui = GUI( root, parameters)
    # bind the keys and draw a grid
    gui.bind_keys()
    gui.draw_grid()
    # start the main loop
    gui.start()


