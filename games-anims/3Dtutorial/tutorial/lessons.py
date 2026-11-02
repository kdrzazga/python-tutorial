from OpenGL.GL import *

from lesson1_pixel import Point, PixelScene
from lesson2_line import Line, LineScene
from lesson3_triangle import TriangleScene
from lesson4_trihedron import TrihedronScene
from lesson5_ball import BallScene
from lesson6_picture import FlatPicture, FlatPictureScene
from lesson7_picture_ball import TexturedBallScene
from lesson8_mesh import MeshScene
from lesson9_sea import SeaScene
from lesson10_face import FaceScene
from lesson11_talking_face import Speech, TalkingFaceScene
from lesson12_bald_head import BaldHeadScene
from lesson13_head import HeadScene
from lesson14_sunglasses import SunglassesScene


def point_between(start, end, fraction):
    position = tuple(begin + (finish - begin) * fraction
                     for begin, finish in zip(start.position, end.position))
    color = tuple(begin + (finish - begin) * fraction
                  for begin, finish in zip(start.color, end.color))
    return Point(*position, color)


class Lesson:
    def __init__(self, number, title, snippet_name):
        self.number = number
        self.title = title
        self.snippet_name = snippet_name
        self.steps = []
        self.build_duration = 0.0
        self.camera_tilt = 22.0
        self.elapsed = 0.0

    def restart(self):
        self.elapsed = 0.0

    def update(self, seconds):
        self.elapsed += seconds

    def phase(self, start, duration):
        return min(max((self.elapsed - start) / duration, 0.0), 1.0)

    def is_built(self):
        return self.elapsed >= self.build_duration

    def caption(self):
        current_text = ""
        for start, text in self.steps:
            if self.elapsed >= start:
                current_text = text
        return current_text

    def draw_appearing(self, point, fraction):
        if fraction <= 0.0:
            return
        appearing_point = Point(*point.position, point.color)
        appearing_point.size = point.size * fraction
        appearing_point.draw()

    def draw_growing_line(self, start, end, fraction):
        if fraction <= 0.0:
            return
        Line(start, point_between(start, end, fraction)).draw()

    def draw(self):
        raise NotImplementedError


class PixelLesson(Lesson):
    def __init__(self):
        super().__init__(1, "Put a pixel and change its colour", "lesson1_pixel.py")
        self.steps = [(0.0, "glVertex3f(0, 0, 0) inside GL_POINTS puts one pixel"),
                      (2.0, "glPointSize(12) makes the pixel big enough to see"),
                      (4.0, "glColor3f before the vertex changes its colour")]
        self.build_duration = 4.0
        self.tiny_size = 1.0
        self.visible_size = 12.0
        self.restart()

    def restart(self):
        super().restart()
        self.scene = PixelScene()
        self.scene.pixel.size = self.tiny_size

    def update(self, seconds):
        super().update(seconds)
        growth = self.phase(2.0, 1.5)
        self.scene.pixel.size = self.tiny_size + (self.visible_size - self.tiny_size) * growth
        if self.is_built():
            self.scene.update(seconds)

    def draw(self):
        self.scene.draw()


class LineLesson(Lesson):
    def __init__(self):
        super().__init__(2, "Draw a 3D line between two points", "lesson2_line.py")
        self.steps = [(0.0, "The pixel from lesson 1 travels to point A"),
                      (2.5, "A second Point B appears"),
                      (3.5, "GL_LINES joins two vertices into a line"),
                      (6.0, "Vertex colours blend smoothly along the line")]
        self.build_duration = 5.5
        self.restart()

    def restart(self):
        super().restart()
        self.scene = LineScene()
        self.lesson_one_pixel = Point(0.0, 0.0, 0.0)

    def draw(self):
        if self.is_built():
            self.scene.draw()
            return
        point_a = self.scene.point_a
        point_b = self.scene.point_b
        self.draw_growing_line(point_a, point_b, self.phase(3.5, 2.0))
        point_between(self.lesson_one_pixel, point_a, self.phase(0.5, 2.0)).draw()
        self.draw_appearing(point_b, self.phase(2.5, 0.5))


