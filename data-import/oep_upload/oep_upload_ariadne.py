
from frictionless.resources import TableResource
from frictionless import Schema, fields

def frictionless_table_infer(fn):
    resource = TableResource(
        path=fn)
    resource.infer(stats=True)
    print(resource)

    return resource


def frictionless_resource_fields(resource):
    # https://framework.frictionlessdata.io/docs/framework/schema.html?query=fields



if __name__ == '__main__':

    # Inspect CSV
    fn_data = 'data/2025-05-05_Ariadne2_Data_v1.0_data.csv'
    resource = frictionless_table_infer(fn_data)

    # Convert schema.field to
    fields =