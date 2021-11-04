#version 330 core
out vec4 FragColor;

// struct Material {
//     sampler2D diffuse;
//     sampler2D specular;    
//     float shininess;
// }; 

struct Light {
    vec3 position;  
  
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
	
    float constant;
    float linear;
    float quadratic;
};

#define NR_POINT_LIGHTS 4

in vec3 FragPos;  
in vec3 Normal;  
in vec2 TexCoords;

uniform vec3 viewPos;
// uniform Material material;
uniform Light lights[NR_POINT_LIGHTS];
uniform sampler2D texture_diffuse1;
uniform sampler2D texture_specular1;

vec3 CalcPointLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main()
{    
    // ambient
    // vec3 ambient = light.ambient * texture(texture_diffuse1, TexCoords).rgb;

    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);	
    // // diffuse 
    // vec3 norm = normalize(Normal);
    // vec3 lightDir = normalize(light.position - FragPos);
    // float diff = max(dot(norm, lightDir), 0.0);
    // vec3 diffuse = light.diffuse * diff * texture(texture_diffuse1, TexCoords).rgb;  
    
    // // // specular
    // vec3 viewDir = normalize(viewPos - FragPos);
    // vec3 reflectDir = reflect(-lightDir, norm);  
    // float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    // vec3 specular = light.specular * spec * texture(texture_specular1, TexCoords).rgb;  
    
    // // attenuation
    // float distance    = length(light.position - FragPos);
    // float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    

    // ambient  *= attenuation;  
    // diffuse   *= attenuation;
    // specular *= attenuation;   
        
    // vec3 result = ambient + diffuse + specular;
    // FragColor = vec4(result, 1.0);
    // FragColor = texture(texture_diffuse1, TexCoords);
    // vec3 result = ambient + diffuse + specular;
    vec3 result;

    for(int i = 0; i < NR_POINT_LIGHTS; i++)
        result += CalcPointLight(lights[i], norm, FragPos, viewDir);

    FragColor = vec4(result, 1.0);
}

vec3 CalcPointLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    // vec3 lightDir = normalize(light.position - fragPos);
    // // diffuse shading
    // float diff = max(dot(normal, lightDir), 0.0);
    // // specular shading
    // vec3 reflectDir = reflect(-lightDir, normal);
    // float spec = pow(max(dot(viewDir, reflectDir), 0.0), 0.32);
    // // attenuation
    // float distance = length(light.position - fragPos);
    // float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    
    // // combine results
    // vec3 ambient = light.ambient * vec3(texture(texture_diffuse1, TexCoords));
    // vec3 diffuse = light.diffuse * diff * vec3(texture(texture_diffuse1, TexCoords));
    // vec3 specular = light.specular * spec * vec3(texture(texture_specular1, TexCoords));
    // ambient *= attenuation;
    // diffuse *= attenuation;
    // specular *= attenuation;

    // ambient
    vec3 ambient = light.ambient * texture(texture_diffuse1, TexCoords).rgb;

    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * diff * texture(texture_diffuse1, TexCoords).rgb;  
    
    // // specular
    vec3 reflectDir = reflect(-lightDir, normal);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 100.0);
    vec3 specular = light.specular * spec * texture(texture_specular1, TexCoords).rgb;  
    
    // attenuation
    float distance    = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));    

    ambient  *= attenuation;  
    diffuse   *= attenuation;
    specular *= attenuation;   
    return (ambient + diffuse + specular);
}