class TriangleLesson(Lesson):
    def __init__(self):
        super().__init__(3, "Draw a triangle from three lines", "lesson3_triangle.py")
        self.steps = [(0.0, "Start from line AB of lesson 2"),
                      (1.0, "Add a third Point C"),
                      (2.0, "Two more Lines close the outline"),
                      (5.5, "GL_TRIANGLES fills the face between the corners")]
        self.build_duration = 7.5
        self.restart()

    def restart(self):
        super().restart()
        self.triangle = TriangleScene().triangle
        self.face_alpha = self.triangle.fill_alpha

    def update(self, seconds):
        super().update(seconds)
        self.triangle.fill_alpha = self.face_alpha * self.phase(5.5, 2.0)

    def draw(self):
        if self.is_built():
            self.triangle.draw()
            return
        first, second, third = self.triangle.corners
        if self.triangle.fill_alpha > 0.0:
            self.triangle.draw_face()
        self.triangle.edges[0].draw()
        self.draw_growing_line(second, third, self.phase(2.0, 1.5))
        self.draw_growing_line(third, first, self.phase(3.5, 1.5))
        first.draw()
        second.draw()
        self.draw_appearing(third, self.phase(1.0, 0.5))


class TrihedronLesson(Lesson):
    def __init__(self):
        super().__init__(4, "Add a point: the trihedron", "lesson4_trihedron.py")
        self.steps = [(0.0, "Start from the triangle of lesson 3"),
                      (1.0, "A fourth Point D rises above the triangle"),
                      (3.0, "Three Lines join D to every corner"),
                      (5.0, "Three more Triangles close the solid"),
                      (7.5, "4 points, 6 edges, 4 faces: a 3D shape")]
        self.build_duration = 7.0
        self.restart()

    def restart(self):
        super().restart()
        self.trihedron = TrihedronScene().trihedron
        self.side_faces = self.trihedron.faces[1:]
        self.face_alpha = self.side_faces[0].fill_alpha
        base_corners = self.trihedron.base.corners
        base_center = tuple(sum(corner.position[axis] for corner in base_corners) / len(base_corners)
                            for axis in range(3))
        self.base_center = Point(*base_center, self.trihedron.apex.color)

    def update(self, seconds):
        super().update(seconds)
        side_alpha = self.face_alpha * self.phase(5.0, 2.0)
        for face in self.side_faces:
            face.fill_alpha = side_alpha

    def draw(self):
        if self.is_built():
            self.trihedron.draw()
            return
        rising_apex = point_between(self.base_center, self.trihedron.apex, self.phase(1.0, 1.5))
        for face in self.side_faces:
            if face.fill_alpha > 0.0:
                face.draw_face()
        self.trihedron.base.draw()
        for corner in self.trihedron.base.corners:
            self.draw_growing_line(corner, rising_apex, self.phase(3.0, 1.5))
        self.draw_appearing(rising_apex, self.phase(1.0, 0.4))


class BallLesson(Lesson):
    def __init__(self):
        super().__init__(5, "Draw a ball", "lesson5_ball.py")
        self.steps = [(0.0, "A ball starts as Points on circles of latitude"),
                      (3.5, "GL_TRIANGLE_STRIP stitches neighbouring rings"),
                      (6.0, "Without light the ball looks like a flat disc"),
                      (7.5, "glNormal3f and GL_LIGHTING make it look round"),
                      (10.0, "glNewList stores the ball, glCallList redraws it")]
        self.build_duration = 7.5
        self.ring_point_size = 4.0
        self.scene = BallScene()
        self.rings = self.create_rings()
        self.restart()

    def create_rings(self):
        ball = self.scene.ball
        rings = []
        for stack_index in range(ball.stacks + 1):
            ring = []
            for slice_index in range(ball.slices):
                direction = ball.direction(slice_index, stack_index)
                ring_point = Point(*(axis * ball.radius for axis in direction), ball.color)
                ring_point.size = self.ring_point_size
                ring.append(ring_point)
            rings.append(ring)
        return rings

    def draw(self):
        if self.is_built():
            self.scene.draw()
            return
        ball = self.scene.ball
        visible_rings = round(len(self.rings) * self.phase(0.0, 3.0))
        stitched_strips = round(ball.stacks * self.phase(3.5, 2.5))
        glColor3f(*ball.color)
        for stack_index in range(stitched_strips):
            ball.draw_strip(stack_index)
        for ring in self.rings[stitched_strips:visible_rings]:
            for ring_point in ring:
                ring_point.draw()


