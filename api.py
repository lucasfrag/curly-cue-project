from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from projects.clump_stylizer.curly_pipeline import generate_strands
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta a pasta 'output' como estática (para acessar strands.obj/mtl)
output_dir = os.path.join(os.path.dirname(__file__), "output")
app.mount("/output", StaticFiles(directory=output_dir), name="output")

# Monta a pasta 'data' como estática (para acessar scalpPath direto via URL)
data_dir = os.path.join(os.path.dirname(__file__), "data")
app.mount("/data", StaticFiles(directory=data_dir), name="data")


# Modelo para requisição
class HairRequest(BaseModel):
    guidePath: str
    scalpPath: str
    groupingCSV: str
    outputPath: str
    curliness: float
    length: float
    density: float
    color: str


@app.post("/generate")
async def generate_hair(params: HairRequest):
    strands = generate_strands(
        guide_path=params.guidePath,
        scalp_path=params.scalpPath,
        grouping_csv=params.groupingCSV,
        output_path=params.outputPath,
        curliness=params.curliness,
        length=params.length,
        density=params.density,
        color=params.color
    )
    return {"strands": strands}
