#version 330 core

in vec4 gl_FragCoord;

uniform vec2 u_resolution;
uniform mat4 u_view;
uniform float u_fov;

out vec4 out_color;

float lerp(float a, float b, float t) {
    return a * (1.0 - t) + b * t;
}

vec3 lerp(vec3 a, vec3 b, float t) {
    return a * (1.0 - t) + b * t; 
}

const vec3 colorA = vec3(0.46, 0.6, 0.82);
const vec3 colorB = vec3(0.0, 0.16, 0.455);
const vec3 colorC = vec3(0.3, 0.3, 0.3);

void main() {
    vec2 screenPos = vec2(
        (gl_FragCoord.x / u_resolution.x) * 2.0 - 1.0,
        (gl_FragCoord.y / u_resolution.y - 1.0) * 2.0 + 1.0
    );

    float h = tan(radians(u_fov/2.0));
    float w = h * u_resolution.x / u_resolution.y;

    vec4 pos = vec4(screenPos.x * w, -screenPos.y * h, 1.0, 1.0) * u_view;
    float angleToHorizon = -atan(pos.y / length(pos.xz)) / 1.570;
    
    float v = pow((1 / (abs(angleToHorizon) + 1)), 5);

    vec3 color = (angleToHorizon > 0.0) ? lerp(colorB, colorA, v) : lerp(colorC, colorA, pow(v, 5));
    out_color = vec4(color, 1.0);
}