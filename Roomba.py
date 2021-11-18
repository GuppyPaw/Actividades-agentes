# -*- coding: utf-8 -*-

# -- Sheet --

import agentpy as ap
import random as ran

class Roomba(ap.Agent):

    # Variables para cada agente
    def setup(self):
        self.x = 0
        self.y = 0
    
    # Metodo para que se mueva el robot en una direccion random
    def move(self):
        self.x += ran.randint(-1,1)
        self.y += ran.randint(-1,1)

class Room(ap.Model):

    def setup(self):
        # Numero total de tiles
        n_tiles = int(self.p['dirty_tiles'] * (self.p.sizeM) * (self.p.sizeN))

        # Se crean los agentes
        self.agents = ap.AgentList(self, self.p.agents, Roomba)
        self.tiles = ap.AgentList(self, n_tiles)

        # Las tiles se "ensucian"
        self.tiles.condition = 0

        # Numero de movimientos
        self.iterations = 0

        # Se crea el grid
        self.grid = self.agents.grid = ap.Grid(self, [self.p.sizeM * self.p.sizeN] * 2, track_empty=True)

        self.grid.add_agents(self.tiles, random=True, empty=True)
        self.grid.add_agents(self.agents, positions = [(0, 0) for i in range(self.p.agents)])

    def step(self):
        dirty_tiles = self.tiles.select(self.tiles.condition == 0)

        # Por cada roomba se limpia o se mueve cada step
        for roomba in self.agents:
            curr_pos = self.grid.positions[roomba]
            tile = dirty_tiles.select([curr_pos[0],curr_pos[1]])
            if tile.condition == 0:
                tile.condition = 1
            else:
                self.agents.move()
                self.grid.positions[roomba] = (roomba.x, roomba.y)
            self.iterations += 1

        # Si ya se limpiaron todas las tiles se detiene
        if len(dirty_tiles) == 0:
            self.stop()

    def end(self):
        self.report('Percentage of cleaned tiles',(len(self.tiles.select(self.tiles.condition == 1)) * 100) / len(self.tiles))
        self.report('Total moves', self.iterations)
        

parameters = {
    'dirty_tiles': 0.8,
    'sizeM': 25,
    'sizeN': 10,
    'agents': 1,
    'steps': 100
}

model = Room(parameters)
results = model.run()
results.save()
results = ap.DataDict.load('Room')

