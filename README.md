
## Comandos

| **Comando**       | **Descrição**                                                 | **Status**
|-------------------|---------------------------------------------------------------|------------
| /proximas [1-15]         | Exibe as próximas [1-15] tarefas                       | OK
| /all              | Exibe todas as futuras tarefas, ordenadas por data de entrega | OK
| /courses          | Exibe uma lista de disciplinas e seus ids                     | OK
| /merge [id]        | Retorna o merge em PDF de uma disciplina específica          | OK
| /pontos           | Retorna um sumário com a pontuação em cada disciplina*        | Não implementado
| /update           | Atualiza o cache manualmente                                  | OK
| /notificar on/off | Ativa ou desativa a notificação de próxima atividade          | OK
| /automerge on/off | Ativa ou desativa o merge automático antes de cada tarefa     | OK

## Instruções

0. [Crie um token no Canvas](https://kb.iu.edu/d/aaja) (Conta -> Configurações -> Novo Token de Acesso)
1. [Crie um bot do telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot), e [obtenha o seu chat_id](https://newbedev.com/how-to-obtain-telegram-chat-id-for-a-specific-user)
2. ```git clone https://github.com/lbltavares/canvas_bot.git```
3. Preencha o [```docker-compose.yml```](https://github.com/lbltavares/canvas_bot/blob/main/docker-compose.yml)
4. ```docker-compose up -d```

#### Configurações
* Todas as configurações estão no arquivo [```config.py```](https://github.com/lbltavares/canvas_bot/blob/main/config.py)


#### Pastas:
- ```📂 logs``` - Um arquivo para os logs gerais (app.log), e um arquivo apenas para os logs do telegram (telegram.log)
- ```📂 merges``` - Os merges de PDF ficam salvos aqui

## Screenshots

![image](https://user-images.githubusercontent.com/34322384/137173722-baac93cb-894c-4f56-8412-4b4d5637c727.png)
![image](https://user-images.githubusercontent.com/34322384/137173801-2f17e167-6b51-4d56-9b9a-55c45738a327.png)
![image](https://user-images.githubusercontent.com/34322384/137173911-8dc5da64-701c-49d4-8d0f-2de2c8a22288.png)
![image](https://user-images.githubusercontent.com/34322384/137174047-96d8b5c7-6ef6-4437-9b64-b543ec24d94a.png)


## TODO
- Exibir o sumário de notas*
- Adicionar outros formatos para o merge (alem de PDF)
- Omitir as tarefas que já foram entregues
