from builder import NightPicBuilder
from show import SceneShow


def build_scenes():
    moon_left = (
        NightPicBuilder(1280, 720, seed=7)
        .with_sky()
        .with_stars(count=150)
        .with_moon(radius=150, center_x=340, center_y=250)
        .with_moon_blaze()
        .with_moon_shade(size=200)
        .with_clouds(count=4)
        .with_water()
        .with_ground()
        .with_trees(count=1)
        .with_flowers(count=12)
        .with_fireflies(count=30)
        .with_vignette()
        .build()
    )

    moon_right = (
        NightPicBuilder(1280, 720, seed=13)
        .with_sky()
        .with_stars(count=160)
        .with_moon(radius=140, center_x=980, center_y=240)
        .with_moon_blaze()
        .with_clouds(count=5)
        .with_water()
        .with_ground()
        .with_trees(count=1)
        .with_flowers(count=12)
        .with_fireflies(count=30)
        .with_vignette()
        .build()
    )

    small_moon = (
        NightPicBuilder(1280, 720, seed=21)
        .with_sky()
        .with_stars(count=220)
        .with_moon(radius=70, center_x=430, center_y=190)
        .with_moon_blaze(intensity=0.8)
        .with_moon_shade(size=120)
        .with_clouds(count=3)
        .with_water()
        .with_ground()
        .with_trees(count=2)
        .with_flowers(count=8)
        .with_fireflies(count=24)
        .with_vignette()
        .build()
    )

    grove_no_flowers = (
        NightPicBuilder(1280, 720, seed=42)
        .with_sky()
        .with_stars(count=150)
        .with_moon(radius=150, center_x=300, center_y=250)
        .with_moon_blaze()
        .with_moon_shade(size=200)
        .with_clouds(count=4)
        .with_water()
        .with_ground()
        .with_trees(count=5)
        .with_fireflies(count=40)
        .with_vignette()
        .build()
    )

    meadow_no_tree = (
        NightPicBuilder(1280, 720, seed=99)
        .with_sky()
        .with_stars(count=130)
        .with_moon(radius=175, center_x=640, center_y=250)
        .with_moon_blaze(intensity=1.2)
        .with_moon_shade(size=240)
        .with_clouds(count=4)
        .with_water()
        .with_ground()
        .with_flowers(count=40)
        .with_fireflies(count=30)
        .with_vignette()
        .build()
    )

    return (moon_left, moon_right, small_moon, grove_no_flowers, meadow_no_tree)


def main():
    SceneShow(build_scenes(), seconds_per_scene=4.0).run()


if __name__ == "__main__":
    main()
