import canvasapi
import canvasapi.course
import config
import shutil
import os
from logger import LoggerFactory
from docx2pdf import convert
from PyPDF2 import PdfFileMerger


_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Merge.LOG_LEVEL)

MERGE_DIR = config.Merge.MERGE_DIR


def get_course_dir(c: canvasapi.course.Course):
    cname = c.name.split('-')[0].strip().replace(' ', '_').title()
    return os.path.join(MERGE_DIR, cname)


def download_files(c: canvasapi.course.Course):
    files = c.get_files()
    files = [f for f in files]
    subdir = get_course_dir(c)
    if os.path.exists(subdir):
        shutil.rmtree(subdir)
    os.makedirs(subdir)
    for f in files:
        fname = f.filename
        mime = f.mime_class
        if mime not in config.Merge.MIME_CLASS:
            _log.info(f'Pulando arquivo: {fname} (mime: {mime})')
            continue
        fsize = f.size
        mb = fsize / 1024 / 1024
        _log.info(f'Baixando arquivo: {fname} ({mb}mb)')
        f.download(os.path.join(subdir, fname))
        fpath = os.path.join(subdir, fname)
        if mime == 'doc':
            try:
                convert_doc_file(fpath)
            except Exception as e:
                _log.error(f'Erro ao converter arquivo: {fpath}')
                _log.error(e)
    return files


def convert_doc_file(fpath: str):
    try:
        _log.info(f'Convertendo arquivo: {fpath}')
        convert(fpath, fpath + '.pdf')
    except Exception as e:
        _log.error(f'Erro ao converter arquivo: {fpath}')
        _log.error(e)


def merge(c: canvasapi.course.Course) -> str:
    pdf_files = []
    for f in os.listdir(get_course_dir(c)):
        if f.endswith('.pdf'):
            pdf_files.append(os.path.join(get_course_dir(c), f))

    _log.info(f'Juntando arquivos: {[p.split("/")[-1] for p in pdf_files]}')
    merger = PdfFileMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    cname = c.name.split('-')[0].strip().replace(' ', '_').title()
    out_dir = os.path.join(get_course_dir(c), f'{cname}.pdf')
    if os.path.exists(out_dir):
        os.remove(out_dir)
    merger.write(out_dir)
    merger.close()
    for pdf in pdf_files:
        os.remove(pdf)
    return {
        'course': c.name,
        'merge_path': out_dir,
        'merge_filename': out_dir.split('/')[-1],
        'total_files_merged': len(pdf_files),
        'files_merged': [p.split('/')[-1] for p in pdf_files]
    }