class PictureLesson(Lesson):
    def __init__(self):
        super().__init__(6, "Show a picture on a flat surface", "lesson6_picture.py")
        self.steps = [(0.0, "Four corner Points mark a flat rectangle"),
                      (1.5, "Four Lines frame it - still no picture"),
                      (3.5, "glTexImage2D uploads KnAshort.png as a texture"),
                      (6.0, "glTexCoord2f pins each picture corner to a vertex")]
        self.build_duration = 5.5
        self.frame_color = (0.85, 0.88, 1.0)
        self.scene = FlatPictureScene()
        self.flat_picture = self.scene.flat_picture
        self.frame_corners = [Point(x, y, z, self.frame_color)
                              for _u, _v, x, y, z in self.flat_picture.corners()]
        self.restart()

    def update(self, seconds):
        super().update(seconds)
        self.flat_picture.opacity = self.phase(3.5, 2.0)

    def draw(self):
        if self.is_built():
            self.scene.draw()
            return
        if self.flat_picture.opacity > 0.0:
            self.flat_picture.draw()
        corner_count = len(self.frame_corners)
        for corner_index, corner in enumerate(self.frame_corners):
            next_corner = self.frame_corners[(corner_index + 1) % corner_count]
            self.draw_growing_line(corner, next_corner, self.phase(1.5, 1.5))
            self.draw_appearing(corner, self.phase(0.3 * corner_index, 0.4))


class PictureBallLesson(Lesson):
    def __init__(self):
        super().__init__(7, "Spread the picture over a ball", "lesson7_picture_ball.py")
        self.steps = [(0.0, "Start from the flat picture of lesson 6"),
                      (1.0, "Cut it into a grid - every vertex gets a glTexCoord2f"),
                      (2.5, "Bend the grid until every vertex sits on the Ball"),
                      (6.0, "Lighting from lesson 5 makes the picture ball round"),
                      (8.5, "TexturedBall = Ball + glTexCoord2f for every vertex")]
        self.build_duration = 6.0
        self.grid_color = (0.85, 0.88, 1.0)
        self.scene = TexturedBallScene()
        self.ball = self.scene.ball
        self.flat_picture = FlatPicture(self.ball.picture, 3.2)
        self.restart()

    def bend(self):
        progress = self.phase(2.5, 3.5)
        return progress * progress * (3.0 - 2.0 * progress)

    def flat_position(self, slice_index, stack_index):
        u = slice_index / self.ball.slices
        v = stack_index / self.ball.stacks
        return ((u - 0.5) * self.flat_picture.width,
                (v - 0.5) * self.flat_picture.height,
                0.0)

    def bent_position(self, slice_index, stack_index, bend):
        flat_position = self.flat_position(slice_index, stack_index)
        direction = self.ball.direction(slice_index, stack_index)
        return tuple(flat + (axis * self.ball.radius - flat) * bend
                     for flat, axis in zip(flat_position, direction))

    def draw_bent_picture(self, bend):
        ball = self.ball
        ball.picture.bind()
        glColor3f(1.0, 1.0, 1.0)
        for stack_index in range(ball.stacks):
            glBegin(GL_TRIANGLE_STRIP)
            for slice_index in range(ball.slices + 1):
                for row_index in (stack_index + 1, stack_index):
                    glTexCoord2f(slice_index / ball.slices, row_index / ball.stacks)
                    glVertex3f(*self.bent_position(slice_index, row_index, bend))
            glEnd()
        ball.picture.unbind()

    def draw_grid(self):
        ball = self.ball
        glDisable(GL_DEPTH_TEST)
        glLineWidth(1.0)
        glColor3f(*self.grid_color)
        glBegin(GL_LINES)
        for slice_index in range(ball.slices + 1):
            glVertex3f(*self.flat_position(slice_index, 0))
            glVertex3f(*self.flat_position(slice_index, ball.stacks))
        for stack_index in range(ball.stacks + 1):
            glVertex3f(*self.flat_position(0, stack_index))
            glVertex3f(*self.flat_position(ball.slices, stack_index))
        glEnd()
        glEnable(GL_DEPTH_TEST)

    def draw(self):
        if self.is_built():
            self.scene.draw()
            return
        bend = self.bend()
        self.draw_bent_picture(bend)
        if self.elapsed >= 1.0 and bend == 0.0:
            self.draw_grid()


