def init_ini(self, file='meilleurs_scores.ini'): #creates file if needed
  """create a .ini files for high-score with ezCLI fonction """
  try :
      read_ini(file)
  except :
      D = {}
      for area in set([ i*j for i in range(5,20) for j in range(5,20)]):
          D[area] = {}
          for i in range(1,11):
              D[area]['Noone %s' % (i)] = 1
      write_ini(file, D)
# ------------------------------------------------------------------------------
def write(self,area, score, file='meilleurs_scores.ini'): # write user nameand his score if player do a high-score
  """write a .ini files for high-score with ezCLI fonction """
  dernier_score = get(area,file)[-1] # Gets the last element of the best scores
  if dernier_score[0] >= score:
      dic = read_ini(file)
      dic[str(area)].pop(dernier_score[1])
      dic[str(area)] = score
      write_ini(file, dic)
      return True
  return False
# ------------------------------------------------------------------------------
def get(self,area, file='meilleurs_scores.ini'):     #import of high-score for area chosen
  dic = read_ini(file)[str(area)]
  liste = [(dic[key],key) for key in dic.keys()]
  liste.sort()
  return liste
