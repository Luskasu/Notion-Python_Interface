from dataclasses import dataclass

@dataclass
class User:
    id : str
    type : str
    name : str
    avatar_url : str
    
@dataclass
class Block:
    id : str
    parent_id : str
    created_time : str
    last_edited_time : str
    created_by : str
    last_edited_by: str
    has_children : bool
    archived : bool
    in_trash : bool
    type : str
    content : str

    def __str__(self) -> str:
        return f"____________________________________\n{self.content}\nid: {self.id}\nparent_id : {self.parent_id},\ncreated_time : {self.created_time},\nlast_edited_time : {self.last_edited_time},\ncreated_by : {self.created_by},\nlast_edited_by : {self.last_edited_by},\nhas_children : {self.has_children},\narchived : {self.archived},\nin_trash : {self.in_trash},\ntype : {self.type},\n"
    

    
    