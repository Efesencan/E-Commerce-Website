import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from .models import Category
#"from online_store.pageRankings import *
class Ranking:
    def __init__(self):
        self.path = "rankings"

    def readFile(self):
        try :
            data = default_storage.open(self.path)
            return json.load(data)
        except:
            categoryNames = Category.objects.values("categoryName")
            categoryNames = [i["categoryName"] for i in categoryNames]
            #print(categoryNames)
            initial_dict = {"default":categoryNames}
            fileContent = json.dumps(initial_dict)

            default_storage.save(self.path, ContentFile(fileContent))
            

    def writeFile(self,data):
        default_storage.delete(self.path)
        default_storage.save(self.path, ContentFile(json.dumps(data)))

    def GetRanking(self,target):
        try:
            data = self.readFile()
            return data[target]
        except:
            return None

    def NewRanking(self,target,targetlist,end,begin,gender):
        data = self.readFile()
        data[target]= self.Validate(targetlist)
        data[target] = {"data": targetlist , "end":end,"begin":begin,"gender":gender}
        self.writeFile(data)
    def DeleteRanking(self,target):
        try:
            if target != "default":
                data = self.readFile()
                del data[target]
                self.writeFile(data)
        except:
            pass
    def AddCategory(self,categoryName):
        data = self.readFile()
        for key,value in data.items():
            value.append(categoryName)
        self.writeFile(data)
    def DeleteCategory(self,categoryName):
        try:
            data = self.readFile()
            for key,value in data.items():
                value.remove(categoryName)
            self.writeFile(data)
        except:
            pass
    
    def Validate(self,data):
        default = self.GetRanking("default")
        for i in data:
            if i not in default:
                raise NameError('Not correct Ranking ' + i + ' not a category')
                break
        
        else:
            return data