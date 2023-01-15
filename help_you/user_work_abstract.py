from abc import ABC, abstractmethod

class UserWork(ABC):
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def show_all(self):
        pass

    @abstractmethod
    def show_one(self):
        pass

    @abstractmethod
    def show_page(self):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def delete_one(self):
        pass

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        pass

    @abstractmethod
    def edit_information(self):
        pass
    
    @abstractmethod
    def edit_name(self):
        pass

    @abstractmethod
    def search_in(self):
        pass

    @abstractmethod
    def add_values(self):
        pass
