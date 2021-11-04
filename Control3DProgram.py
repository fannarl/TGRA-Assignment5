try:
    from OpenGL.GL import *
    from glfw.GLFW import *
    
    from glfw import _GLFWwindow as GLFWwindow

    import PIL
    
    import glm

    import assimp_py

except ImportError:
    import requirements

    from OpenGL.GL import *
    from glfw.GLFW import *
    
    from glfw import _GLFWwindow as GLFWwindow

    import PIL
    
    import glm

    import assimp_py


from shader_m import Shader
from camera import Camera, Camera_Movement
from model import Model
from bezier import Curve

import platform, ctypes, os

MODEL_RESOURCE_PATH = "C:/Users/fanna/OneDrive/Documents/Skóli/Forritun/Tolvugrafik/Assignment05/TGRA-Assignment5"

SCR_WIDTH = 800
SCR_HEIGHT = 600

camera = Camera(glm.vec3(0.0, 0.0, 3.0))
lastX = SCR_WIDTH / 2.0
lastY = SCR_HEIGHT / 2.0
firstMouse = True

deltaTime = 0.0
lastFrame = 0.0

lightPos = glm.vec3(0.0, 0.1, 0.0)

def main() -> int:
    global deltaTime, lastFrame

    glfwInit()
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    if (platform.system() == "Darwin"):
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    if (window == None):

        print("Failed to create GLFW window")
        glfwTerminate()
        return -1

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)
    glfwSetCursorPosCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)

    ourShader = Shader(
        os.path.join(MODEL_RESOURCE_PATH, "3DModel.vs"),
        os.path.join(MODEL_RESOURCE_PATH, "3DModel.fs")
    )
    lightCubeShader = Shader("test_cube.vs", "test_cube.fs")

    ourModel = Model(os.path.join(MODEL_RESOURCE_PATH, "resources/viking_room.obj"))

    path = [
        (glm.vec3(0, 0, 0), glm.vec3(3, 2, 0)),
        (glm.vec3(5, 0, 5), glm.vec3(-1, -1, 0)),
        (glm.vec3(3, 0, 3), glm.vec3(0, 0, -4)),
        (glm.vec3(5, 0.5, 3), glm.vec3(0, 0, 4))
    ]

    curve = Curve(path)

    curve.setBuffer()

    t = 0
    vertices = glm.array(glm.float32,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,

        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,

         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0
    )

    pointLightPositions = [
        glm.vec3( 0.0,  0.2,  0.25),
        glm.vec3( 1.25, 1.3, -0.45),
        glm.vec3( -1.1,  1.3, -0.45),
        glm.vec3( 0.35,  0.6, -0.5),
        glm.vec3( -0.3,  0.6, -0.5)
    ]

    cubeVAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

    glBindVertexArray(cubeVAO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(6 * glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(2)

    lightCubeVAO = glGenVertexArrays(1)
    glBindVertexArray(lightCubeVAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    while (not glfwWindowShouldClose(window)):
        currentFrame = glfwGetTime()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        curvemodel = glm.mat4(1.0)
        curvemodel = glm.translate(curvemodel, glm.vec3(5.0, 1.0, 5.0))
        curvemodel = glm.scale(curvemodel, glm.vec3(1.0, 1.0, 1.0))
        curvemodel = glm.rotate(curvemodel, glm.radians(180), glm.vec3(0.0, 1.0, 0.0))

        camera.Position = curve.getPoint(t)
        camera.Position = glm.vec3(curvemodel * glm.vec4(camera.Position, 1.0))

        processInput(window)

        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ourShader.use()
        ourShader.setVec3("viewPos", camera.Position)

        ourShader.setVec3("lights[0].position", pointLightPositions[0])
        ourShader.setVec3("lights[0].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[0].diffuse", 0.4, 0.4, 0.4)
        ourShader.setVec3("lights[0].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[0].constant", 1.0)
        ourShader.setFloat("lights[0].linear", 0.09)
        ourShader.setFloat("lights[0].quadratic", 0.032)

        ourShader.setVec3("lights[1].position", pointLightPositions[1])
        ourShader.setVec3("lights[1].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[1].diffuse", 0.3, 0.3, 0.3)
        ourShader.setVec3("lights[1].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[1].constant", 1.0)
        ourShader.setFloat("lights[1].linear", 0.09)
        ourShader.setFloat("lights[1].quadratic", 0.032)

        ourShader.setVec3("lights[2].position", pointLightPositions[2])
        ourShader.setVec3("lights[2].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[2].diffuse", 0.3, 0.3, 0.3)
        ourShader.setVec3("lights[2].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[2].constant", 1.0)
        ourShader.setFloat("lights[2].linear", 0.09)
        ourShader.setFloat("lights[2].quadratic", 0.032)

        ourShader.setVec3("lights[3].position", pointLightPositions[3])
        ourShader.setVec3("lights[3].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[3].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[3].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[3].constant", 1.0)
        ourShader.setFloat("lights[3].linear", 0.09)
        ourShader.setFloat("lights[3].quadratic", 0.032)

        ourShader.setVec3("lights[3].position", pointLightPositions[4])
        ourShader.setVec3("lights[3].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[3].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[3].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[3].constant", 1.0)
        ourShader.setFloat("lights[3].linear", 0.09)
        ourShader.setFloat("lights[3].quadratic", 0.032)


        projection = glm.perspective(glm.radians(camera.Zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
        view = camera.GetViewMatrix()
        ourShader.setMat4("projection", projection)
        ourShader.setMat4("view", view)

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(1.0, 1.0, 1.0))
        ourShader.setMat4("model", model)
        ourModel.Draw(ourShader)

        lightCubeShader.use()
        lightCubeShader.setMat4("projection", projection)
        lightCubeShader.setMat4("view", view)

        glBindVertexArray(lightCubeVAO)
        #--------------remove comments to see the location of lights-------------------#
        # for i in range(5):
        #     model = glm.mat4(1.0)
        #     model = glm.translate(model, pointLightPositions[i])
        #     model = glm.scale(model, glm.vec3(0.2)) # Make it a smaller cube
        #     lightCubeShader.setMat4("model", model)
        #     glDrawArrays(GL_TRIANGLES, 0, 36)
        #------------------------------------------------------------------------------#

        ourShader.setMat4("model", curvemodel)
        curve.draw()

        glfwSwapBuffers(window)
        glfwPollEvents()

        t += 0.1 * deltaTime

    glfwTerminate()
    return 0

def processInput(window: GLFWwindow) -> None:

    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS):
        glfwSetWindowShouldClose(window, True)

    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.BACKWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.LEFT, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.RIGHT, deltaTime)

def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:
    glViewport(0, 0, width, height)

def mouse_callback(window: GLFWwindow, xpos: float, ypos: float) -> None:
    global lastX, lastY, firstMouse
    
    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(xoffset, yoffset)

def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:

    camera.ProcessMouseScroll(yoffset)


main()
