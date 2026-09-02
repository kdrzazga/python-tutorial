import ctypes
import math
import os

import glfw
import numpy
from OpenGL.GL import *
from pygltflib import GLTF2


VERTEX_SHADER_SOURCE = """
#version 330 core
layout(location = 0) in vec3 vertex_position;
layout(location = 1) in vec3 vertex_normal;
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;
out vec3 world_space_normal;
void main()
{
    world_space_normal = mat3(model_matrix) * vertex_normal;
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
in vec3 world_space_normal;
uniform vec4 base_color_factor;
out vec4 output_fragment_color;
void main()
{
    vec3 normalized_surface_normal = normalize(world_space_normal);
    vec3 incoming_light_direction = normalize(vec3(0.4, 0.8, 0.6));
    float diffuse_intensity = max(dot(normalized_surface_normal, incoming_light_direction), 0.0);
    float ambient_intensity = 0.25;
    float combined_light_intensity = ambient_intensity + diffuse_intensity * 0.75;
    output_fragment_color = vec4(base_color_factor.rgb * combined_light_intensity, base_color_factor.a);
}
"""

GLTF_COMPONENT_TYPE_TO_NUMPY_DTYPE = {
    5120: numpy.int8,
    5121: numpy.uint8,
    5122: numpy.int16,
    5123: numpy.uint16,
    5125: numpy.uint32,
    5126: numpy.float32,
}

GLTF_ACCESSOR_TYPE_TO_COMPONENT_COUNT = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
    "MAT2": 4,
    "MAT3": 9,
    "MAT4": 16,
}


class MatrixBuilder:
    @staticmethod
    def create_translation_matrix(translation_x, translation_y, translation_z):
        matrix = numpy.identity(4, dtype=numpy.float32)
        matrix[0][3] = translation_x
        matrix[1][3] = translation_y
        matrix[2][3] = translation_z
        return matrix

    @staticmethod
    def create_uniform_scale_matrix(scale_factor):
        matrix = numpy.identity(4, dtype=numpy.float32)
        matrix[0][0] = scale_factor
        matrix[1][1] = scale_factor
        matrix[2][2] = scale_factor
        return matrix

    @staticmethod
    def create_rotation_matrix_around_y_axis(angle_in_radians):
        cosine_of_angle = math.cos(angle_in_radians)
        sine_of_angle = math.sin(angle_in_radians)
        matrix = numpy.identity(4, dtype=numpy.float32)
        matrix[0][0] = cosine_of_angle
        matrix[0][2] = sine_of_angle
        matrix[2][0] = -sine_of_angle
        matrix[2][2] = cosine_of_angle
        return matrix

    @staticmethod
    def create_perspective_projection_matrix(field_of_view_in_radians, aspect_ratio, near_plane_distance, far_plane_distance):
        focal_length = 1.0 / math.tan(field_of_view_in_radians / 2.0)
        matrix = numpy.zeros((4, 4), dtype=numpy.float32)
        matrix[0][0] = focal_length / aspect_ratio
        matrix[1][1] = focal_length
        matrix[2][2] = (far_plane_distance + near_plane_distance) / (near_plane_distance - far_plane_distance)
        matrix[2][3] = (2.0 * far_plane_distance * near_plane_distance) / (near_plane_distance - far_plane_distance)
        matrix[3][2] = -1.0
        return matrix

    @staticmethod
    def create_look_at_view_matrix(camera_position, target_position, world_up_direction):
        forward_direction = target_position - camera_position
        forward_direction = forward_direction / numpy.linalg.norm(forward_direction)
        right_direction = numpy.cross(forward_direction, world_up_direction)
        right_direction = right_direction / numpy.linalg.norm(right_direction)
        corrected_up_direction = numpy.cross(right_direction, forward_direction)
        matrix = numpy.identity(4, dtype=numpy.float32)
        matrix[0][0:3] = right_direction
        matrix[1][0:3] = corrected_up_direction
        matrix[2][0:3] = -forward_direction
        matrix[0][3] = -numpy.dot(right_direction, camera_position)
        matrix[1][3] = -numpy.dot(corrected_up_direction, camera_position)
        matrix[2][3] = numpy.dot(forward_direction, camera_position)
        return matrix


class MeshPrimitiveGeometry:
    def __init__(self, vertex_positions, vertex_normals, triangle_indices, base_color_factor):
        self.vertex_positions = vertex_positions
        self.vertex_normals = vertex_normals
        self.triangle_indices = triangle_indices
        self.base_color_factor = base_color_factor


