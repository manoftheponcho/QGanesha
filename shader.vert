#version 130
in vec3 vertex;
in vec4 texCoord;
out vec4 texc;
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex.x, -vertex.y, vertex.z, 1.0);
    texc = texCoord;
}
