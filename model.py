
class Content(object):
    def __init__(self, category="", name="", link="", price=None, sale=None, availability=None):
        self.category = category
        self.name = name
        self.link = link
        self.price = price if price else 0
        self.sale = sale if sale else "Нет скидки"
        self.availability = availability if availability else "В наличии"


    def __str__(self):
        return f"{self.category},{self.name},{self.link},{self.price},{self.sale},{self.availability}"