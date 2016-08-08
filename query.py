"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Part 2: Write queries


# Get the brand with the **id** of 8.
Brand.query.get(8)

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
Model.query.filter(Model.name == 'Corvette', 
                   Model.brand_name == 'Chevrolet').all()

# Get all models that are older than 1960.
Model.query.filter(Model.year > 1960).all()

# Get all brands that were founded after 1920.
Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor".
Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
Brand.query.filter(Brand.discontinued.is_(None)).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded 
# before 1950.
Brand.query.filter((Brand.discontinued.is_(None)) | (Brand.founded < 1950)).all()

# Get any model whose brand_name is not Chevrolet.
Model.query.filter(Model.brand_name != 'Chevrolet').all()


# Fill in the following functions. (See directions for more info.)

def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''
    
    # List of tuples of Model objects and Brand objects, filtered by model year.
    models = db.session.query(Model, Brand).outerjoin(Brand).filter(Model.year == year).all()

    for model, brand in models:
        # When the model's brand is in the brands table, it will have HQ info.
        if brand is not None:
            print model.name, model.brand_name, brand.headquarters
        else:
            print model.name, model.brand_name, "HQ is not listed."


def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
     using only ONE database query.'''

    brands = db.session.query(Brand, Model).outerjoin(Model).filter(Brand.name == Model.brand_name).all()

    brand_to_model = {}

    for brand, model in brands:
        current_brand = brand.name

        if current_brand in brand_to_model:
            # If the model is not in value list, add it, and reset values to key.
            if model.name not in brand_to_model[current_brand]:
                current_models = brand_to_model[current_brand]
                current_models.append(model.name)
                brand_to_model[current_brand] = current_models
        else:
            brand_to_model[current_brand] = [model.name]

    print brand_to_model




# -------------------------------------------------------------------
# Part 2.5: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
    # The datatype is a query object (a SQLAlchemy query object). 
    # The returned value will be where the query object is in memory.
    # It will not return Brand objects or their repr descriptions for 
    # Brand objects where the row has 'Ford' in the 'name' column in the 
    # brands table.

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
    # An association table is the way to manage the many to many relationship
    # between two other tables. It generally doesn't contain any meaningful data
    # other than the relationship between the two other tables.  The association
    # table helps navigate from one table to the other table. 

    # For example, for students and classes, students may take many classes, 
    # and classes can have many students.  An association table may hold
    # the class id and the student id, so we can navigate which students 
    # are in which classes.

# -------------------------------------------------------------------
# Part 3

def search_brands_by_name(mystr):
    """Returns list of brand objects which partially or fully contains the string parameter."""

    query = Brand.query.filter(Brand.name.like("%" + mystr + "%")).all()

    return query


def get_models_between(start_year, end_year):
    """Returns list of model objects between start (inclusive) and end (exclusive) years."""

    query = Model.query.filter((Model.year >= start_year) & (Model.year < end_year)).all()

    return query
