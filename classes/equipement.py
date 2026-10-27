from pydantic import BaseModel ,EmailStr, Field
import datetime as dt


class Equipement(BaseModel):
   """

   """
   id: int              #INT NOT NULL AUTO_INCREMENT,
   nom: str             #VARCHAR(100) NOT NULL,
   description: str     #VARCHAR(255),
   # PRIMARY KEY(id)
