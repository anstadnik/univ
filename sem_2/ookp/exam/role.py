class Role():

    """This class represents the role"""

    def __init__(self, *, name:str, add_role:bool, del_role:bool, add_user:bool, del_user:bool,
                 add_f:bool, view_f:bool, edit_f:bool, del_f:bool):
        """Create role with permissions """
        self.name = name
        self.add_role = add_role
        self.del_role = del_role
        self.add_user = add_user
        self.del_user = del_user
        self.add_f = add_f
        self.view_f = view_f
        self.edit_f = edit_f
        self.del_f = del_f
