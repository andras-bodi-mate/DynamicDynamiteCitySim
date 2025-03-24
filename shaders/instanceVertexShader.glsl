#version 330 core

uniform mat4 u_projection;
uniform mat4 u_view;

in vec3 in_vertex;
in mat4 in_instanceTransform;
in vec3 in_instanceTranslation;
in vec2 in_texcoord;

out vec2 frag_texcoord;

void main() {
    gl_Position = (u_projection * u_view) * (in_instanceTransform * vec4(in_vertex, 1.0) + vec4(in_instanceTranslation, 1.0));
    frag_texcoord = in_texcoord;
}   