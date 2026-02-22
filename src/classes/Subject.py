
class Subject:
  def __init__(self, name, credits, theoryHours, practicalHours, totalHours, variableContent, group, nature, neededActivities, neededExtra):
    self.credits = int(credits)
    self.theoryHours = int(theoryHours)
    self.practicalHours = int(practicalHours)
    self.totalHours = int(totalHours)
    self.variableContent = variableContent == 'S'
    self.group = group
    self.nature = nature
    self.neededActivities = neededActivities.split(', ')
    self.neededExtra = neededExtra

    _DIG, code, *discipline_alias = name.split(' - ')

    self.name = (' - ').join(discipline_alias)
    self.code = code

    self.fields = ['name', 'code', 'credits', 'theoryHours', 'practicalHours', 'totalHours', 'variableContent', 'group', 'nature', 'neededActivities', 'neededExtra']
    
  def to_dict(self):
    return {
      field: getattr(self, field) for field in self.fields
    }

  def __str__(self):
    return f'{self.name}'