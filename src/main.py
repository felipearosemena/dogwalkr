import graphene
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.graphql import GraphQLApp

from graphene_pydantic import PydanticObjectType

from src.services.dogs.schema import Dog, DogsResponse
from src.services.users.schema import User, UsersResponse
from src.services.toys.schema import Toy, ToysResponse
from src.services.common.db import engine
from src.services.common.models import Base
from src.services.common.schema import Meta
from src.services.dogs.db import DogsContextManager, DogDAO
from src.services.users.db import UsersContextManager, UserDAO
from src.services.toys.db import ToysContextManager, ToyDAO

app = FastAPI()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/dogs/", response_model=DogsResponse)
def get_dogs():
    with DogsContextManager() as manager:
        results, count = manager.get_dogs(name="test")
        return DogsResponse(
            meta=Meta(total=count), dogs=[Dog.from_orm(result) for result in results]
        )


@app.get("/users/", response_model=UsersResponse)
def get_users():
    with UsersContextManager() as manager:
        results, count = manager.get_users(user_id=1)
        return UsersResponse(
            meta=Meta(total=count), users=[User.from_orm(result) for result in results]
        )


@app.get("/toys/", response_model=ToysResponse)
def get_toys():
    with ToysContextManager() as manager:
        results, count = manager.get_toys(toy_id=1)
        return ToysResponse(
            meta=Meta(total=count), users=[Toy.from_orm(result) for result in results]
        )


class UserType(PydanticObjectType):
    class Meta:
        model = User


class DogType(PydanticObjectType):
    class Meta:
        model = Dog

class ToyType(PydanticObjectType):
    class Meta:
        model = Toy

class Query(graphene.ObjectType): 
    user = graphene.Field(UserType, user_id=graphene.Int())
    dogs = graphene.List(DogType, owner_id=graphene.Int())
    toys = graphene.List(ToyType, dog_owner_id=graphene.Int())

    def resolve_user(self, info, user_id):
        with UsersContextManager() as manager:
            results, count = manager.get_users(user_id)
            first_user = results[0]
            return User.from_orm(first_user)

    def resolve_dogs(self, info, owner_id):
        with DogsContextManager() as manager:
            results, count = manager.get_dogs(owner_ids=[owner_id])
            return [Dog.from_orm(result) for result in results]

    def resolve_toys(self, info, dog_owner_id):
        with ToysContextManager() as manager:
            results, count = manager.get_toys(owner_ids=[dog_owner_id])
            return [Toy.from_orm(result) for result in results]
            

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))