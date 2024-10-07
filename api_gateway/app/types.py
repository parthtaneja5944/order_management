import graphene

class UserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    address = graphene.String()

class ProductType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    price = graphene.Float()
    inventory = graphene.Int()
    description = graphene.String()

class ProductOrderType(graphene.ObjectType):
    product_id = graphene.Int()
    quantity = graphene.Int()

class OrderType(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.Int()
    products = graphene.List(ProductOrderType)

class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    address = graphene.String(required=True)
    type = graphene.String(required=True)

class LoginInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    description = graphene.String(required=True)
    inventory = graphene.Int(required=True)

class ProductOrderInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)

class OrderInput(graphene.InputObjectType):
    user_id = graphene.Int(required=True)
    products = graphene.List(ProductOrderInput)
