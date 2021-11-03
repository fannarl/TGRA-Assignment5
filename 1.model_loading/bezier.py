from OpenGL.GL import * 

import glm


class Curve:
    
    def __init__(self):
        self.points = []
        self.vertices = []

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

    def addPoint(self, anchor : glm.vec3(), control : glm.vec3()):
        self.points.append((anchor, control))

        if len(self.points) < 2: return

        i = len(self.points) - 2

        p0 = self.points[i][0]
        p1 = self.points[i][0] + self.points[i][1]
        p2 = anchor - control
        p3 = anchor

        t = 0.0
        while t < 1.0:
            t1 = 1 - t
            b =  (t1 ** 3) * p0 
            b += (3 * t * (t1 ** 2)) * p1
            b += (3 * t1 * (t ** 2)) * p2
            b += (t ** 3) * p3

            self.vertices.append(b)
            t += 0.05

    def setBuffer(self):
        vertices = glm.array(self.vertices)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)

        # note that this is allowed, the call to glVertexAttribPointer registered VBO as the vertex attribute's bound vertex buffer object so afterwards we can safely unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0) 

        # You can unbind the VAO afterwards so other VAO calls won't accidentally modify this VAO, but this rarely happens. Modifying other
        # VAOs requires a call to glBindVertexArray anyways so we generally don't unbind VAOs (nor VBOs) when it's not directly necessary.
        glBindVertexArray(0) 

    def draw(self, drawPoints : bool = True):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_LINE_STRIP, 0, len(self.vertices))
        glBindVertexArray(0)

    def getPoint(self, t):
        if len(self.points) < 2: return

        i = int(t - t % 1)
        i = i % (len(self.points) - 1)
        t = t % 1

        p0 = self.points[i][0]
        p1 = self.points[i][0] + self.points[i][1]
        p2 = self.points[i+1][0] - self.points[i+1][1]
        p3 = self.points[i+1][0]

        t1 = 1 - t
        b =  (t1 ** 3) * p0 
        b += (3 * t * (t1 ** 2)) * p1
        b += (3 * t1 * (t ** 2)) * p2
        b += (t ** 3) * p3

        return b