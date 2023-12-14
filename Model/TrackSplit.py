from Model.LinearAlgebra import LinearAlgebra


class TrackSplit:
    def __init__(self, source_dict: dict, down_sample=1):
        self.name = list(source_dict.keys())[0]
        self.vector = LinearAlgebra.create_vector(source_dict[self.name], down_sample=down_sample)
