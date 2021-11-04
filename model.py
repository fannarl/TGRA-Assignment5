from OpenGL.GL import * 
    
import glm

from PIL import Image

import assimp_py

from mesh import Mesh, Texture
from shader import Shader

import platform, ctypes, os

from typing import List


LOAD_IMAGE = lambda name: Image.open(name)

class Model:
    def __init__(self, path: str, gamma : bool = False):
        self.gammaCorrection = gamma
        self.loadModel(path)

    def Draw(self, shader : Shader):
        for mesh in self.meshes:
            mesh.Draw(shader)
            
    def loadModel(self, path : str):
        assimp_flags = assimp_py.Process_Triangulate | assimp_py.Process_GenSmoothNormals | assimp_py.Process_FlipUVs | assimp_py.Process_CalcTangentSpace
        scene = assimp_py.ImportFile(path, assimp_flags)

        self.directory = os.path.dirname(path)

        self.meshes = []
        self.textures_loaded = []

        self.processMeshes(scene)

    def processMeshes(self, scene : assimp_py.Scene):
        for mesh in scene.meshes:
            self.meshes.append(self.processMesh(mesh, scene))

    def processMesh(self, mesh : assimp_py.Mesh, scene : assimp_py.Scene) -> Mesh:
        vertices = []
        indices = []
        textures = []

        for i in range(mesh.num_vertices):
            vertices += list(mesh.vertices[i])
            if (mesh.normals):
                vertices += list(mesh.normals[i][:3])
            else:
                vertices += [0] * 3
            if(mesh.texcoords and mesh.texcoords[0] and mesh.tangents and mesh.bitangents):
                vertices += list(mesh.texcoords[0][i][:2]) + list(mesh.tangents[i][:3]) + list(mesh.bitangents[i][:3])
            else:
                vertices += [0] * (2 + 3 + 3)

        for i in range(mesh.num_faces):
            face = mesh.faces[i]
            indices += list(face)     

        material = scene.materials[mesh.material_index]    

        diffuseMaps = self.loadMaterialTextures(material, assimp_py.TextureType_DIFFUSE, "texture_diffuse")
        textures += diffuseMaps

        specularMaps = self.loadMaterialTextures(material, assimp_py.TextureType_SPECULAR, "texture_specular")
        textures += specularMaps

        normalMaps = self.loadMaterialTextures(material, assimp_py.TextureType_HEIGHT, "texture_normal")
        textures += normalMaps

        heightMaps = self.loadMaterialTextures(material, assimp_py.TextureType_AMBIENT, "texture_height")
        textures += heightMaps
        
        return Mesh(glm.array.from_numbers(glm.float32, *vertices), indices, textures)

    def loadMaterialTextures(self, mat : dict, type : int, typeName : str) -> List[Texture]:
        textures = []
        for i in range(list(mat["TEXTURES"].keys()).count(type)):
            texStr = mat["TEXTURES"][type][i]
            if not list(filter(lambda texture: texture.path == texStr, self.textures_loaded)):                
                id = TextureFromFile(texStr, self.directory)
                type = typeName
                path = texStr

                texture = Texture(id, type, path)
                textures.append(texture)
                self.textures_loaded.append(texture)

        return textures


def TextureFromFile(path : str, directory : str, gamma : bool = False) -> int:

    filename = os.path.join(directory, path)
    
    textureID = glGenTextures(1)

    try:
        img = LOAD_IMAGE(filename)
        
        nrComponents = len(img.getbands())

        format = GL_RED if nrComponents == 1 else \
                 GL_RGB if nrComponents == 3 else \
                 GL_RGBA 

        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexImage2D(GL_TEXTURE_2D, 0, format, img.width, img.height, 0, format, GL_UNSIGNED_BYTE, img.tobytes())
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img.close()

    except:

        print("Texture failed to load at path: " + path)

    return textureID

