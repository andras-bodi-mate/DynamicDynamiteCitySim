#version 330 core

in vec2 in_vertex;

void main() {
    gl_Position = vec4(in_vertex, 0.9999, 1.0);
}