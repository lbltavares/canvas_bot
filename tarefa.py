import re
from datetime import datetime as dt


def from_dict(d):
    desc = d.get('description')
    if desc:
        desc = str(desc)
        desc = re.sub(r'<[^>]*>', '', desc)
        desc = re.sub(r'(&nbsp|&amp|&quot|&lt|&gt)', '', desc)
        desc = re.sub(r'\s+', ' ', desc)
        desc = re.sub(r'https?://[^\s]+', '', desc)
    return {
        # 'course_name': None,
        'name': d.get('name') or d.get('title'),
        'id': d.get('id'),
        'description': desc,
        'due_at': d.get('due_at_date').astimezone().strftime('%d/%m/%Y %H:%M:%S') if d.get('due_at_date') else None,
        'points_possible': d.get('points_possible'),
        'url': d.get('html_url'),
        'question_count': d.get('question_count'),
    }


def faltam_quantos_dias(tarefa):
    if tarefa['due_at'] is None:
        return None
    return (dt.strptime(tarefa['due_at'], '%d/%m/%Y %H:%M:%S') - dt.now()).days


def format(tarefa):
    faltam = faltam_quantos_dias(tarefa)
    ja_passou = faltam is not None and faltam < 0
    faltam = max(faltam, 0) if faltam is not None else None
    desc = tarefa['description']
    desc = desc[:50]+'...' if desc else None
    return (
        f"\tcourse_name:     {tarefa.get('course_name')}\n" +
        f"\tname:            {tarefa.get('name')}\n" +
        f"\tid:              {tarefa.get('id')}\n" +
        f"\tdescription:     {desc}\n" +
        f"\tdue_at:          {tarefa.get('due_at')}\n" +
        f"\tpoints_possible: {tarefa.get('points_possible')}\n" +
        f"\turl:             {tarefa.get('url')}\n" +
        f"\tquestion_count:  {tarefa.get('question_count')}\n" +
        f"\tfaltam:          {faltam} dias\n" +
        f"\tja_passou:       {ja_passou}\n"
    )
