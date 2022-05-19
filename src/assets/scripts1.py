    def subjectNow3(self):
        subject = "Details in Short Stories or Poems"
        self.subject_Title.setText(subject)
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.updateScreen("Stories and Poems")
        self.speak("Are you familiar with short stories and poems?")
        
        self.speak("You've possibly read and listened to different stories and poems,")
        self.updateScreen("fairy tales and other bedtime stories.")
        self.speak("such as fairy tales and other bedtime stories.")
        
        self.updateScreen("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        self.speak("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        self.speak("Now. Listen to this story,")
        self.updateScreen("The New Toys")
        self.speak("The New Toys")
        
        self.updateScreen("The New Toys\n Jay and Joy have new toys. \n Jay has a new toy car. It is small but shiny.\n Meanwhile,Joy has a new doll. It is big and beautiful.\n She hid them behind the table to surprise them.\n They hurriedly looked for the hidden gifts.\n When they saw them, they immediately opened them.\n They jumped for joy when they saw their new toys. They were just what they wished for.\n They thanked andkissed their Tita. They love their new toys.") 
        self.speak("The New Toys. Jay and Joy have new toys.")
        self.speak("Jay has a new toy car. It is small but shiny.")
        self.speak("Meanwhile,Joy has a new doll. It is big and beautiful.")
        self.speak("She hid them behind the table to surprise them.")
        self.speak("They hurriedly looked for the hidden gifts.")
        self.speak("When they saw them, they immediately opened them.")
        self.speak("They jumped for joy when they saw their new toys. They were just what they wished for.")
        self.speak("They thanked andkissed their Tita. They love their new toys.")
        
        
        self.speak("Try to answer these questions")
        self.speak("Who received gifts during their birthday?")
        while True:
                response = ask_ettibot().lower()     
                if response == "Jay and Joy":
                    self.speak("Perfect!")
                    self.updateScreen("Perfect")
                    self.countResponse()
                    break
                
         self.speak("Who gave them the gifts?")
        while True:
                response = ask_ettibot().lower()     
                if response == "Tita":
                    self.speak("Perfect!")
                    self.updateScreen("Perfect")
                    self.countResponse()
                    break
                
        self.speak("Where did she hide the gifts?")
        while True:
                response = ask_ettibot().lower()     
                if response == "table":
                    self.speak("Perfect!")
                    self.updateScreen("Perfect")
                    self.countResponse()
                    break
                
        self.speak("What gifts did they receive?")
        while True:
                response = ask_ettibot().lower()     
                if response == "toy car and doll":
                    self.speak("Perfect!")
                    self.updateScreen("Perfect")
                    self.countResponse()
                    break
                
        self.speak("What did they do when they found the gifts?")
        while True:
                response = ask_ettibot().lower()     
                if response == "jumped":
                    self.speak("Perfect!")
                    self.updateScreen("Perfect")
                    self.countResponse()
                    break
                
                
        self.speak("That's all for today's video, thank you for listening!")
        self.close()
