import graphene
from app.resolvers import resolve_users, resolve_user, resolve_products, resolve_product, resolve_orders, resolve_order, resolve_user_profile
from app.resolvers import register_user, create_product, place_order, login_user
from app.types import UserType, ProductType, OrderType, RegisterInput, LoginInput, ProductInput, OrderInput

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user_profile = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int(required=True))
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    def resolve_users(self, info):
        return resolve_users(info)

    def resolve_user(self, info, id):
        return resolve_user(id,info)
    
    def resolve_user_profile(self, info):
        return resolve_user_profile(info) 

    def resolve_products(self, info):
        return resolve_products()

    def resolve_product(self, info, id):
        return resolve_product(id, info)

    def resolve_orders(self, info):
        return resolve_orders(info)

    def resolve_order(self, info, id):
        return resolve_order(id)

class Mutation(graphene.ObjectType):
    register_user = graphene.Field(UserType, input=RegisterInput())
    login_user = graphene.Field(graphene.String, input=LoginInput())  
    create_product = graphene.Field(ProductType, input=ProductInput())
    place_order = graphene.Field(OrderType, input=OrderInput())

    def resolve_register_user(self, info, input):
        return register_user(input)
    
    def resolve_login_user(self, info, input):
        return login_user(input) 
    
    def resolve_create_product(self, info, input):
        return create_product(input,info)

    def resolve_place_order(self, info, input):
        return place_order(input, info)

schema = graphene.Schema(query=Query, mutation=Mutation)
