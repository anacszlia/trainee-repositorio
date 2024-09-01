# Resposta etapa 2
Sim,é possível reutilizar o conteiner parado reiniciando ele através do comando:
```docker
docker start container_nome
```
ou executar novamente uma imagem já criada,deve-se criar um novo container baseado nela e executar o comando:
docker run --rm --name container-carguru2 carguru-image