class GlbModelLoader:
    def __init__(self, glb_file_path):
        self._glb_file_path = glb_file_path
        self._parsed_document = None
        self._binary_buffer = None

    def load_all_mesh_primitives(self):
        self._parsed_document = GLTF2().load(self._glb_file_path)
        self._binary_buffer = self._parsed_document.binary_blob()
        loaded_geometries = []
        for mesh in self._parsed_document.meshes:
            for primitive in mesh.primitives:
                loaded_geometries.append(self._build_geometry_from_primitive(primitive))
        return loaded_geometries

    def _build_geometry_from_primitive(self, primitive):
        vertex_positions = self._read_accessor_as_array(primitive.attributes.POSITION).astype(numpy.float32)
        triangle_indices = self._read_index_array(primitive, vertex_positions.shape[0])
        vertex_normals = self._read_or_generate_normals(primitive, vertex_positions, triangle_indices)
        base_color_factor = self._read_base_color_factor(primitive)
        return MeshPrimitiveGeometry(vertex_positions, vertex_normals, triangle_indices, base_color_factor)

    def _read_index_array(self, primitive, vertex_count):
        if primitive.indices is None:
            return numpy.arange(vertex_count, dtype=numpy.uint32)
        return self._read_accessor_as_array(primitive.indices).reshape(-1).astype(numpy.uint32)

    def _read_or_generate_normals(self, primitive, vertex_positions, triangle_indices):
        if primitive.attributes.NORMAL is not None:
            return self._read_accessor_as_array(primitive.attributes.NORMAL).astype(numpy.float32)
        return self._generate_smooth_normals(vertex_positions, triangle_indices)

    def _generate_smooth_normals(self, vertex_positions, triangle_indices):
        accumulated_normals = numpy.zeros_like(vertex_positions)
        triangle_vertex_index_triples = triangle_indices.reshape(-1, 3)
        for first_vertex_index, second_vertex_index, third_vertex_index in triangle_vertex_index_triples:
            first_edge = vertex_positions[second_vertex_index] - vertex_positions[first_vertex_index]
            second_edge = vertex_positions[third_vertex_index] - vertex_positions[first_vertex_index]
            face_normal = numpy.cross(first_edge, second_edge)
            accumulated_normals[first_vertex_index] += face_normal
            accumulated_normals[second_vertex_index] += face_normal
            accumulated_normals[third_vertex_index] += face_normal
        normal_lengths = numpy.linalg.norm(accumulated_normals, axis=1, keepdims=True)
        normal_lengths[normal_lengths == 0.0] = 1.0
        return (accumulated_normals / normal_lengths).astype(numpy.float32)

    def _read_base_color_factor(self, primitive):
        default_base_color_factor = numpy.array([0.8, 0.8, 0.8, 1.0], dtype=numpy.float32)
        if primitive.material is None:
            return default_base_color_factor
        material = self._parsed_document.materials[primitive.material]
        if material.pbrMetallicRoughness is None or material.pbrMetallicRoughness.baseColorFactor is None:
            return default_base_color_factor
        return numpy.array(material.pbrMetallicRoughness.baseColorFactor, dtype=numpy.float32)

    def _read_accessor_as_array(self, accessor_index):
        accessor = self._parsed_document.accessors[accessor_index]
        buffer_view = self._parsed_document.bufferViews[accessor.bufferView]
        numpy_dtype = numpy.dtype(GLTF_COMPONENT_TYPE_TO_NUMPY_DTYPE[accessor.componentType])
        component_count = GLTF_ACCESSOR_TYPE_TO_COMPONENT_COUNT[accessor.type]
        element_byte_size = numpy_dtype.itemsize * component_count
        starting_byte_offset = (buffer_view.byteOffset or 0) + (accessor.byteOffset or 0)
        byte_stride = buffer_view.byteStride or element_byte_size
        if byte_stride == element_byte_size:
            packed_byte_length = accessor.count * element_byte_size
            packed_bytes = self._binary_buffer[starting_byte_offset:starting_byte_offset + packed_byte_length]
            return numpy.frombuffer(packed_bytes, dtype=numpy_dtype).reshape(accessor.count, component_count)
        element_array = numpy.empty((accessor.count, component_count), dtype=numpy_dtype)
        for element_index in range(accessor.count):
            element_start = starting_byte_offset + element_index * byte_stride
            element_bytes = self._binary_buffer[element_start:element_start + element_byte_size]
            element_array[element_index] = numpy.frombuffer(element_bytes, dtype=numpy_dtype)
        return element_array


