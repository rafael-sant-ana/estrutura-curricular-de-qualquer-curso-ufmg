import pymupdf
import re 

from src.classes.subject import Subject

class PdfProcessor:
  def __init__(self, fname):
    self.fname = fname

  def get_pages(self):
    with pymupdf.open(self.fname) as doc:  # open document
      return [page.get_text() for page in doc]

  def process_semester(self, semester):
    subjects_start_on_idx = (re.search(r"Atividades\nAdicionais\n", semester))
    if not subjects_start_on_idx:
      return None, None
    subjects_start_on_idx = subjects_start_on_idx.span()[1]

    semester_subjects = []
    semester_subjects_splitted = semester[subjects_start_on_idx:].split('\n')

    has_ended = False
    amount_labels = 10 # ['Nome', 'Creditos', 'HTeorica', 'HPratica', 'HTotal', 'CVariavel', 'Grupo', 'Natureza', 'PreReqAtividades', 'PreReqAdicionais']

    characteristics = []
    amount_of_splitted_subjects = len(semester_subjects_splitted)
    
    i = 0
    while i < amount_of_splitted_subjects:
      is_new_subject = (i > 0) and (i % amount_labels == 0)
      if is_new_subject:
        semester_subjects.append(Subject(*characteristics))
        characteristics = []

      characteristic = semester_subjects_splitted[i]
      if characteristic == 'Atividades de estágio curricular obrigatório':
        has_ended = True
        break      

      if characteristic in ['Carga horária adicional do período', 'RELATÓRIO DE PERCURSO CURRICULAR']: # Marcadores de que saimos da tabela
        break
      
      if ((i % amount_labels) == 1) and not re.match(r"\d+", characteristic): # a caracteristica atual eh uma extensao do nome, e nao os creditos
        semester_subjects_splitted.pop(i)
        amount_of_splitted_subjects -= 1
        continue 

      is_last_characteristic = (i+1 > 0) and ((i+1) % amount_labels == 0) # is next new subject ?
      if (is_last_characteristic and characteristic != ' -'):
        semester_subjects_splitted.pop(i)
        amount_of_splitted_subjects -= 1
        # lista de  pre requisitos que deveria estar na anterior
        continue 

      characteristics.append(characteristic)
      i += 1
    
    return semester_subjects, has_ended

  def process_page(self, page):
    semesters_texts = re.split(r"\d+º PERÍODO", page)
    semesters_subjects = []
    should_append_first_in_previous_page = False
    has_ended = False

    for i in range(0, len(semesters_texts)):
      subjects, is_last_semester = self.process_semester(semesters_texts[i])
      if not subjects: # apesar de termos cortado em subjects ele nao continha infos
        continue #por exemplo o texto "<infos> 1o periodo <dados-do-semestre>" 
        # ao splittar em \d periodo teriamos que a posicao 0 sera <infos>, que nao contem dados para serem processados do semestre

      if i == 0 and subjects:
        # eh um dos casos em que o semestre eh cortado por falta de espaco
        # entao a proxima pagina comeca com as materias do semestre anterior
        should_append_first_in_previous_page = True

      semesters_subjects.append(subjects)

      if is_last_semester:
        has_ended = True

    
    return semesters_subjects, should_append_first_in_previous_page, has_ended


  def get_subjects_by_semester(self):
    pages = self.get_pages()
    semesters_subjects = []

    for i in range(1, len(pages)): # a 1a pagina eh informacoes de curso
      page = pages[i]
      page_semesters_subjects, should_append_first_in_previous_page, has_ended = self.process_page(page)

      if should_append_first_in_previous_page:
        semesters_subjects[-1].extend(page_semesters_subjects[0])
        page_semesters_subjects = page_semesters_subjects[1:]
      
      semesters_subjects.extend(page_semesters_subjects)

      if has_ended:
        break

    return semesters_subjects

