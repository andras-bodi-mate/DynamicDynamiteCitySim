#version 330 core

uniform mat4 camera;

in vec3 in_vertex;
in mat4 in_instanceTransform;
in vec3 in_instanceTranslation;
in vec2 in_texcoord;

out vec2 frag_texcoord;

void main() {
    gl_Position = camera * (in_instanceTransform * vec4(in_vertex, 1.0) + vec4(in_instanceTranslation, 1.0));
    frag_texcoord = in_texcoord;
}   