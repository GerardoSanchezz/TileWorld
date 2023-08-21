import mesa
import pandas as pd

from model import TileWorld, Box, TileAgent, Hole, Wall

model_params_run = {
    "num_agents": [1],
    "num_boxes": [4, 8],
    "num_holes": [10, 12],
    "num_walls": [1],
    "width": 20,
    "height": 20
}

results = mesa.batch_run(
    TileWorld,
    parameters=model_params_run,
    iterations=1,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)