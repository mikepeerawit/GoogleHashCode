import numpy as np
from collections import OrderedDict 

DATASET = ""
FILE_PATH = ""
OUTPUT_TXT = ""

class DataPrebs:
    #variable member
    #teamCount[0] is team2
    #teamCount[1] is team3
    #teamCount[2] is team4
    _teamCount = []
    #list of unique ingredient
    _ingredientList = []
    #index mapping of unique ingredient
    _ingredientDict= {}
    #list of pizza bits
    _pizzaList = []
    #ingredient size
    _ingredientSize = 0


    #public function member
    #load file data
    def LoadData(self, filePath):
        file = open(filePath, "r")
        wordList = file.read().split()

        self._AssignTeamData(int(wordList[1]), int(wordList[2]), int(wordList[3]))

        for i in range(4, len(wordList)):
            self._AssignIngredientData(wordList[i])
            self._AssignPizzaData(wordList[i])
        
        self._ingredientSize = len(self._ingredientList)

        self._AdjustPizzaSize()

        #testing ingredient list
        """for i in range(0, len(self._ingredientList)):
            print(self._ingredientList[i])"""
        #testing pizza list
        """for i in range(0, len(self._pizzaList)):
            print(self._pizzaList[i])"""

        self._ingredientList.clear()
        self._ingredientDict.clear()
        
        file.close()

    #reset file data
    def ResetFile(self):
        file = open(OUTPUT_TXT, "w")
        file.write("")

    #write file data
    def OutputFile(self, teamNumber, pizzaList):
        file = open(OUTPUT_TXT, "a")
        file.write(str(teamNumber) + " ")
        for i in range(0, len(pizzaList)):
            file.write(str(pizzaList[i]) + " ")
        file.write('\n')
        file.close()

    #finalizing output file data
    def FinalizingOutput(self, dataSet, teamDelivered, pizzaDelivered, mlRecursion):
        #read file data
        readFile = open(OUTPUT_TXT, "r")
        content = readFile.read()
        #write file data
        folderPath = "Outputs/" + "DataSet_" + dataSet + "/"
        fileName = "Output_DataSet_" + dataSet + "_" + str(teamDelivered) + "_" + str(pizzaDelivered) + "_ML_" + str(mlRecursion) + ".txt"
        writeFile = open(folderPath + fileName, "w")
        writeFile.write(str(teamDelivered)+'\n')
        writeFile.write(content)



    #constructor
    def __init__(self):
        self.LoadData(FILE_PATH)



    #getters
    def GetTeamCount(self, teamNumber):
        if teamNumber >= 2 and teamNumber <= 4:
            return self._teamCount[teamNumber - 2]
        else :
            print("Invalid team number: " + str(teamNumber))
            return 0
    
    def GetTotalTeamCount(self):
        return sum(self._teamCount)

    def GetPizzaList(self):
        return self._pizzaList
    
    def GetIngredientSize(self):
        return self._ingredientSize



    #assigning private function
    def _AssignTeamData(self, team2, team3, team4):
        self._teamCount.append(team2)
        self._teamCount.append(team3)
        self._teamCount.append(team4)

    def _AssignIngredientData(self, ingredient):
        if ((ingredient.isdigit() == False) and (ingredient not in self._ingredientList)):
            self._ingredientList.append(ingredient)
            self._ingredientDict[ingredient] = len(self._ingredientList) - 1

    def _AssignPizzaData(self, ingredient):
        if (ingredient.isdigit() == True):
            self._pizzaList.append(list())
        else:
            pizzaIndex = len(self._pizzaList) - 1
            ingredientIndex = self._ingredientDict[ingredient]
            if ingredientIndex >= len(self._pizzaList[pizzaIndex]):
                for i in range(len(self._pizzaList[pizzaIndex]), ingredientIndex + 1):
                    self._pizzaList[pizzaIndex].append(False)
            self._pizzaList[pizzaIndex][ingredientIndex] = True
    
    def _AdjustPizzaSize(self):
        for i in range(0, len(self._pizzaList)):
            for j in range(len(self._pizzaList[i]), self._ingredientSize):
                self._pizzaList[i].append(False)            

def SetupDataSetType(dataType):
  global DATASET
  global FILE_PATH
  global OUTPUT_TXT

  DATASET = dataType
  OUTPUT_TXT = "Outputs/" + "DataSet_" + dataType + "/Temp" + ".txt"

  if (dataType == "A"):
    FILE_PATH = "Inputs/Raw_DataSets/a_example"
  elif (dataType == "B"):
    FILE_PATH = "Inputs/Raw_DataSets/b_little_bit_of_everything.in"
  elif (dataType == "C"):
    FILE_PATH = "Inputs/Raw_DataSets/c_many_ingredients.in"
  elif (dataType == "D"):
    FILE_PATH = "Inputs/Raw_DataSets/d_many_pizzas.in"
  elif (dataType == "E"):
    FILE_PATH = "Inputs/Raw_DataSets/e_many_teams.in"

