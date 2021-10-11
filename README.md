


| **Comando**       | **Descrição**                                                 |
|-------------------|---------------------------------------------------------------|
| /calendario       | Mostra o calendario de tarefas                                |
| /proximas         | Exibe as próximas tarefas                                     |
| /all              | Exibe todas as futuras tarefas, ordenadas por data de entrega |
| /courses          | Exibe uma lista de disciplinas e seus ids                     |
| /merge 123        | Retorna o merge em PDF da disciplina com id=123               |
| /pontos           | Retorna um sumário com a pontuação em cada disciplina         |
| /update           | Atualiza o cache manualmente                                  |
| /notificar on/off | Ativa ou desativa a notificação de próxima atividade          |
| /automerge on/off | Ativa ou desativa o merge automático antes de cada tarefa     |


```
course:
    id: int
    nome: str
    tarefas: [tarefa]


tarefa:
    id: int
    name: str
    description: str
    due_at: datetime
    points_possible: int
    url: str

    question_count: int
    published: bool
```