class MeshLesson(Lesson):
    def __init__(self):
        super().__init__(8, "A mesh covered in see-through blue", "lesson8_mesh.py")
        self.steps = [(0.0, "MeshSurface: rows of Lines across a grid"),
                      (2.5, "Columns of Lines cross them into a mesh"),
                      (5.5, "Triangle strips cover it in blue at 15% alpha"),
                      (8.0, "GL_BLEND lets the mesh lines show through")]
        self.build_duration = 7.5
        self.scene = MeshScene()
        self.mesh = self.scene.mesh
        self.full_fill_alpha = self.mesh.fill_alpha
        self.restart()

    def update(self, seconds):
        super().update(seconds)
        self.mesh.fill_alpha = self.full_fill_alpha * self.phase(5.5, 2.0)

    def draw(self):
        if self.is_built():
            self.scene.draw()
            return
        positions = self.mesh.grid_positions()
        line_count = self.mesh.divisions + 1
        glLineWidth(1.0)
        self.mesh.draw_rows(positions, range(round(line_count * self.phase(0.0, 2.5))))
        self.mesh.draw_columns(positions, range(round(line_count * self.phase(2.5, 2.5))))
        if self.mesh.fill_alpha > 0.0:
            self.mesh.draw_fill(positions)


class SeaLesson(Lesson):
    def __init__(self):
        super().__init__(9, "Move the MeshSurface like sea waves", "lesson9_sea.py")
        self.steps = [(0.0, "Start from the calm MeshSurface of lesson 8"),
                      (1.0, "SeaSurface overrides height() with a sine Wave"),
                      (2.5, "More Waves in other directions mix together"),
                      (4.0, "Lines removed - only the pure sea waves remain"),
                      (7.0, "fill_color_at(): crests whiter, less see-through"),
                      (10.0, "Every frame time grows, so the Waves travel")]
        self.build_duration = 6.0
        self.wave_start_delay = 1.5
        self.wave_grow_duration = 2.0
        self.scene = SeaScene()
        self.sea = self.scene.sea
        self.full_amplitudes = [wave.amplitude for wave in self.sea.waves]
        self.restart()

    def restart(self):
        super().restart()
        self.sea.time = 0.0

    def update(self, seconds):
        super().update(seconds)
        self.scene.update(seconds)
        for wave_index, wave in enumerate(self.sea.waves):
            wave_start = 1.0 + self.wave_start_delay * wave_index
            growth = self.phase(wave_start, self.wave_grow_duration)
            wave.amplitude = self.full_amplitudes[wave_index] * growth

    def draw(self):
        self.scene.draw()


class FaceLesson(Lesson):
    def __init__(self):
        super().__init__(10, "A face from a 200 x 200 mesh", "lesson10_face.py")
        self.steps = [(0.0, "A flat MeshSurface, now 200 x 200 points"),
                      (1.0, "Oval dome: side points sit lower than the centre"),
                      (3.5, "Negative FaceFeatures sink the eye sockets"),
                      (5.5, "The highest FaceFeatures stick out as the nose"),
                      (7.5, "Lower bumps form the lips, a thin dip parts them"),
                      (9.5, "Soft wide bumps add the cheeks"),
                      (11.0, "A bump below the lips sticks out as the chin"),
                      (14.0, "numpy shapes all points, glDrawElements draws them")]
        self.build_duration = 12.5
        self.camera_tilt = 50.0
        self.feature_grow_duration = 1.5
        self.scene = FaceScene()
        self.face = self.scene.face
        self.full_dome_height = self.face.dome_height
        self.full_feature_heights = {feature: feature.height for feature in self.face.features}
        self.feature_starts = [(self.face.eyes, 3.5), (self.face.nose, 5.5),
                               (self.face.lips, 7.5), (self.face.cheeks, 9.5),
                               (self.face.chin, 11.0)]
        self.is_shaped = False
        self.restart()

    def restart(self):
        super().restart()
        self.is_shaped = False

    def update(self, seconds):
        super().update(seconds)
        if self.is_shaped:
            return
        self.face.dome_height = self.full_dome_height * self.phase(1.0, 2.0)
        for features, start in self.feature_starts:
            growth = self.phase(start, self.feature_grow_duration)
            for feature in features:
                feature.height = self.full_feature_heights[feature] * growth
        self.face.build()
        self.is_shaped = self.is_built()

    def draw(self):
        self.scene.draw()