print("Start DataPrebs")

SetupDataSetType("C")
dp = DataPrebs()

print("End DataPrebs")

# Data Compile

totalTeamCount = dp.GetTotalTeamCount()
teamCount = [dp.GetTeamCount(2), dp.GetTeamCount(3), dp.GetTeamCount(4)]
ingredientSize = dp.GetIngredientSize()
activePizza = [True]*len(dp.GetPizzaList())

uniqueModifier = 1
repeatModifier = 0
combSizeModifier = 1
combTresholdModifier = 0.8

teamDeliverd = 0
pizzaDeliverd = 0

findCombination_activePizza = activePizza

def DeductTeamCount(teamNumber):
  global teamCount
  if teamNumber >= 2 and teamNumber <= 4:
      teamCount[teamNumber - 2] -= 1
  else :
      print("Invalid team number: " + str(teamNumber))

def GetDifferentScore(pizzaA, pizzaB):
  similarity = np.logical_or(pizzaA, pizzaB)
  return sum(similarity)

def GetCombinationScore(combination):

  unique = dp.GetPizzaList()[combination[0]]
  for i in range(1, len(combination)):
    unique = np.logical_or(unique, dp.GetPizzaList()[combination[i]])
  repeat = dp.GetPizzaList()[combination[0]]
  for i in range(1, len(combination)):
    repeat = np.logical_and(repeat, dp.GetPizzaList()[combination[i]])

  uniqueCount = sum(unique)
  repeatCount = sum(repeat)
  combsSize = len(combination)

  score = ((uniqueCount * uniqueModifier) - (repeatCount * repeatModifier))
  # score = ((uniqueCount * uniqueModifier) - (repeatCount * repeatModifier)) * ((5 - combsSize) * combSizeModifier)

  return score

def GetBestPizza(pizzaIndex):
  
  global findCombination_activePizza

  bestPizza = -1
  bestScore = 0

  currentPizzaData = list(dp.GetPizzaList()[pizzaIndex])

  for i in range(len(findCombination_activePizza)):
    if (findCombination_activePizza[i] == True):
      currentScore = GetDifferentScore(currentPizzaData, dp.GetPizzaList()[i])
      if (bestScore <= currentScore):
        bestPizza = i
        bestScore = currentScore
        
        currentPizzaData = np.logical_or(dp.GetPizzaList()[pizzaIndex], dp.GetPizzaList()[i])
        ingredientSize * combTresholdModifier
        if (bestScore > float(ingredientSize) * combTresholdModifier):
          break
  
  findCombination_activePizza[bestPizza] = False

  return bestPizza

def GetBestPizzaCombination(pizzaIndex):
  global findCombination_activePizza
  findCombination_activePizza = list(activePizza)

  combination = []
  combination.append(pizzaIndex)

  for i in range(3):
    bestPizza = GetBestPizza(combination[len(combination) - 1])
    if (bestPizza != -1):
      combination.append(bestPizza)
      totalScore = GetCombinationScore(combination)

  return combination

def AssignPizzaToTeam():
  global activePizza
  global teamDeliverd
  global pizzaDeliverd 

  for i in range(totalTeamCount):
    bestCombiantion = []
    bestScore = 0

    for j in range(len(activePizza)):
      if (activePizza[j] == True):
        currentCombination = GetBestPizzaCombination(j)
        currentScore = GetCombinationScore(currentCombination)

        if (len(currentCombination) > 1 and (teamCount[len(currentCombination)-2] > 0)):
          if (bestScore < currentScore or ((bestScore == currentScore) and len(currentCombination) < len(bestCombiantion))):
            bestScore = currentScore
            bestCombiantion = currentCombination
            break

    if (len(bestCombiantion) > 0):
      dp.OutputFile(len(bestCombiantion), bestCombiantion)
      print(len(bestCombiantion), " ", end='')
      for n in range(len(bestCombiantion)):
        print(bestCombiantion[n], " ", end='')
        activePizza[bestCombiantion[n]] = False
      print()
      DeductTeamCount(len(bestCombiantion))
      teamDeliverd += 1
      pizzaDeliverd += len(bestCombiantion)
    if (len(activePizza) < 2):
      break

def Main():

  print("Start DataCompiler")

  dp.ResetFile()

  global activePizza
  activePizza = [True]*len(dp.GetPizzaList())
  
  AssignPizzaToTeam()

  dp.FinalizingOutput(DATASET, teamDeliverd, pizzaDeliverd, 1)

  print("End DataCompiler")

  return 0

Main()
