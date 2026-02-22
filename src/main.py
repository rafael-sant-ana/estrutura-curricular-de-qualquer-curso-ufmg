from src.classes.PdfProcessor import PdfProcessor
from src.classes.SubjectsRepository import SubjectsRepository
from src.classes.Visualizer import Visualizer

def main():
  fname = "grade-compsci.pdf"

  pdf = PdfProcessor(fname)
  subjects_by_semester = pdf.get_subjects_by_semester()
  
  subjects_repository = SubjectsRepository(subjects_by_semester)

  df = subjects_repository.to_pandas()

  visualizer = Visualizer(df)

  visualizer.generate_visualization()

if __name__ == "__main__":
  main()
 