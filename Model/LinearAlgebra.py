class LinearAlgebra:
    @staticmethod
    def create_point(source_dict: dict, down_sample=1):
        return [int(source_dict["Y"] / down_sample), int(source_dict["X"] / down_sample)]

    @staticmethod
    def create_vector(source_dict: dict, down_sample=1):
        return (
            [int(source_dict["from"]["Y"] / down_sample), int(source_dict["from"]["X"] / down_sample)],
            [int(source_dict["to"]["Y"] / down_sample), int(source_dict["to"]["X"] / down_sample)]
        )

    @staticmethod
    def create_vector_halfway(vector):
        return [int((vector[0][0] + vector[1][0]) / 2), int((vector[0][1] + vector[1][1]) / 2)]

    @staticmethod
    def check_incision_of_sections(section1, section2):
        i2 = None
        if section1[1][1] - section1[0][1] == 0:
            i2 = section1[1][1]
            m1 = None
        else:
            m1 = (section1[1][0] - section1[0][0]) / (section1[1][1] - section1[0][1])

        if section2[1][1] - section2[0][1] == 0:
            if i2 is not None and i2 != section2[1][1]:
                return False
            i2 = section2[1][1]
            m2 = None
        else:
            m2 = (section2[1][0] - section2[0][0]) / (section2[1][1] - section2[0][1])

        if m1 == m2:
            return False  # no incision

        if i2 is None:
            i2 = (section2[0][0] - m2 * section2[0][1] - section1[0][0] + m1 * section1[0][1]) / (m1 - m2)

        if m1 is None:
            i1 = section2[0][0] - m2 * section2[0][1] + m2 * i2
        else:
            i1 = section1[0][0] - m1 * section1[0][1] + m1 * i2

        if (min(section1[0][0], section1[1][0]) <= i1 <= max(section1[0][0], section1[1][0])
                and min(section1[0][1], section1[1][1]) <= i2 <= max(section1[0][1], section1[1][1])
                and min(section2[0][0], section2[1][0]) <= i1 <= max(section2[0][0], section2[1][0])
                and min(section2[0][1], section2[1][1]) <= i2 <= max(section2[0][1], section2[1][1])):
            return True

        return False
