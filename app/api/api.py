from fastapi import APIRouter
import socket
from utils.k8s import get_config_map

router = APIRouter(prefix='/api')

# Hostname endpoint
@router.get("/hostname")
async def get_hostname():
    hostname = socket.gethostname()
    config_map_message = get_config_map()
    return {"hostname": hostname, "config_map_message": config_map_message}
