import mesa

from model import TileWorld, Box, TileAgent, Hole, Wall


def draw(agent):
    if agent is None:
        return
    if isinstance(agent, TileAgent):
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    elif isinstance(agent, Box):
        portrayal = {"Shape": "rect", "w": 0.5, "h": 0.5, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#AA0000", "#5C0DF0"]
        portrayal["stroke_color"] = "#800000"
    elif isinstance(agent, Hole):
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#000000", "#000000"]
        portrayal["stroke_color"] = "#000000"
    elif isinstance(agent, Wall):
        portrayal = {"Shape": "rect", "w": 0.5, "h": 0.5, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#BD8A3E", "#BD8A3E"]
        portrayal["stroke_color"] = "#BD8A3E"
    return portrayal


happy_chart = mesa.visualization.ChartModule([{"Label": "num_holes", "Color": "black"}, 
                                              {"Label": "num_boxes", "Color": "red"},
                                              {"Label": "num_walls", "Color": "Brown"}])


canvas_element = mesa.visualization.CanvasGrid(draw, 20, 20, 500, 500)


model_params = {
    "num_agents": mesa.visualization.Slider("Number of Agents", 1, 1, 20, 1),
    "num_boxes": mesa.visualization.Slider("Number of Boxes", 5, 1, 20, 1),
    "num_holes": mesa.visualization.Slider("Number of Holes", 5, 1, 20, 1),
    "num_walls": mesa.visualization.Slider("Number of Walls", 5, 1, 20, 1),
    "width": 20,
    "height": 20
}



server = mesa.visualization.ModularServer(
    TileWorld,
    [canvas_element, happy_chart],
    "TileWorld",
    model_params
)
