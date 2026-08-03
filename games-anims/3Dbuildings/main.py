from building_application import BuildingApplication
from building.building_builder import BuildingBuilder
from linear_algebra import Vector3
from orbit_camera import OrbitCamera
from rendering import LitSurfaceRenderer
from scene import Scene


if __name__ == "__main__":
    building = BuildingBuilder().with_pillar(0.9).with_logo(segment_x=2, segment_y=2).build()
    camera = OrbitCamera(
        target_point=Vector3(0.0, building.total_height * 0.5, 0.0),
        distance=70.0,
        elevation=0.22)
    renderer = LitSurfaceRenderer(light_direction=Vector3(0.4, 0.85, 0.5))
    scene = Scene(building, camera, renderer)
    BuildingApplication(scene).run()
