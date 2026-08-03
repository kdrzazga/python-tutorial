from building_application import BuildingApplication
from color_palette import BuildingColorPalette
from illumination_scheme import WindowIlluminationScheme
from linear_algebra import Vector3
from orbit_camera import OrbitCamera
from rendering import LitSurfaceRenderer
from ring_building import RingBuilding


def build_donut_headquarters_scene():
    palette = BuildingColorPalette()
    illumination_scheme = WindowIlluminationScheme(lit_probability=0.42, random_seed=7)
    building = RingBuilding(
        outer_semi_width=30.0,
        outer_semi_depth=7.5,
        wall_depth=3.0,
        upper_floor_count=8,
        upper_floor_height=2.4,
        ground_floor_height=4.4,
        upper_segment_count=64,
        ground_segment_count=32,
        pillar_availability=True,
        pillar_placement_angle=0.9,
        palette=palette,
        illumination_scheme=illumination_scheme)
    camera = OrbitCamera(
        target_point=Vector3(0.0, building.total_height * 0.5, 0.0),
        distance=70.0,
        elevation=0.22)
    renderer = LitSurfaceRenderer(light_direction=Vector3(0.4, 0.85, 0.5))
    return BuildingApplication(building=building, camera=camera, renderer=renderer)


if __name__ == "__main__":
    build_donut_headquarters_scene().run()
