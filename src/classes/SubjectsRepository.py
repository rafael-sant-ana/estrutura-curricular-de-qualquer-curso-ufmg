from src.classes.Subject import Subject
import pandas as pd

class SubjectsRepository:
  def __init__(self, subjects_by_semester: list[list[Subject]]):
    self.subjects_by_semester = subjects_by_semester

  def to_pandas(self):
    subjects_as_dict = []
    for semester_idx in range(len(self.subjects_by_semester)):
      semester = self.subjects_by_semester[semester_idx]
      for subject in semester:
        ## **dict retorna chave: valor
        ## *list retorna [...list]
        subjects_as_dict.append({**subject.to_dict(), "semester": semester_idx+1})

    df = pd.DataFrame(subjects_as_dict)
    return df