class ModelBoundingBoxCalculator:
    @staticmethod
    def compute_center_and_scale_factor(mesh_primitive_geometries, target_largest_dimension):
        combined_positions = numpy.concatenate([geometry.vertex_positions for geometry in mesh_primitive_geometries], axis=0)
        minimum_corner = combined_positions.min(axis=0)
        maximum_corner = combined_positions.max(axis=0)
        bounding_box_center = (minimum_corner + maximum_corner) / 2.0
        largest_dimension = float((maximum_corner - minimum_corner).max())
        scale_factor = target_largest_dimension / largest_dimension if largest_dimension > 0.0 else 1.0
        return bounding_box_center, scale_factor


class ShaderProgram:
    def __init__(self, vertex_shader_source, fragment_shader_source):
        self._program_identifier = self._compile_and_link_program(vertex_shader_source, fragment_shader_source)
        self._uniform_location_cache = {}

    def _compile_and_link_program(self, vertex_shader_source, fragment_shader_source):
        vertex_shader_identifier = self._compile_shader_stage(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader_identifier = self._compile_shader_stage(fragment_shader_source, GL_FRAGMENT_SHADER)
        program_identifier = glCreateProgram()
        glAttachShader(program_identifier, vertex_shader_identifier)
        glAttachShader(program_identifier, fragment_shader_identifier)
        glLinkProgram(program_identifier)
        if glGetProgramiv(program_identifier, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(program_identifier).decode())
        glDeleteShader(vertex_shader_identifier)
        glDeleteShader(fragment_shader_identifier)
        return program_identifier

    def _compile_shader_stage(self, shader_source, shader_stage_type):
        shader_identifier = glCreateShader(shader_stage_type)
        glShaderSource(shader_identifier, shader_source)
        glCompileShader(shader_identifier)
        if glGetShaderiv(shader_identifier, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader_identifier).decode())
        return shader_identifier

    def activate(self):
        glUseProgram(self._program_identifier)

    def _resolve_uniform_location(self, uniform_name):
        if uniform_name not in self._uniform_location_cache:
            self._uniform_location_cache[uniform_name] = glGetUniformLocation(self._program_identifier, uniform_name)
        return self._uniform_location_cache[uniform_name]

    def set_uniform_matrix(self, uniform_name, matrix_values):
        glUniformMatrix4fv(self._resolve_uniform_location(uniform_name), 1, GL_TRUE, matrix_values)

    def set_uniform_vector4(self, uniform_name, vector_values):
        glUniform4fv(self._resolve_uniform_location(uniform_name), 1, vector_values)


class RenderableMeshPrimitive:
    def __init__(self, mesh_primitive_geometry):
        self._base_color_factor = mesh_primitive_geometry.base_color_factor
        self._index_count = int(mesh_primitive_geometry.triangle_indices.size)
        self._vertex_array_object = glGenVertexArrays(1)
        glBindVertexArray(self._vertex_array_object)
        self._position_buffer_object = self._create_float_attribute_buffer(0, mesh_primitive_geometry.vertex_positions)
        self._normal_buffer_object = self._create_float_attribute_buffer(1, mesh_primitive_geometry.vertex_normals)
        self._index_buffer_object = self._create_index_buffer(mesh_primitive_geometry.triangle_indices)
        glBindVertexArray(0)

    def _create_float_attribute_buffer(self, attribute_location, attribute_data):
        buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer_object)
        contiguous_data = numpy.ascontiguousarray(attribute_data, dtype=numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, contiguous_data.nbytes, contiguous_data, GL_STATIC_DRAW)
        components_per_vertex = contiguous_data.shape[1]
        glEnableVertexAttribArray(attribute_location)
        glVertexAttribPointer(attribute_location, components_per_vertex, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        return buffer_object

    def _create_index_buffer(self, triangle_indices):
        buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer_object)
        contiguous_indices = numpy.ascontiguousarray(triangle_indices, dtype=numpy.uint32)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, contiguous_indices.nbytes, contiguous_indices, GL_STATIC_DRAW)
        return buffer_object

    def draw(self, shader_program):
        shader_program.set_uniform_vector4("base_color_factor", self._base_color_factor)
        glBindVertexArray(self._vertex_array_object)
        glDrawElements(GL_TRIANGLES, self._index_count, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)


