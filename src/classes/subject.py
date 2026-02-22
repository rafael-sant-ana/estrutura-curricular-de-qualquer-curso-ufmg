
class Subject:
  def __init__(self, name, credits, theoryHours, practicalHours, totalHours, variableContent, group, nature, neededActivities, neededExtra):
    self.name = name
    self.credits = credits
    self.theoryHours = theoryHours
    self.practicalHours = practicalHours
    self.totalHours = totalHours
    self.variableContent = variableContent
    self.group = group
    self.nature = nature
    self.neededActivities = neededActivities
    self.neededExtra = neededExtra
    
  def __str__(self):
    return f'{self.name}'