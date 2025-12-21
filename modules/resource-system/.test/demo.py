from _hydrogenlib_resource_system import *
from pathlib import Path


class ResourceSystem(HRS.ResourceSystemBase):
    class Resources(HRS.Resources):
        textures = RMount("zip://icons.gz")
        usercache = Mount("osfs://usercache/")
        icons = RMount("zip://icons.gz")
        ram_cache = Mount("mem://")
        temp = Mount("temp://")


rs = ResourceSystem(Path(__file__).parent, 'xxxx', 'xxxx')
rs.auto_mount()
