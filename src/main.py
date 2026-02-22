from src.classes.PdfProcessor import PdfProcessor
from src.classes.SubjectsRepository import SubjectsRepository

def main():
  fname = "grade-farmacia.pdf"

  pdf = PdfProcessor(fname)
  subjects_by_semester = pdf.get_subjects_by_semester()
  
  subjects_repository = SubjectsRepository(subjects_by_semester)

  df = subjects_repository.to_pandas()

  print(df)

if __name__ == "__main__":
  main()