class TalkingFaceLesson(Lesson):
    def __init__(self):
        super().__init__(11, "Make the face talk", "lesson11_talking_face.py")
        self.camera_tilt = 50.0
        self.tour_start = 2.0
        self.scene = TalkingFaceScene()
        self.face = self.scene.face
        self.lip_shapes = self.scene.lip_shapes
        self.speech = self.scene.speech
        tour_words = [(shape.example, [shape.syllable]) for shape in self.lip_shapes.shapes]
        self.tour = Speech(self.lip_shapes, tour_words)
        self.tour.syllable_duration = 0.35
        self.tour.pause_slots = 1
        self.talk_start = self.tour_start + self.tour.duration
        self.restart()

    def current_pose(self):
        if self.elapsed < self.tour_start:
            return self.lip_shapes.rest.pose
        if self.elapsed < self.talk_start:
            self.tour.time = self.elapsed - self.tour_start
            return self.tour.lip_pose()
        self.speech.time = self.elapsed - self.talk_start
        return self.speech.lip_pose()

    def update(self, seconds):
        super().update(seconds)
        self.face.shape_lips(*self.current_pose())
        self.face.build()

    def caption(self):
        if self.elapsed < self.tour_start:
            return "TalkingFace imports the whole face of lesson 10"
        if self.elapsed < self.talk_start:
            shape_index = self.tour.current_slot()[0]
            shape = self.lip_shapes.shapes[shape_index]
            shape_count = len(self.lip_shapes.shapes)
            return f"LipShape {shape_index + 1}/{shape_count}: '{shape.syllable}' as in {shape.example}"
        return f"Speech - {self.speech.spoken_text()}"

    def draw(self):
        self.scene.draw()


class BaldHeadLesson(Lesson):
    def __init__(self):
        super().__init__(12, "A talking bald head", "lesson12_bald_head.py")
        self.steps = [(0.0, "HeadFront: the talking face, its grid bent into an oval"),
                      (2.5, "BackOfHead: a new MeshSurface on the same oval rim"),
                      (5.0, "It bulges away behind the face: the back of the skull"),
                      (7.5, "One shared rim closes the two meshes into a head")]
        self.camera_tilt = 12.0
        self.back_appear_time = 2.5
        self.back_grow_start = 5.0
        self.back_grow_duration = 2.5
        self.talk_caption_start = 10.0
        self.scene = BaldHeadScene()
        self.head = self.scene.head
        self.speech = self.scene.speech
        self.full_back_depth = self.head.back.back_depth
        self.restart()

    def restart(self):
        super().restart()
        self.speech.time = 0.0

    def update(self, seconds):
        super().update(seconds)
        self.scene.update(seconds)
        back = self.head.back
        self.head.show_back = self.elapsed >= self.back_appear_time
        growth = self.phase(self.back_grow_start, self.back_grow_duration)
        back_depth = self.full_back_depth * growth
        if back_depth != back.back_depth:
            back.back_depth = back_depth
            back.invalidate()

    def caption(self):
        if self.elapsed < self.talk_caption_start:
            return super().caption()
        return f"Speech - {self.speech.spoken_text()}"

    def draw(self):
        self.scene.draw()