class ModelViewerApplication:
    def __init__(self, glb_file_path, window_width, window_height, rotation_degrees_per_second):
        self._glb_file_path = glb_file_path
        self._window_width = window_width
        self._window_height = window_height
        self._rotation_degrees_per_second = rotation_degrees_per_second
        self._window_handle = None
        self._shader_program = None
        self._renderable_primitives = []
        self._model_normalization_matrix = None
        self._view_matrix = None
        self._projection_matrix = None
        self._current_rotation_angle_in_radians = 0.0

    def run(self):
        self._initialize_window_and_context()
        self._configure_global_rendering_state()
        self._shader_program = ShaderProgram(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)
        self._load_model_and_create_renderables()
        self._configure_camera_and_projection()
        self._run_render_loop()
        self._shut_down()

    def _initialize_window_and_context(self):
        if not glfw.init():
            raise RuntimeError("GLFW initialization failed")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        self._window_handle = glfw.create_window(self._window_width, self._window_height, "GLB Model Viewer", None, None)
        if not self._window_handle:
            glfw.terminate()
            raise RuntimeError("GLFW window creation failed")
        glfw.make_context_current(self._window_handle)
        glfw.swap_interval(1)

    def _configure_global_rendering_state(self):
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self._window_handle)
        glViewport(0, 0, framebuffer_width, framebuffer_height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.11, 0.12, 0.15, 1.0)

    def _load_model_and_create_renderables(self):
        model_loader = GlbModelLoader(self._glb_file_path)
        mesh_primitive_geometries = model_loader.load_all_mesh_primitives()
        bounding_box_center, scale_factor = ModelBoundingBoxCalculator.compute_center_and_scale_factor(mesh_primitive_geometries, 2.0)
        translation_to_origin = MatrixBuilder.create_translation_matrix(-bounding_box_center[0], -bounding_box_center[1], -bounding_box_center[2])
        uniform_scale = MatrixBuilder.create_uniform_scale_matrix(scale_factor)
        self._model_normalization_matrix = uniform_scale @ translation_to_origin
        for mesh_primitive_geometry in mesh_primitive_geometries:
            self._renderable_primitives.append(RenderableMeshPrimitive(mesh_primitive_geometry))

    def _configure_camera_and_projection(self):
        camera_position = numpy.array([0.0, 1.0, 4.0], dtype=numpy.float32)
        target_position = numpy.array([0.0, 0.0, 0.0], dtype=numpy.float32)
        world_up_direction = numpy.array([0.0, 1.0, 0.0], dtype=numpy.float32)
        self._view_matrix = MatrixBuilder.create_look_at_view_matrix(camera_position, target_position, world_up_direction)
        aspect_ratio = self._window_width / self._window_height
        self._projection_matrix = MatrixBuilder.create_perspective_projection_matrix(math.radians(45.0), aspect_ratio, 0.1, 100.0)

    def _run_render_loop(self):
        previous_frame_time_in_seconds = glfw.get_time()
        while not glfw.window_should_close(self._window_handle):
            current_frame_time_in_seconds = glfw.get_time()
            elapsed_seconds_since_last_frame = current_frame_time_in_seconds - previous_frame_time_in_seconds
            previous_frame_time_in_seconds = current_frame_time_in_seconds
            self._current_rotation_angle_in_radians += elapsed_seconds_since_last_frame * math.radians(self._rotation_degrees_per_second)
            self._render_single_frame()
            glfw.swap_buffers(self._window_handle)
            glfw.poll_events()
            if glfw.get_key(self._window_handle, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self._window_handle, True)

    def _render_single_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._shader_program.activate()
        rotation_matrix = MatrixBuilder.create_rotation_matrix_around_y_axis(self._current_rotation_angle_in_radians)
        model_matrix = rotation_matrix @ self._model_normalization_matrix
        self._shader_program.set_uniform_matrix("model_matrix", model_matrix)
        self._shader_program.set_uniform_matrix("view_matrix", self._view_matrix)
        self._shader_program.set_uniform_matrix("projection_matrix", self._projection_matrix)
        for renderable_primitive in self._renderable_primitives:
            renderable_primitive.draw(self._shader_program)

    def _shut_down(self):
        glfw.terminate()


def main():
    model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.glb")
    application = ModelViewerApplication(model_file_path, 1024, 768, 45.0)
    application.run()


if __name__ == "__main__":
    main()
