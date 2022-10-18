from front.Tab import Tab

class ModelTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Modèle", tabBar.getResource("images\\form.jpg"))
        