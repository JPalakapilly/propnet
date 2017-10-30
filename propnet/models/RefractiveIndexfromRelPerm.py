from propnet.core.models import AbstractModel, validate_evaluate

class RefractiveIndexfromRelPerm(AbstractAnalyticalModel):

    @property
    def title(self):
        return "Relate Refractive Index with relative permittivity and relative permeability of a material."

    @property
    def tags(self):
        return ["stub"]

    @property
    def description(self):
        return """
        The refractive index is the geometric mean of the relative permittivity and the relative permeability.
        """

    @property
    def references(self):
        return []

    @property
    def symbol_mapping(self):
        return {
            'n': 'refractive index',
            'Ur': 'relative_permittivity',
            'Er': 'relative_permeability'

        }

    @property
    def assumption_mapping(self):
        return None

    @property
    def required_conditions(self):
        return None

    # @property
    # def connections(self):
    #     return {
    #         'n': {'Ur', 'Er'},
    #         'Ur': {'n', 'Er'},
    #         'Er': {'n', 'Ur'}
    #     }



    @property
    def test_sets(self):
        return {}

    @property
    def equations(self):
        return ["n - sqrt(Ur*Er)"]
