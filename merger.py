from subprocess import PIPE, Popen
import canvasapi
import canvasapi.course
import config
import shutil
from cache import get_course_dir
import os
from logger import LoggerFactory
from PyPDF2 import PdfFileMerger


_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Merge.LOG_LEVEL)

MERGE_DIR = config.Merge.MERGE_DIR


def convert_to_pdf(course_dir: str):
    try:
        _log.info(f'Convertendo arquivos de {course_dir}')
        pdf_dir = os.path.join(course_dir, 'pdf')

        # Recria o diretorio de pdfs
        if os.path.exists(pdf_dir):
            shutil.rmtree(pdf_dir)
        os.makedirs(pdf_dir)

        # Converte os arquivos
        files = os.listdir(course_dir)
        p = Popen(['libreoffice',
                   '--headless',
                   '--convert-to',
                   'pdf', '--outdir', 'pdf', *files],
                  cwd=course_dir,
                  stdout=PIPE)
        p.wait(timeout=120)

        # Copia os arquivos pdf para o diretorio de pdfs
        for f in os.listdir(course_dir):
            if f.endswith('.pdf'):
                shutil.copy(os.path.join(course_dir, f), pdf_dir)

    except Exception as e:
        _log.error(f'Erro ao converter arquivos: {course_dir}')
        _log.error(e)

    return os.listdir(pdf_dir) if os.path.exists(pdf_dir) else []


def merge_dir(dir: str, dest_file: str) -> list:
    merger = PdfFileMerger()
    dir_files = os.listdir(dir)
    for f in dir_files:
        fpath = os.path.join(dir, f)
        merger.append(fpath)

    _log.info(f'Mergeando arquivos de {dir}')

    if os.path.exists(dest_file):
        os.remove(dest_file)

    merger.write(dest_file)
    merger.close()
    return dir_files


def merge(c: canvasapi.course.Course) -> str:
    cname = c.name.split('-')[0].strip().replace(' ', '_').title()
    course_dir = get_course_dir(c)
    course_pdf_dir = os.path.join(course_dir, 'pdf')
    out_file = os.path.join(course_dir, f'{cname}.pdf')

    pdf_files = []
    for f in os.listdir(course_pdf_dir):
        pdf_files.append(os.path.join(course_dir, f))

    _log.info(f'Mergeando {len(pdf_files)} arquivos:')

    merger = PdfFileMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    # if os.path.exists(out_file):
    #     os.remove(out_file)
    merger.write(out_file)
    merger.close()

    return {
        'course': c.name,
        'merge_path': out_file,
        'merge_filename': out_file.split('/')[-1],
        'total_files_merged': len(pdf_files),
        'files_merged': [p.split('/')[-1] for p in pdf_files]
    }
