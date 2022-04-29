import folium
from folium import plugins
from tkinter import *
import os
import json
import tkinter as tk
import webbrowser

class navigator:
    def __init__(self):
        self.geoResources = {}
        self.Location =(24.904678, 67.137966)
        self.position = 'Garden'
        self.destination = 'Courts'

        for root, dirs, files in os.walk('DSA-project'):  
            for file in files:
                self.geoResources[file.split('.')[0]] = root+'/'+file

    def changeDestination(self,newDestination, draw=True):
        if newDestination[-5:]!="False":
          self.destination = newDestination
        #print(self.destination[-5:])
          if self.destination!=self.position:
            self.redrawMap()
        else:
          self.destination=newDestination[:len(newDestination)-5]

    def changeStartPoint(self, newStartPoint, draw=True):
        
        self.position = newStartPoint 
        if self.destination!=self.position:
          self.redrawMap()
        

    def drawPathWay(self,Map):
      
      def switchPosition(coordinate):
        temp = coordinate[0]
        coordinate[0] = coordinate[1]
        coordinate[1] = temp
        return coordinate

      searchString = self.position +"To"+ self.destination
      with open(self.geoResources[searchString]) as f:
           testWay = json.load(f)

      for feature in testWay['features']:
        path = feature['geometry']['coordinates']

      finalPath = list(map(switchPosition,path))
      folium.plugins.AntPath(finalPath).add_to(Map)

    def drawBuilding(self,Map):

      def switchPosition(coordinate):
        temp = coordinate[0]
        coordinate[0] = coordinate[1]
        coordinate[1] = temp
        return coordinate

      hauseOutline = 'DSA-project/Main Map.geojson'
      folium.GeoJson(hauseOutline, name="geojson").add_to(Map)
      markers={}
      points=['Amphitheatre','C-001','C-004','C-007','C-015','C-025','Courts','Dukaan','Dhabba','E-010','E-011','E-012','Female Lounge','Garden','Gym','Learn Courtyard','Linux Lab','Lockers','Music Room','Swimming Pool','Table Tennis','Tapal Cafeteria','W-004','W-002','W-003','Washroom 1','Washroom 2','Washroom 3']
      for root, dirs, files in os.walk('DSA-project/Markers'):  
        for file in files:
          markers[file.split('.')[0]] = root+'/'+file
      for i in points:
        searchString = i + " M"
        with open(markers[searchString]) as f:
          testWay = json.load(f)

        for feature in testWay['features']:
          mark = feature['geometry']['coordinates']
    
          mark = list(switchPosition(mark))
          tooltip = "Click"
          name = i +".html"
          (folium.Marker(mark, popup=i, tooltip=tooltip).add_to(Map))
          Map.save(name)
        

    def redrawMap(self):
        Map = folium.Map(location = self.Location, width = "75%", zoom_start = 18)
        self.drawPathWay(Map)
        self.drawBuilding(Map)
        Map.save('map.html')
        webbrowser.open('map.html', new=2)
        
myNavigator = navigator()
def displayWay(whereTo, draw=True):
    myNavigator.changeDestination(whereTo)
def changePosition(whereFrom, Draw=True):
    myNavigator.changeStartPoint(whereFrom)

# Dijkstra
def Enqueue(queue, item, priority):
    x = (item, priority,)
    if queue == []:
        queue.append(x)
    else:
        for i in range(len(queue)): 
            if priority < queue[i][1]:
                queue.insert(i,(x))
                break
        else:
            queue.append((item,priority,))
                   

def Dequeue(queue):
    x = queue[0][0]
    queue.remove(queue[0])
    return x

def getNeighbors(G, node):
    neighbors = []
    for j in G[node]:
        neighbors.append(j[0])
    return neighbors
def getShortestPath(graph, start, to):
  parent={}
  dist = {}
  for i in graph:
    dist[i] = float('inf')
    parent[i] = ''
  
  dist[start] = 0
  parent[start] = start
  Q = []
  Enqueue(Q,start,0)
  visited = []

  while Q:
    x = Dequeue(Q)
    visited.append(x)  
    neighbors = getNeighbors(graph,x)
    for i in neighbors:
      for j in graph[x]:
        if j[0] == i and i not in visited:     
          if dist[i] > dist[x] + j[1]:
            dist[i] = dist[x] + j[1]
            Enqueue(Q, i, dist[i])
            parent[i] = x

  path=[to]
  x=parent[to]
  while x!=start:
    path.append(x)
    x=parent[x]
  path.append(start)
  path.reverse()
  return path

