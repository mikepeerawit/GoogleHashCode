import numpy as np

teamCount = 4
ingredientSize = 4
activePizza = [0, 1, 2, 3]
pizzaDataList = [[True, False, True, True],[False, False, False, True],[True, True, False, False],[False, False, True, False]]

uniqueModifier = 1
repeatModifier = 0
combSizeModifier = 1
combTresholdModifier = 0.9

findCombination_activePizza = activePizza

def GetDifferentScore(pizzaA, pizzaB):
  similarity = np.logical_and(pizzaA, pizzaB)
  return len(pizzaA) - sum(similarity)

def GetCombinationScore(combination):

  unique = pizzaDataList[combination[0]]
  for i in range(1, len(combination)):
    unique = np.logical_or(unique, pizzaDataList[combination[i]])
  repeat = pizzaDataList[combination[0]]
  for i in range(1, len(combination)):
    repeat = np.logical_and(repeat, pizzaDataList[combination[i]])

  uniqueCount = sum(unique)
  repeatCount = sum(repeat)
  combsSize = len(combination)

  score = ((uniqueCount * uniqueModifier) - (repeatCount * repeatModifier))
  # score = ((uniqueCount * uniqueModifier) - (repeatCount * repeatModifier)) * ((5 - combsSize) * combSizeModifier)

  return score

def GetBestPizza(pizzaIndex):
  
  bestPizza = -1
  bestScore = 0

  for i in findCombination_activePizza:
    currentScore = GetDifferentScore(pizzaDataList[pizzaIndex], pizzaDataList[i])
    if (bestScore < currentScore):
      bestPizza = i
      bestScore = currentScore
  
  return bestPizza

def GetBestPizzaCombination(pizzaIndex):
  findCombination_activePizza = activePizza

  combination = []
  combination.append(pizzaIndex)

  findCombination_activePizza.remove(pizzaIndex)

  for i in range(3):
    bestPizza = GetBestPizza(combination[len(combination) - 1])
    if (bestPizza != -1):
      combination.append(bestPizza)
      findCombination_activePizza.remove(bestPizza)

      totalScore = GetCombinationScore(combination)

      if (totalScore > ingredientSize * combTresholdModifier):
        return combination

  return combination

def AssignPizzaToTeam():

  for i in range(teamCount):
    bestCombiantion = []
    bestScore = 0

    for j in activePizza:
      currentCombination = GetBestPizzaCombination(j)
      currentScore = GetCombinationScore(currentCombination)

      if (len(currentCombination) > 1 and teamCount > 0):
        if (bestScore < currentScore or (bestScore == currentScore and len(currentCombination) < len(bestCombiantion))):
          bestScore = currentScore
          bestCombiantion = currentCombination
    if (len(bestCombiantion) > 0):
      print(len(bestCombiantion), " ", end='')
      for n in bestCombiantion:
        print(bestCombiantion[n], " ", end='')
      print()
    
    if (len(activePizza) < 2):
      break

def Main():

  activePizza = range(len(pizzaDataList))

  AssignPizzaToTeam()

  return 0

Main()
