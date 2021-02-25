from collections import OrderedDict 

FILE_PATH = "Inputs/Raw_DataSets/a_example"
#FILE_PATH = "Inputs/Raw_DataSets/b_little_bit_of_everything"
#FILE_PATH = "Inputs/Raw_DataSets/c_many_ingredients"
#FILE_PATH = "Inputs/Raw_DataSets/d_many_pizzas"
#FILE_PATH = "Inputs/Raw_DataSets/e_many_teams"

OUTPUT_TXT = "output.txt"

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

        self._AssignTeamData(wordList[1], wordList[2], wordList[3])

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
        file.close()

    #finalizing output file data
    def FinalizingOutput(dataSet, score, teamDelivered, pizzaDelivered, mlRecursion):
        #read file data
        readFile = open(OUTPUT_TXT, "r")
        content = readFile.read()
        #write file data
        folderPath = "Outputs/" + "DataSet_" + dataSet + "/"
        fileName = "Output_DataSet_" + dataSet + "_" + str(score) + "_" + teamDelivered + "_" + pizzaDelivered + "_ML_" + mlRecursion + ".txt"
        writeFile = open(folderPath + fileName, "w")
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
        return self._teamCount[0] + self._teamCount[1] + self._teamCount[2]

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



dp = DataPrebs()
