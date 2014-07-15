#version 130
in vec3 vertex;
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex.x, -vertex.y, vertex.z, 1.0);
}
