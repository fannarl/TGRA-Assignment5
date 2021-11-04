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

# settings
SCR_WIDTH = 800
SCR_HEIGHT = 600

# camera
camera = Camera(glm.vec3(0.0, 0.0, 3.0))
lastX = SCR_WIDTH / 2.0
lastY = SCR_HEIGHT / 2.0
firstMouse = True

# timing
deltaTime = 0.0
lastFrame = 0.0

# lighting
lightPos = glm.vec3(0.0, 0.1, 0.0)

def main() -> int:
    global deltaTime, lastFrame

    # glfw: initialize and configure
    # ------------------------------
    glfwInit()
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    if (platform.system() == "Darwin"): # APPLE
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    # glfw window creation
    # --------------------
    window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    if (window == None):

        print("Failed to create GLFW window")
        glfwTerminate()
        return -1

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)
    glfwSetCursorPosCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    # tell GLFW to capture our mouse
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    # configure global opengl state
    # -----------------------------
    glEnable(GL_DEPTH_TEST)

    # build and compile shaders
    # -------------------------
    # ourShader = Shader("1.model_loading.vs", "1.model_loading.fs")
    ourShader = Shader(
        os.path.join(MODEL_RESOURCE_PATH, "1.model_loading/1.model_loading.vs"),
        os.path.join(MODEL_RESOURCE_PATH, "1.model_loading/1.model_loading.fs")
    )
    lightCubeShader = Shader("6.light_cube.vs", "6.light_cube.fs")

    # load models
    # -----------
    ourModel = Model(os.path.join(MODEL_RESOURCE_PATH, "resources/viking_room.obj"))
    # draw in wireframe
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
        # positions          # normals           # texture coords
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
    # note that we update the lamp's position attribute's stride to reflect the updated buffer data
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)
    # render loop
    # -----------
    while (not glfwWindowShouldClose(window)):

        # per-frame time logic
        # --------------------
        currentFrame = glfwGetTime()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        curvemodel = glm.mat4(1.0)
        curvemodel = glm.translate(curvemodel, glm.vec3(5.0, 1.0, 5.0))
        curvemodel = glm.scale(curvemodel, glm.vec3(1.0, 1.0, 1.0))
        curvemodel = glm.rotate(curvemodel, glm.radians(180), glm.vec3(0.0, 1.0, 0.0))

        camera.Position = curve.getPoint(t)
        camera.Position = glm.vec3(curvemodel * glm.vec4(camera.Position, 1.0))

        # input
        # -----
        processInput(window)

        # render
        # ------
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # don't forget to enable shader before setting uniforms
        ourShader.use()
        # ourShader.setVec3("light.position", lightPos)
        ourShader.setVec3("viewPos", camera.Position)

        # light properties
        # point light 1
        ourShader.setVec3("lights[0].position", pointLightPositions[0])
        ourShader.setVec3("lights[0].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[0].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[0].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[0].constant", 1.0)
        ourShader.setFloat("lights[0].linear", 0.09)
        ourShader.setFloat("lights[0].quadratic", 0.032)
        # point light 2
        ourShader.setVec3("lights[1].position", pointLightPositions[1])
        ourShader.setVec3("lights[1].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[1].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[1].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[1].constant", 1.0)
        ourShader.setFloat("lights[1].linear", 0.09)
        ourShader.setFloat("lights[1].quadratic", 0.032)
        # point light 3
        ourShader.setVec3("lights[2].position", pointLightPositions[2])
        ourShader.setVec3("lights[2].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[2].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[2].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[2].constant", 1.0)
        ourShader.setFloat("lights[2].linear", 0.09)
        ourShader.setFloat("lights[2].quadratic", 0.032)
        # point light 4
        ourShader.setVec3("lights[3].position", pointLightPositions[3])
        ourShader.setVec3("lights[3].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[3].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[3].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[3].constant", 1.0)
        ourShader.setFloat("lights[3].linear", 0.09)
        ourShader.setFloat("lights[3].quadratic", 0.032)
        # point light 5
        ourShader.setVec3("lights[3].position", pointLightPositions[4])
        ourShader.setVec3("lights[3].ambient", 0.08, 0.03, 0.01)
        ourShader.setVec3("lights[3].diffuse", 0.2, 0.2, 0.2)
        ourShader.setVec3("lights[3].specular", 0.886, 0.345, 0.133)
        ourShader.setFloat("lights[3].constant", 1.0)
        ourShader.setFloat("lights[3].linear", 0.09)
        ourShader.setFloat("lights[3].quadratic", 0.032)


        # view/projection transformations
        projection = glm.perspective(glm.radians(camera.Zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
        view = camera.GetViewMatrix()
        ourShader.setMat4("projection", projection)
        ourShader.setMat4("view", view)

        # render the loaded model
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0)) # translate it down so it's at the center of the scene
        model = glm.scale(model, glm.vec3(1.0, 1.0, 1.0))	# it's a bit too big for our scene, so scale it down
        ourShader.setMat4("model", model)
        ourModel.Draw(ourShader)

        lightCubeShader.use()
        lightCubeShader.setMat4("projection", projection)
        lightCubeShader.setMat4("view", view)

        glBindVertexArray(lightCubeVAO)
        # for i in range(5):

        #--------------remove comments for debugging-------------------#
        #  model = glm.mat4(1.0)
        #  model = glm.translate(model, pointLightPositions[i])
        #  model = glm.scale(model, glm.vec3(0.2)) # Make it a smaller cube
        #  lightCubeShader.setMat4("model", model)
        #  glDrawArrays(GL_TRIANGLES, 0, 36)
        #--------------------------------------------------------------#

        # render curve
        ourShader.setMat4("model", curvemodel)
        curve.draw()
        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        # -------------------------------------------------------------------------------
        glfwSwapBuffers(window)
        glfwPollEvents()

        t += 0.1 * deltaTime

    # glfw: terminate, clearing all previously allocated GLFW resources.
    # ------------------------------------------------------------------
    glfwTerminate()
    return 0

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------
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

# glfw: whenever the window size changed (by OS or user resize) this callback function executes
# ---------------------------------------------------------------------------------------------
def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:

    # make sure the viewport matches the new window dimensions note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)

# glfw: whenever the mouse moves, this callback is called
# -------------------------------------------------------
def mouse_callback(window: GLFWwindow, xpos: float, ypos: float) -> None:
    global lastX, lastY, firstMouse
    
    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates go from bottom to top

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(xoffset, yoffset)

# glfw: whenever the mouse scroll wheel scrolls, this callback is called
# ----------------------------------------------------------------------
def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:

    camera.ProcessMouseScroll(yoffset)


main()
