
from frictionless.resources import TableResource

def frictionless_table_infer(fn):
    resource = TableResource(
        path=fn)
    resource.infer(stats=True)
    print(resource)
    return resource

if __name__ == '__main__':

    # Inspect CSV
    fn_data = 'data/2025-05-05_Ariadne2_Data_v1.0_data.csv'
    frictionless_table_infer(fn_data)
