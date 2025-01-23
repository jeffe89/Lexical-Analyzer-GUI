########################################################################
#
#                           	FINAL PROJECT
#                             Geoffrey Giordano
#
#           TREE SOURCE: IMPORTED TREELIB AND MANUALLY MADE TREE USING
#                        TREELIB LIBRARY FUNCTIONS
#
########################################################################

from tkinter import *
from tkinter import ttk
# IMPORTING TREELIB FOR CONSOLE TREE
from treelib import Node, Tree
import tkinter.messagebox
import re


# Class Definition: A Graphical User Interface for a lexical analyzer forTinyPie
class LexerGui:
    
    #Index variable
    index = 0
    
    #Parser Counter
    pCount = 1
    
    #Regex expressions
    ##		=   +	>	*
    myregOp = re.compile(r'\=|\+|\>|\*')

    ##		if	else  int	float
    myregKey = re.compile(r'if|else|int|float')

    ##		(	)	:	"	;
    myregSep = re.compile(r'\(|\)|\:|\;')

    ##		test, test123, checkVal
    myregIden = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')

    ##		Only Strings
    myregLitStr = re.compile(r'(\")(.+)(\")')

    ##		Only Integers, floats
    myregLitInt = re.compile(r'\d+')
    
    ##		Only floats
    myregLitFloat = re.compile(r'\d+\.\d+')
    
    def __init__(self, root):
        #Create Main window for GUI display
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")
        self.master.geometry('1000x675')
        self.master.resizable(False, False)
        with open('tree.txt', 'w') as f:
            f.write("Data tree text file:")
            f.write("\n\n")
            
        #Create treelib tree for console printout and counters
        self.pTree = Tree()
        self.viewTree = ttk.Treeview(root, columns=("parent","token_id", "type_token"), show="headings")
        self.viewTree.heading("parent", text="Parent")
        self.viewTree.heading("token_id", text="ID")
        self.viewTree.heading("type_token", text="Type/Token")
        self.expCount = self.mathCount = self.multiCount = self.ifCount = self.printCount = self.compCount = 0
        self.opCount = self.keyCount = self.sepCount = self.idenCount = self.strCount = self.intCount = self.floatCount = self.tokenCount = 0
        
        #Create Labels for each statement needed.
        self.label1 = Label(self.master, text="Source Code", font=(12))
        self.label2 = Label(self.master, text="Tokens", font=(12))
        self.label3 = Label(self.master, text="Current Processing Line:", font=(12))
        self.label4 = Label(self.master, text="Parse Tree", font =(12))
        self.label5 = Label(self.master, text="Treelib Data Tree", font =(12))
        self.label6 = Label(self.master, text="Treeview Graphical Display", font =(12))
        
        #Positioning Labels
        self.label1.grid(row=0,column=0, columnspan = 3,sticky=W, padx=15, pady= 5)
        self.label2.grid(row=0,column=2, columnspan = 3,sticky=W, padx=5, pady= 5)
        self.label3.grid(row=4,column=0,sticky=W, padx=20, pady= 5) 
        self.label4.grid(row=0,column=4, columnspan = 3,sticky=W, padx=15, pady= 5)
        self.label5.grid(row=2,column=0, columnspan = 3,sticky=W, padx=15, pady= 5)
        self.label6.grid(row=2,column=2, columnspan = 3,sticky=W, padx=35, pady= 5)
        
        #Create two windows for text. One for input and another for output
        self.inputText = Text(self.master, width = 35, height = 15) 
        self.outputText = Text(self.master, width = 35, height = 15)
        self.parserText = Text(self.master, width = 48, height = 15)
        self.treeDisplay = Text(self.master, width = 25, height = 17, padx=10)
        self.treeViewDisplay = Text(self.master, width = 25, height = 17)
        self.inputText.grid(row=1,column=0, columnspan = 2, sticky=W+E, padx=10)
        self.outputText.grid(row=1,column=2, columnspan = 2, sticky=W+E, padx=0)
        self.parserText.grid(row=1,column=4, columnspan = 2, sticky=W+E, padx=10)
        self.treeDisplay.grid(row=3,column=0, columnspan = 2, sticky=W+E, padx=10)
        self.viewTree.grid(row=3, column=2, columnspan = 4, sticky=W+E, padx=25)
        
        #Create window for processing line and counter
        self.processLine = Text(self.master, width=4 , height=1)
        self.processLine.grid(row=4,column=1, sticky=E)
        self.processLine.insert(INSERT, "   " + str(self.index))
        
        #Create two buttons. One for Next Line and One for Quit
        self.nextButton = Button (self.master, text="    Next Line    ", command=self.nextline)
        self.quitButton = Button (self.master, text="        Quit        ", command=self.quit)
        self.nextButton.grid(row=5,column=0, columnspan = 2, sticky=E)
        self.quitButton.grid(row=5,column=5, columnspan = 2, sticky=E, padx=10)
       
    def nextline(self):
        ##Copy input line by line and display in output
        code = self.inputText.get("1.0", "end").splitlines()
        
        global tokenList
        
        ##Update Processor Line Count
        self.processLine.delete("1.0", "2.0")
        self.processLine.insert(END, "   " + str(self.index+1))
        self.treeDisplay.delete("1.0", "end")
        self.outputText.delete("1.0", "end")
        self.parserText.delete("1.0", "end")
        
        for item in self.viewTree.get_children():
            self.viewTree.delete(item)
        
        ##Check to see if index has surpased amount of lines
        if (self.index < len(code)):
            #gather first string of list and use for function call
            line = code[self.index]
            tokenList = self.CutOneLineTokens(line)
            ##Update output text 
            for x in tokenList:
                self.outputText.insert(END, x)
                self.outputText.insert(END, "\n\n")
            self.index +=1
        else:
            self.inputText.delete("1.0", "end")
            self.outputText.delete("1.0", "end")
            self.parserText.delete("1.0", "end")
            self.index = 0
            self.processLine.delete("1.0", "2.0")
            self.processLine.insert(END, "   " + str(self.index))
            self.treeDisplay.delete("1.0", "end")
            self.pCount = 1
            with open('tree.txt', 'w') as f:
                f.write("Data tree text file")
                f.write("\n")
        
        self.parser(tokenList)
        
        if(self.pTree.size() != 0):
            print("####Parse tree for line " + str(self.pCount - 1) + "####")
            print(self.pTree.show(stdout=False))
            #self.pTree.save2file('tree.txt')
            with open('tree.txt', 'w') as f:
                self.pTree.save2file('tree.txt')
            with open('tree.txt', 'r', encoding='utf-8-sig') as f:
                contents = f.read()
            self.treeDisplay.insert("1.0", contents)
            
            #Graphical Tree Output
            self.tList = self.pTree.all_nodes()
            treeInfo = []
            for node in self.tList:
                treeInfo.append((node.predecessor(self.pTree.identifier), node.identifier, node.tag))
            
            for tup in treeInfo:
                self.viewTree.insert('', END, values=tup)
            
            self.viewTree.bind('<<TreeviewSelect>>', self.item_selected())
            self.pTree = Tree()
    
    def item_selected(self):
        for selected_item in self.viewTree.selection():
            item = self.viewTree.item(selected_item)
            record = item['values']
            showinfo(title='Information', message=','.join(record))
    
    def quit(self):
        self.master.destroy()
        print("Quitting Lexical Analyzer For TinyPie...")

    def CutOneLineTokens(self, line):
        ##Return list with formatted output
        returnList = []
    
        ##While loop until input line of code is fully read
        while (line != ""):
        
            #Check and remove white spaces
            line = line.lstrip()
        
            #Check for keyword first
            result = self.myregKey.match(line)
            if (result != None):
                returnList.append("<Keyword, " + result.group() + ">")
                line = line[result.end():]
            
            #Check for Separator next
            result = self.myregSep.match(line)
            if (result != None):
                returnList.append("<Separator, " + result.group() + ">")
                line = line[result.end():]
            
            #Check for String Literal if quotation mark	
            result = self.myregLitStr.match(line)
            if (result != None):
                returnList.append("<Separator, " + line[0:1] + ">")
                returnList.append("<String Literal, " + line[result.start() + 1:result.end() - 1] + ">")
                returnList.append("<Separator, " + line[result.end() - 1:result.end()] + ">")
                line = line[result.end():]
            
            #Check for Identifier next
            result = self.myregIden.match(line)
            if (result != None):
                returnList.append(("<Identifier, " + result.group() + ">"))
                line = line[result.end():]
            
            #Check for Operator next
            result = self.myregOp.match(line)
            if (result != None):
                returnList.append(("<Operator, " + result.group() + ">"))
                line = line[result.end():]
                
            #Check for Float Literal
            result = self.myregLitFloat.match(line)
            if (result != None):
                returnList.append("<Float, " + result.group() + ">")
                line = line[result.end():]
                
            #Check for Integer Literal
            result = self.myregLitInt.match(line)
            if (result != None):
                returnList.append("<Integer, " + result.group() + ">")
                line = line[result.end():]

        ##Return formatted output
        return returnList
        
    def accept_token(self, tokenList):
        global inToken
        self.parserText.insert(END, "\nAccepting Token: " + inToken[1] + "\n")
        if(len(tokenList) == 0):
            return
        listPop = tokenList.pop(0)
        listPop = listPop[1:-1]
        listTuple = tuple(map(str, listPop.split(', ')))
        inToken = listTuple
    
    def multi(self, tokenList):
        self.multiCount += 1
        self.pTree.create_node("Multi", "multi" + str(self.multiCount), parent = "math" + str(self.mathCount))
        self.parserText.insert(END, "\nParent Node: Multi\nFinding children nodes...\n")
        global inToken

        typeT,token = inToken
        if(inToken[0]=="Float"):
            self.floatCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Float Lit")
            self.parserText.insert(END, "\nFloat Lit has child node (token): " + token)
            self.pTree.create_node("Float", "floatlit" + str(self.floatCount), parent="multi" + str(self.multiCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="floatlit" + str(self.floatCount))
            self.accept_token(tokenList)
        
        elif(inToken[0]=="Integer"):
            self.intCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Integer Lit")
            self.parserText.insert(END, "\nInteger Lit has child node (token): " + token)
            self.pTree.create_node("Integer", "intlit" + str(self.intCount), parent="multi" + str(self.multiCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="intlit" + str(self.intCount))
            self.accept_token(tokenList)
            typeT,token = inToken
            if (inToken[1]=="*"):
                self.opCount += 1
                self.tokenCount += 1
                self.parserText.insert(END, "\nChild Node (internal): Operator")
                self.parserText.insert(END, "\nOperator has child node (token): " + token)
                self.pTree.create_node("Operator", "op" + str(self.opCount), parent="multi" + str(self.multiCount))
                self.pTree.create_node(token, token + str(self.tokenCount), parent="op" + str(self.opCount))
                self.accept_token(tokenList)
                self.multi(tokenList)
            else:
                if(inToken[1]=="+"):
                    return
                self.parserText.insert(END, "\nExpect '*' operator after int")
                return
        else:
            self.parserText.insert(END, "\nExpect 'float' or 'int' literal")
            return
        
    def math(self, tokenList):
        self.mathCount += 1
        self.pTree.create_node("Math", "math" + str(self.mathCount), parent = "exp" + str(self.expCount))
        self.parserText.insert(END, "\nParent Node: Math\nFinding children nodes...\n")
        global inToken
        
        self.parserText.insert(END, "\nChild Node (internal): Multi")
        self.multi(tokenList)
        
        typeT,token = inToken
        if(inToken[1]=="+"):
            self.opCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nParent Node: Math\nFinding children nodes...\n")
            self.parserText.insert(END, "\nChild node (internal): Operator")
            self.parserText.insert(END, "\nOperator has child node (token): " + token)
            self.pTree.create_node("Operator", "op" + str(self.opCount), parent="math" + str(self.mathCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="op" + str(self.opCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect '+' operator after multi")
            return
        
        self.parserText.insert(END, "\nChild Node (internal): Multi")
        self.multi(tokenList)
    
    def comparison_exp(self, tokenList):
        self.compCount += 1
        self.pTree.create_node("Comparison Expression", "compexp" + str(self.compCount), parent = "ifexp" + str(self.ifCount))
        self.parserText.insert(END, "\nParent Node: Comparison_Exp\nFinding children nodes...\n")
        global inToken
        
        typeT,token=inToken
        if(typeT=="Identifier"):
            self.idenCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Identifier")
            self.parserText.insert(END, "\nIdentifier has child node (token): " + token)
            self.pTree.create_node("Identifier", "iden" + str(self.idenCount), parent="compexp" + str(self.compCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="iden" + str(self.idenCount))
            self.accept_token(tokenList)
            typeT,token=inToken
            if(token==">"):
                self.opCount += 1
                self.tokenCount += 1
                self.parserText.insert(END, "\nChild Node (internal): Operator")
                self.parserText.insert(END, "\nOperator has child node (token): " + token)
                self.pTree.create_node("Operator", "op" + str(self.opCount), parent="compexp" + str(self.compCount))
                self.pTree.create_node(token, token + str(self.tokenCount), parent="op" + str(self.opCount))
                self.accept_token(tokenList)
                typeT,token=inToken
                if(typeT=="Identifier"):
                    self.idenCount += 1
                    self.tokenCount += 1
                    self.parserText.insert(END, "\nChild Node (internal): Identifier")
                    self.parserText.insert(END, "\nIdentifier has child node (token): " + token)
                    self.pTree.create_node("Identifier", "iden" + str(self.idenCount), parent="compexp" + str(self.compCount))
                    self.pTree.create_node(token, token + str(self.tokenCount), parent="iden" + str(self.idenCount))
                    self.accept_token(tokenList)
                else:
                    self.parserText.insert(END, "\nExpect ident. for comparison")
                    return
            else:
                self.parserText.insert(END, "\nExpect '>' operator after ident.")
                return
        else:
            self.parserText.insert(END, "\nExpect ident. for comparison")
            return
        return
    
    def if_exp(self, tokenList):
        self.ifCount += 1
        self.pTree.create_node("If Expression", "ifexp" + str(self.ifCount), parent = "exp" + str(self.expCount))
        self.parserText.insert(END, "\nParent Node: If_Exp\nFinding children nodes...\n")
        global inToken
        
        typeT,token=inToken
        if(token=="if" or token=="else"):
            self.keyCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Keyword")
            self.parserText.insert(END, "\nKeyword has child node (token): " + token)
            self.pTree.create_node("Keyword", "key" + str(self.keyCount), parent="ifexp" + str(self.ifCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="key" + str(self.keyCount))
            if(token=="else"):
                self.accept_token(tokenList)
                typeT,token=inToken
                if(token==":"):
                    self.sepCount += 1
                    self.tokenCount += 1
                    self.parserText.insert(END, "\nChild Node (internal): Separator")
                    self.parserText.insert(END, "\nSeparator has child node (token): " + token)
                    self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="ifexp" + str(self.ifCount))
                    self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
                    return
                else:
                    self.parserText.insert(END, "\nExpect ':' to end the line")
                    return
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect 'if' keyword at begin of line")
            return
        
        typeT,token=inToken
        if(token=="("):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="ifexp" + str(self.ifCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect '(' sep. before statement")
            return
        
        typeT,token=inToken
        self.parserText.insert(END, "\nChild Node (internal): Comparison_Exp")
        self.comparison_exp(tokenList)
        
        typeT,token=inToken
        if(token==")"):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="ifexp" + str(self.ifCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect ')' sep. after statement")
            return
        
        typeT,token=inToken
        if(token==":"):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="ifexp" + str(self.ifCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            return
        else:
            self.parserText.insert(END, "\nExpect ':' to end the line")
            return
    
    def print_exp(self, tokenList):
        self.printCount += 1
        self.pTree.create_node("Print Expression", "printexp" + str(self.printCount), parent = "exp" + str(self.expCount))
        self.parserText.insert(END, "\nParent Node: Print_Exp\nFinding children nodes...")
        global inToken
        
        typeT,token=inToken
        if(token=="print"):
            self.idenCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Identifier")
            self.parserText.insert(END, "\nIdentifier has child node (token): " + token)
            self.pTree.create_node("Identifier", "iden" + str(self.idenCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="iden" + str(self.idenCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect 'print' at begin of line")
            return
        
        typeT,token=inToken
        if(token=="("):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect '(' sep. before quote")
            return
        
        typeT,token=inToken
        if(token=='"'):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, '\nExpect " sep. before string lit')
            return
        
        typeT,token=inToken
        if(typeT=="String Literal"):
            self.strCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): String Lit")
            self.parserText.insert(END, "\nString Lit has child node (token): " + token)
            self.pTree.create_node("String Literal", "strlit" + str(self.strCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="strlit" + str(self.strCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect string lit. after quote")
            return
        
        typeT,token=inToken
        if(token=='"'):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, '\nExpect " sep. after string lit.')
            return
        
        typeT,token=inToken
        if(token==")"):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect ')' sep. after quote")
            return
        
        typeT,token = inToken
        if(inToken[1]==";"):
            self.sepCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            self.pTree.create_node("Separator", "sep" + str(self.sepCount), parent="printexp" + str(self.printCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="sep" + str(self.sepCount))
            return
        else:
            self.parserText.insert(END, "\nExpect ';' to end the line")
            return
    
    def exp(self, tokenList):
        self.expCount += 1
        self.pTree.create_node("Expression", "exp" + str(self.expCount))
        global inToken
        
        typeT,token=inToken
        if(token=="if"):
            self.if_exp(tokenList)
            return
        elif(token=="else"):
            self.if_exp(tokenList)
            return
            
        typeT,token=inToken
        if(token=="print"):
            self.print_exp(tokenList)
            return
                
        self.parserText.insert(END, "\nParent Node: Exp\nFinding children nodes...\n")
        typeT,token=inToken
        if(typeT=="Keyword"):
            self.keyCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Keyword")
            self.parserText.insert(END, "\nKeyword has child node (token): " + token)
            self.pTree.create_node("Keyword", "key" + str(self.keyCount), parent="exp" + str(self.expCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="key" + str(self.keyCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect keyword 'int' or 'float'")
            return
            
        typeT,token = inToken
        if(typeT=="Identifier"):
            self.idenCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Identifier")
            self.parserText.insert(END, "\nIdentifier has child node (token): " + token)
            self.pTree.create_node("Identifier", "iden" + str(self.idenCount), parent="exp" + str(self.expCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="iden" + str(self.idenCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect ident. after keyword")
            return
            
        typeT,token = inToken
        if(token=="="):
            self.opCount += 1
            self.tokenCount += 1
            self.parserText.insert(END, "\nChild Node (internal): Operator")
            self.parserText.insert(END, "\nOperator has child node (token): " + token)
            self.pTree.create_node("Operator", "op" + str(self.opCount), parent="exp" + str(self.expCount))
            self.pTree.create_node(token, token + str(self.tokenCount), parent="op" + str(self.opCount))
            self.accept_token(tokenList)
        else:
            self.parserText.insert(END, "\nExpect '=' after ident.")
            return
            
        typeT,token = inToken
        self.parserText.insert(END, "\nChild Node (internal): Math")
        self.math(tokenList)
        
        typeT,token = inToken
        if(inToken[1]==";"):
            self.parserText.insert(END, "\nChild Node (internal): Separator")
            self.parserText.insert(END, "\nSeparator has child node (token): " + token)
            return
        else:
            self.parserText.insert(END, "\nExpect ';' to end the line")
            return
    
    def parser(self, tokenList):
        global inToken
        if(len(tokenList) == 0):
            return
        listPop = tokenList.pop(0)
        listPop = listPop[1:-1]
        listTuple = tuple(map(str, listPop.split(', ')))
        inToken= listTuple
        
        if(self.pCount == 1):
            self.parserText.insert(END, "####Parse tree for line " + str(self.pCount) + "####")
            self.outputText.insert(1.0, "####Token List for line " + str(self.pCount) + "####\n")
            self.exp(tokenList)
            if(inToken[1]==";" or inToken[1]==":"):
                self.parserText.insert(END, "\n\nParse tree building success!")
            self.pCount += 1
            return
        else:
            self.parserText.insert(END, "####Parse tree for line " + str(self.pCount) + "####")
            self.outputText.insert(1.0, "####Token List for line " + str(self.pCount) + "####\n")
            self.exp(tokenList)
            if(inToken[1]==";" or inToken[1]==":"):
                self.parserText.insert(END, "\n\nParse tree building success!")
            self.pCount += 1
            return

if __name__ == '__main__':
    myTkRoot = Tk() 
    my_gui = LexerGui(myTkRoot)
    myTkRoot.mainloop()
