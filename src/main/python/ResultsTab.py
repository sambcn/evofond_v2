from Tab import Tab

class ResultsTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Résultats", tabBar.getResource("images\\results.png"))
        