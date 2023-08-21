
import mesa
from pathfinding import a_star

class TileAgent(mesa.Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.beliefs = {"agents": [], "boxes": [], "holes": [], "walls": []}
        self.desires = {"target": Box, "objects": []}
        self.intentions = {"box_to_move": None, "destination": None, "path": []}
        self.able_to_push = False

    def set_destination(self):
        min_distance = 1000
        for goal_object in self.desires["objects"]:
            if self.desires["target"] == Box:
                x, y = self.pos
                xBox, yBox = goal_object.__getattribute__("pos") 
                distance = abs(x - xBox) + abs(y - yBox)
            else:
                x, y = self.intentions["box_to_move"].__getattribute__("pos")
                xHole, yHole = goal_object.__getattribute__("pos") 
                distance = abs(x - xHole) + abs(y - yHole)
            if distance < min_distance:
                self.intentions["destination"] = goal_object 
                min_distance = distance
        
                    
    def brf(self):
        boxes = []
        agents = []
        holes = []
        walls = []
        for cell_content, position in self.model.grid.coord_iter():
            if isinstance(cell_content, TileAgent):
                agents.append(cell_content)
            elif isinstance(cell_content,  Box):
                boxes.append(cell_content)
            elif isinstance(cell_content,  Hole):
                holes.append(cell_content)
            elif isinstance(cell_content, Wall):
                walls.append(cell_content)
        self.beliefs["agents"] = agents
        self.beliefs["boxes"] = boxes
        self.beliefs["holes"] = holes
        self.beliefs["walls"] = walls
    
    def filter_desires(self):
        filtered_beliefs = []
        for box in self.desires["objects"]:
            if box not in self.beliefs["walls"]:
                filtered_beliefs.append(box)
        self.desires["objects"] = filtered_beliefs

    def options(self):
        if self.intentions["destination"] is None:
            self.desires["target"] = Box
            self.desires["objects"] = self.beliefs["boxes"]
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=False, include_center=False):
            if (isinstance(self.intentions["destination"], Box))  and isinstance(neighbor, Box):
                self.desires["target"] = Hole
                self.desires["objects"] = self.beliefs["holes"]
                break

    def filter(self):
        self.filter_desires()
        self.set_destination()
        if self.desires["target"] == Box:
            self.intentions["box_to_move"] = self.intentions["destination"]
        
        print(self.intentions["destination"])
        print(self.intentions["box_to_move"])
        self.calculate_path()

    def calculate_path(self):
        xBox, yBox = self.intentions["box_to_move"].__getattribute__("pos")
        xDestination, yDestination = self.intentions["destination"].__getattribute__("pos")
        if self.desires["target"] == Box:
            self.intentions["path"] = a_star(self.model.grid, self.pos, (xDestination, yDestination))
        else: 
            path_box_hole = a_star(self.model.grid, (xBox, yBox), (xDestination, yDestination))
            next_step = path_box_hole[0]
            is_aligned_in_x = self.pos[0] == next_step[0]
            is_in_order_in_y = next_step[1] > yBox > self.pos[1] or next_step[1] < yBox < self.pos[1]
            is_aligned_in_y = self.pos[1] == next_step[1]
            is_in_order_in_x = next_step[0] > xBox > self.pos[0] or next_step[0] < xBox < self.pos[0]
            if (is_aligned_in_x and is_in_order_in_y) or (is_aligned_in_y and is_in_order_in_x):
                self.able_to_push = True 
                self.intentions["path"] = path_box_hole 
            else:
                # if next_step[0] < xBox:
                #     self.intentions["path"] = a_star(self.model.grid, self.pos, (next_step[0]+2, next_step[1]))
                # elif next_step[0] > xBox: 
                #     self.intentions["path"] = a_star(self.model.grid, self.pos, (next_step[0]-2, next_step[1]))
                # elif next_step[1] < yBox: 
                #     self.intentions["path"] = a_star(self.model.grid, self.pos, (next_step[0], next_step[1]+2))
                # elif next_step[1] > yBox:
                #     self.intentions["path"] = a_star(self.model.grid, self.pos, (next_step[0], next_step[1]-2))
                # else:
                #     print("no se ni que rollo")
                # print(f"next step: {next_step}")
                for cell in self.model.grid.get_neighborhood((xBox, yBox), moore=False, include_center=False):
                    if self.model.grid.is_cell_empty(cell) and (next_step[0] == cell[0]-2 or next_step[0] == cell[0]+2 or next_step[1] == cell[1]-2 or next_step[1] == cell[1]+2):
                        self.intentions["path"] = a_star(self.model.grid, self.pos, cell)
                        break
                    else:
                        print("no puedo irme ahi")
                self.able_to_push = False
    
    def reset(self, object):
        self.model.grid.remove_agent(self.intentions[object])
        self.model.grid.remove_agent(self.intentions[object])
        self.intentions[object] = None


    def push_box(self):
        if len(self.intentions["path"]) == 1:
            self.reset("destination")
            self.reset("box_to_move")
            self.model.num_boxes -= 1
            self.model.num_holes -= 1
            self.able_to_push = False
        else:
            self.model.grid.move_agent(self.intentions["box_to_move"], self.intentions["path"][0])
    
    def action(self):
        self.brf()
        self.options()
        self.filter()
    
    def move(self):
        if self.able_to_push:
            new_position = self.intentions["box_to_move"].__getattribute__("pos")
            self.push_box()
        else:
            new_position = self.intentions["path"][0]
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)
        else:
            self.beliefs["walls"].append(self.intentions["destination"])

    def step(self):
        self.action()
        self.move() 


class Box(mesa.Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class Hole(mesa.Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class Wall(mesa.Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class TileWorld(mesa.Model):

    def __init__(self, width, height, num_agents, num_boxes, num_holes, num_walls):
        super().__init__()
        self.num_agents = num_agents
        self.num_boxes = num_boxes
        self.num_holes = num_holes
        self.num_walls = num_walls
        self.grid = mesa.space.SingleGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.datacollector = mesa.DataCollector(
            model_reporters={"num_holes": "num_holes", 
                             "num_boxes": "num_boxes",
                             "num_agents": "num_agents",
                             "num_walls": "num_walls"}, 
            # agent_reporters={"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )
        self.put_agents()
        
    def put_agents(self):
        self.place_agents_randomly(TileAgent, self.num_agents)
        self.place_agents_randomly(Box, self.num_boxes)
        self.place_agents_randomly(Hole, self.num_holes)
        self.place_agents_randomly(Wall, self.num_walls)

    def place_agents_randomly(self, Type, num):
        c = 0
        for cell in self.grid.coord_iter():
            if (c == num): break
            x, y = cell[1]
            id = self.next_id()
            agent = Type(id, self, (x, y)) 
            self.grid.move_to_empty(agent)
            self.schedule.add(agent)
            c += 1

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self) 
        self.running = self.num_holes != 0
        self.datacollector.collect(self)
        if self.schedule.steps == 100:
            self.running = False

