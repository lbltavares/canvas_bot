import re
from datetime import datetime as dt, timezone


class Tarefa:
    def __init__(self, d):
        self.d = d

    def get_name(self):
        return self.d.get('name')

    def get_id(self):
        return self.d.get('id')

    def get_parsed_description(self):
        desc = self.get_description()
        if desc:
            desc = str(desc)
            desc = re.sub(r'<[^>]*>', '', desc)
            desc = re.sub(r'(&nbsp|&amp|&quot|&lt|&gt)', '', desc)
            desc = re.sub(r'\s+', ' ', desc)
            desc = re.sub(r'https?://[^\s]+', '', desc)
        return desc

    def get_description(self):
        return self.d.get('description')

    def get_due_at_date(self):
        return self.d.get('due_at_date')

    def get_due_at(self):
        return self.d.get('due_at')

    def get_points_possible(self):
        return self.d.get('points_possible')

    def get_html_url(self):
        return self.d.get('html_url')

    def get_question_count(self):
        return self.d.get('question_count')

    @staticmethod
    def from_dict(d):
        return Tarefa(d)

    def __str__(self):
        return self.d

    def __dict__(self):
        d = self.d
        desc = self.get_parsed_description()
        return {
            # 'course_name': None,
            'name': d.get('name') or d.get('title'),
            'id': d.get('id'),
            'description': desc,
            'due_at': due_at,
            'points_possible': d.get('points_possible'),
            'url': d.get('url') or d.get('html_url'),
            'question_count': d.get('question_count'),
        }


def from_dict(d):
    desc = d.get('description')
    if desc:
        desc = str(desc)
        desc = re.sub(r'<[^>]*>', '', desc)
        desc = re.sub(r'(&nbsp|&amp|&quot|&lt|&gt)', '', desc)
        desc = re.sub(r'\s+', ' ', desc)
        desc = re.sub(r'https?://[^\s]+', '', desc)
    due_at = d.get('due_at_date') or d.get('due_at')
    return {
        # 'course_name': None,
        'name': d.get('name') or d.get('title'),
        'id': d.get('id'),
        'description': desc,
        'due_at': due_at,
        'points_possible': d.get('points_possible'),
        'url': d.get('url') or d.get('html_url'),
        'question_count': d.get('question_count'),
    }


def faltam_quantos_dias(t):
    if t.get('due_at') is None:
        return None
    return (t.get('due_at') - dt.now(timezone.utc)).days


def format(t):
    faltam = faltam_quantos_dias(t)
    ja_passou = faltam is not None and faltam < 0
    faltam = max(faltam, 0) if faltam is not None else None
    desc = t['description']
    desc = desc[:50]+'...' if desc else None
    return (
        f"\tcourse_name:     {t.get('course_name')}\n" +
        f"\tname:            {t.get('name')}\n" +
        f"\tid:              {t.get('id')}\n" +
        f"\tdescription:     {desc}\n" +
        f"\tdue_at:          {t.get('due_at')}\n" +
        f"\tpoints_possible: {t.get('points_possible')}\n" +
        f"\turl:             {t.get('url')}\n" +
        f"\tquestion_count:  {t.get('question_count')}\n" +
        f"\tfaltam:          {faltam} dia(s)\n" +
        f"\tja_passou:       {ja_passou}\n"
    )
