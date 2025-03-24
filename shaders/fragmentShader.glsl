#version 330 core

in vec2 frag_texcoord;

uniform sampler2D t_baseTexture;

out vec4 out_color;

void main() {
    vec4 color = texture(t_baseTexture, frag_texcoord);
    out_color = vec4(color);
}