class HeadLesson(Lesson):
    def __init__(self):
        super().__init__(13, "A head with eyes, ears and hair", "lesson13_head.py")
        self.steps = [(0.0, "Start from the talking BaldHead of lesson 12"),
                      (1.5, "Eyeball: a white Ball from lesson 5 in each socket"),
                      (4.0, "Vertices near the front pole turn blue: the iris"),
                      (6.5, "A smaller black circle in the middle: the pupil"),
                      (8.0, "Ear: an oval donut rim around a flat Ball bowl"),
                      (10.0, "Each Ear flares out from the side of the skull"),
                      (11.5, "Hair: a bent cylinder narrowing to a thin tip")]
        self.build_duration = 13.5
        self.camera_tilt = 12.0
        self.talk_caption_start = 16.0
        self.eyes_start = 1.5
        self.sink_depth = 0.35
        self.ears_start = 8.0
        self.ear_grow_duration = 1.5
        self.hair_start = 11.5
        self.hair_grow_duration = 2.0
        self.scene = HeadScene()
        self.head = self.scene.head
        self.speech = self.scene.speech
        hair_count = self.head.haircut.hair_count
        self.title = f"A head with eyes, ears and {hair_count} hair strands"
        self.steps.append((13.5, f"{hair_count} Hairs: forehead top, crown and above the ears"))
        self.full_eye_rise = self.head.eye_rise
        self.full_iris_degrees = self.head.eyeballs[0].iris_degrees
        self.full_pupil_degrees = self.head.eyeballs[0].pupil_degrees
        self.restart()

    def restart(self):
        super().restart()
        self.speech.time = 0.0

    def update(self, seconds):
        super().update(seconds)
        self.scene.update(seconds)
        self.head.show_eyes = self.elapsed >= self.eyes_start
        rise = self.phase(self.eyes_start, 1.5)
        self.head.eye_rise = self.full_eye_rise - self.sink_depth * (1.0 - rise)
        self.head.show_ears = self.elapsed >= self.ears_start
        ear_size = self.phase(self.ears_start, self.ear_grow_duration)
        for ear in self.head.ears:
            ear.size = max(ear_size, 0.01)
        haircut = self.head.haircut
        self.head.show_hair = self.elapsed >= self.hair_start
        hair_share = self.phase(self.hair_start, self.hair_grow_duration)
        haircut.visible_count = round(haircut.hair_count * hair_share)
        iris_degrees = self.full_iris_degrees * self.phase(4.0, 1.5)
        pupil_degrees = self.full_pupil_degrees * self.phase(6.5, 1.0)
        for eyeball in self.head.eyeballs:
            if (eyeball.iris_degrees, eyeball.pupil_degrees) != (iris_degrees, pupil_degrees):
                eyeball.iris_degrees = iris_degrees
                eyeball.pupil_degrees = pupil_degrees
                eyeball.invalidate()

    def caption(self):
        if self.elapsed < self.talk_caption_start:
            return super().caption()
        return f"Speech - {self.speech.spoken_text()}"

    def draw(self):
        self.scene.draw()


class SunglassesLesson(Lesson):
    def __init__(self):
        super().__init__(14, "Put sunglasses on the head", "lesson14_sunglasses.py")
        self.steps = [(0.0, "Start from the Head of lesson 13"),
                      (1.0, "Sunglasses move in and sit on the nose"),
                      (3.5, "FrameRim: a thick green bar around each Lens"),
                      (5.5, "Lens: a rounded black rectangle with a shine"),
                      (7.5, "CurvedBar: a bridge over the nose, flat arms to ears")]
        self.camera_tilt = 12.0
        self.talk_caption_start = 10.0
        self.glasses_start = 1.0
        self.glasses_travel = 2.0
        self.start_lift = 1.5
        self.scene = SunglassesScene()
        self.head = self.scene.head
        self.speech = self.scene.speech
        self.restart()

    def restart(self):
        super().restart()
        self.speech.time = 0.0

    def update(self, seconds):
        super().update(seconds)
        self.scene.update(seconds)
        arrival = self.phase(self.glasses_start, self.glasses_travel)
        smooth_arrival = arrival * arrival * (3.0 - 2.0 * arrival)
        self.head.show_sunglasses = self.elapsed >= self.glasses_start
        self.head.sunglasses.lift = self.start_lift * (1.0 - smooth_arrival)

    def caption(self):
        if self.elapsed < self.talk_caption_start:
            return super().caption()
        return f"Speech - {self.speech.spoken_text()}"

    def draw(self):
        self.scene.draw()
