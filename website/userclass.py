


class User:
    def __init__(self , id , usrname , password):
        self.id = id
        self.usrname = usrname
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.id},{self.usrname},{self.password} >'
