import numpy as np

def LoadData(text):
  my_file = open(text, "r")
  content = my_file.read()
  content_list = content.split("\n")
  my_file.close()
  return content_list;

datalist = LoadData("Inputs/Raw_DataSets/c_many_ingredients.in")

def GetIngredient():
    res = []
    for data in datalist[1:]:
        ingredientlist = data.split(" ")
        [res.append(x) for x in ingredientlist[1:] if x not in res]
    return res

ingredientList = GetIngredient()

def GetPizzaDataList(ingredientList):
  pizzaList = []
  for data in datalist[1:]:
    pizza = data.split(" ")
    ingredientData = 0
    for ingredient in pizza[1:]:
      ingredientData += pow(2, ingredientList.index(ingredient))
    pizzaList.append(("{0:0" + str(len(ingredientList)) + "b}").format(ingredientData))
    # print(("{0:0" + str(len(ingredientList)) + "b}").format(ingredientData))
  return pizzaList

pizzaList = GetPizzaDataList(ingredientList) #return list of PizzaData
print(len(ingredientList))