G={'Female Lounge': [('Learn Courtyard', 1)], 'Learn Courtyard': [('Female Lounge', 1), ('W-002', 10), ('C-001', 29)], 'W-002': [('Learn Courtyard', 10), ('W-003', 2)], 'W-003': [('W-002', 2), ('Washroom 3', 1)], 'Washroom 3': [('W-003', 1), ('W-004', 15)], 'W-004': [('Washroom 3', 15), ('C-025', 8), ('Table Tennis', 42)], 'C-025': [('W-004', 8), ('Amphitheatre', 5)], 'Table Tennis': [('W-004', 42), ('Swimming Pool', 6), ('Amphitheatre', 20), ('Lockers', 11)], 'Swimming Pool': [('Table Tennis', 6)], 'Amphitheatre': [('C-025', 5), ('Table Tennis', 20), ('Washroom 2', 3)], 'Washroom 2': [('Amphitheatre', 3), ('C-015', 28)], 'Lockers': [('Table Tennis', 11), ('Gym', 15), ('C-015', 8)], 'Gym': [('Lockers', 15)], 'C-015': [('Washroom 2', 28), ('Lockers', 8), ('Dhabba', 8)], 'Dhabba': [('C-015', 8), ('Garden', 6), ('Dukaan', 13)], 'Garden': [('Dhabba', 6), ('Courts', 42)], 'Courts': [('Garden', 42)], 'Dukaan': [('Dhabba', 13), ('Tapal Cafeteria', 2)], 'Tapal Cafeteria': [('Dukaan', 2), ('C-007', 7)], 'C-007': [('Tapal Cafeteria', 7), ('C-004', 17), ('E-012', 45)], 'C-004': [('C-007', 17), ('C-001', 16)], 'C-001': [('Learn Courtyard', 29), ('C-004', 16), ('Music Room', 15)], 'E-012': [('C-007', 45), ('E-011', 3)], 'E-011': [('E-012', 3), ('E-010', 8)], 'E-010': [('E-011', 8), ('Linux Lab', 22)], 'Linux Lab': [('E-010', 22), ('Washroom 1', 5), ('Music Room', 2)], 'Washroom 1': [('Linux Lab', 5)], 'Music Room': [('C-001', 15), ('Linux Lab', 2)]}

def abra():
  parent = tk.Tk() 

  parent.geometry("200x150") 
  parent.title("Checkpoint")  
  Label(parent, text="Checkpoint",font=("Arial", 15),height=1, width=35, bg="#FF0099", fg="white").pack()
  Label(parent, text="").pack()
  my_button = tk.Button(parent, text='Show checkpoint', height=1, width=35, command=parent.destroy,bg = "#ba83c9", fg ="white")
  my_button.pack() 
  parent.mainloop()
  

def output(lst):
  print(lst)
  displayWay(lst[0] + "False")
  for i in range(len(lst)-1):
    abra()
    changePosition(lst[i])
    displayWay(lst[i+1])
  return


# def dropdown():
options = ['Amphitheatre','C-001','C-004','C-007','C-015','C-025','Courts','Dukaan','Dhabba','E-010','E-011','E-012','Female Lounge','Garden','Gym','Learn Courtyard','Linux Lab','Lockers','Music Room','Swimming Pool','Table Tennis','Tapal Cafeteria','W-024','W-002','W-003','Washroom 1','Washroom 2','Washroom 3']


root = tk.Tk()
root.title('Path')
frame = Frame(root)
root.geometry('500x500')
options = ['Amphitheatre','C-001','C-004','C-007','C-015','C-025','Courts','Dukaan','Dhabba','E-010','E-011','E-012','Female Lounge','Garden','Gym','Learn Courtyard','Linux Lab','Lockers','Music Room','Swimming Pool','Table Tennis','Tapal Cafeteria','W-024','W-002','W-003','Washroom 1','Washroom 2','Washroom 3']

def selected():
        # Label(root, text ="From: "+ clicked.get()).pack()
        # Label(root, text ="To: "+ clicked2.get()).pack()
        start = clicked.get()
        end = clicked2.get()
        path=getShortestPath(G, start,end)
        Label(root, text= "").pack()
        Label(root,text = ' => '.join(path),font =("Calibri",13), bg="#72098f", fg="white").pack()
        Label(root, text= "").pack()
        destroyButton = Button(root, text ="Show Map",command= root.destroy, bg = "#ba83c9", fg = "white")
        destroyButton.pack()
        
clicked = StringVar(root)
clicked.set(options[0])
clicked2 = StringVar(root)
clicked2.set(options[7])

Label(root, text="").pack()
Label(root, text="").pack()
Label(root, text=" Welcome to Habib University ",font=("Arial", 25), bg="#72098f", fg="white").pack()
Label(root, text="").pack()
Label(root, text="").pack()
drop = OptionMenu(root, clicked, *options)
drop2 = OptionMenu(root, clicked2, *options)
Label(root, text="Where are you?",font=("Arial", 18),height=1, width=35, bg="#FF0099", fg="white").pack()
drop.pack(pady=20)
Label(root, text="Where do you want to go?",font=("Arial", 18),height=1, width=35, bg="#FF0099", fg="white").pack()
drop2.pack(pady=20)
drop.config(width=20, font = ("Arial", 15),bg = "#72098f", fg = "white")
drop2.config(width=20, font = ("Arial", 15),bg = "#72098f", fg = "white")
myButton = Button(root, text ="Search", command = selected, width =20, font = ("Arial", 10), bg = "#ba83c9", fg = "white")
myButton.pack()


root.mainloop()

Start= clicked.get()#dropdown() 
End= clicked2.get()#dropdown() 
path=getShortestPath(G, Start,End)
output(path)