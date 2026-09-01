# Night Picture

A procedurally drawn moonlit night scene rendered with OpenGL (PyOpenGL + pygame).
Everything is math: the moon is a circle, cloud silhouettes are sums of sines, the tree
is a recursive branch system, the crown is a sine-perturbed polar curve, and the flower
petals are parametric leaf shapes. All gradients and shading come from per-vertex color
interpolation plus additive glow blending.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Press `Esc` or close the window to quit. The window is 1280x720.

## Building the scene

The picture is composed with a fluent builder (`builder.py`). Coordinates are
top-left (the origin is the top-left corner, y grows downward); the builder
converts them to the OpenGL frame internally.

```python
from builder import NightPicBuilder

(
    NightPicBuilder(width=1280, height=720)
    .with_sky()
    .with_stars(count=150)
    .with_moon(radius=150, center_x=340, center_y=250)
    .with_moon_blaze()
    .with_moon_shade(size=200)
    .with_clouds(count=4)
    .with_water()
    .with_ground()
    .with_trees(count=1)
    .with_flowers(count=10)
    .with_fireflies(count=30)
    .with_vignette()
    .run()
)
```

Every `with_*` returns the builder, so calls chain. Only the layers you add are
drawn (`NightPicBuilder.default().run()` adds them all). `with_moon_blaze` adds
the halo around the moon, `with_moon_shade` casts the moon's reflection onto the
water, and `with_trees` drops trees at random positions along the ground line.
`build()` returns a `Scene`; `run()` builds it and opens the window.

## Structure

Each visual element is its own class.

| Layer | Class | File |
|-------|-------|------|
| Sky gradient | `Sky` | `elements/sky.py` |
| Stars | `Star`, `StarField` | `elements/star.py` |
| Moon disc, halo, maria, rim | `Moon` | `elements/moon.py` |
| Moon reflection on water | `MoonShade` | `elements/moon_shade.py` |
| Sinusoidal clouds | `Cloud`, `CloudBank` | `elements/cloud.py` |
| Sea surface + ripples | `Water` | `elements/water.py` |
| Cliff | `Soil` | `elements/soil.py` |
| Foliage mass | `Crown` | `elements/tree.py` |
| Recursive branches | `Tree`, `Segment` | `elements/tree.py` |
| Hanging light strands | `LightStrand`, `Vines` | `elements/vine.py` |
| Glowing flowers | `Petal`, `Flower`, `Garden` | `elements/flower.py` |
| Fireflies | `Firefly`, `Swarm` | `elements/firefly.py` |
| Corner darkening | `Vignette` | `elements/sky.py` |

`NightPicBuilder` (`builder.py`) assembles the elements back-to-front into a
`Scene`. `Painter` (`painter.py`) is the drawing layer: it owns every OpenGL
immediate-mode primitive (gradient rects, radial glows, rings, fans, tapered
segments, column strips). `Scene` (`scene.py`) holds the element list and renders
it. `App` (`app.py`) owns the window, the projection, and the render loop. Colors
live in `palette.py`; the ground line lives in `terrain.py`.
