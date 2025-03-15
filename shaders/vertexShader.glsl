#version 330 core

uniform mat4 camera;

in vec3 in_vertex;
in vec2 in_texcoord;

out vec2 frag_texcoord;

void main() {
    gl_Position = camera * vec4(in_vertex, 1.0);
    frag_texcoord = in_texcoord;
}   