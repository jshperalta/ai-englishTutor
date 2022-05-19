    def subjectNow4(self):
        subject = "Polite Expressions"
        self.subject_Title.setText(subject)
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.updateScreen("Politeness")
        self.speak("Politeness is one of the characteristics that you should have.")
        
        self.speak("There are lots of ways on how one can show politeness.")
        self.speak("Saying,")
        self.updateScreen("po and opo")
        self.speak("po and opo is one of these ways. Also, you can show politeness using appropriate words or expressions in different events.")
        
        self.speak("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        self.updateScreen("The New Toys")
        self.speak("Now.. Read this story. The New Toys. You may also listen to it by asking your parents or guardian to read it for you.")
    
    
        self.speak("Who received gifts during their birthday?")
        self.speak("Who gave them the gifts?")
        self.speak("Where did she hide the gifts?")
        self.speak("What gifts did they receive?")
        self.speak("What did they do when they found the gifts?")
    
        self.speak("That's all for today's video, thank you for listening!")
        self.close()